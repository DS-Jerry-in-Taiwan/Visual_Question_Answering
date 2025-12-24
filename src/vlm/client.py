import logging
import json
import uuid
import os
from datetime import datetime
from typing import List
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
import torch

from src.vlm.config import VLMConfig
from src.vlm.models import Frame, VLMResult
from src.vlm.exceptions import ModelLoadError, InferenceError

logger = logging.getLogger(__name__)

class VLMClient:
    """
    VLMClient: 負責載入 Qwen2-VL 模型並對影片幀進行推理。
    """
    def __init__(self, config: VLMConfig):
        self.config = config
        self.model = None
        self.processor = None
        self._load_model()

    def _load_model(self):
        try:
            logger.info(f"載入模型: {self.config.model_name}")
            self.processor = AutoProcessor.from_pretrained(
                self.config.model_name,
                trust_remote_code=getattr(self.config, "trust_remote_code", True)
            )

            if self.config.use_quantization:
                from transformers import BitsAndBytesConfig
                quant_config = BitsAndBytesConfig(load_in_8bit=True)
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    self.config.model_name,
                    device_map=self.config.device,
                    quantization_config=quant_config,
                    trust_remote_code=True
                )
            else:
                self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                    self.config.model_name,
                    device_map=self.config.device,
                    trust_remote_code=True
                )
            logger.info("模型載入成功")
        except Exception as e:
            logger.error(f"模型載入失敗: {e}")
            raise ModelLoadError(f"模型載入失敗: {e}") from e

    def process_frames(self, frames: List[Frame], video_path: str, segment_size: int = 1) -> list:
        """
        將 frames 切分為多個片段，批次推論，彙整多事件結果。
        segment_size: 每段包含的 frame 數量
        """
        try:
            logger.info(f"開始處理 {len(frames)} 幀，分段大小: {segment_size}")
            all_events = []
            for seg_idx in range(0, len(frames), segment_size):
                segment_frames = frames[seg_idx:seg_idx+segment_size]
                if not segment_frames:
                    continue
                images = []
                valid_frames = []
                for frame in segment_frames:
                    if not os.path.isfile(frame.image_path):
                        logger.warning(f"檔案不存在，跳過: {frame.image_path}")
                        continue
                    try:
                        from PIL import Image
                        image = Image.open(frame.image_path)
                        images.append(image)
                        valid_frames.append(frame)
                    except Exception as e:
                        logger.warning(f"無法開啟圖片，跳過: {frame.image_path}, error: {e}")
                        continue
                if not valid_frames:
                    continue
                # 批次 messages
                messages_batch = [self._build_prompt([frame], multi_event=True)[0] for frame in valid_frames]
                texts = [
                    self.processor.apply_chat_template(
                        [msg],
                        tokenize=False,
                        add_generation_prompt=True
                    ) for msg in messages_batch
                ]
                inputs = self.processor(
                    text=texts,
                    images=images,
                    return_tensors="pt"
                ).to(self.config.device)
                with torch.no_grad():
                    generated_ids = self.model.generate(
                        **inputs,
                        max_new_tokens=self.config.max_new_tokens,
                        temperature=self.config.temperature,
                        do_sample=self.config.do_sample,
                        top_p=self.config.top_p
                    )
                generated_ids_trimmed = [
                    out_ids[len(in_ids):]
                    for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                for idx, output_text in enumerate(self.processor.batch_decode(
                    generated_ids_trimmed,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False
                )):
                    logger.info(f"VLM 輸出: {output_text}")
                    segment_events = self._parse_multi_event_response(
                        output_text, video_path, seg_idx, [valid_frames[idx]]
                    )
                    all_events.extend(segment_events)
            return all_events
        except Exception as e:
            logger.error(f"VLM 多事件推理失敗: {e}")
            raise InferenceError(f"VLM 多事件推理失敗: {e}") from e

    def _parse_multi_event_response(self, response: str, video_path: str, seg_idx: int, segment_frames: list) -> list:
        """
        解析模型回傳的多事件 JSON 陣列，並補充片段資訊。
        """
        if not segment_frames:
            return []
        try:
            response = response.strip()
            # 處理 markdown code block
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            # 解析 JSON
            data = json.loads(response)
            if not isinstance(data, list) or len(segment_frames) == 0:
                logger.warning(f"多事件 JSON 不是陣列，response: {response[:200]}")
                return []
            events = []
            # 安全取得時間
            start_time = segment_frames[0].timestamp if segment_frames and len(segment_frames) > 0 else None
            end_time = segment_frames[-1].timestamp if segment_frames and len(segment_frames) > 0 else None
            for event in data:
                event_id = f"evt_{uuid.uuid4().hex[:8]}"
                events.append({
                    "event_id": event_id,
                    "video_path": video_path,
                    "segment_index": seg_idx,
                    "start_time": start_time,
                    "end_time": end_time,
                    "timestamp": datetime.now().isoformat(),
                    "summary": event.get("summary", ""),
                    "zone": event.get("zone"),
                    "activity": event.get("activity"),
                    "objects": event.get("objects"),
                    "person_count": event.get("person_count"),
                    "confidence": event.get("confidence", 0.8),
                    "raw_output": json.dumps(event, ensure_ascii=False),
                    "processed_at": datetime.now().isoformat()
                })
            return events
        except Exception as e:
            logger.warning(f"多事件 JSON 解析失敗: {e}，response: {response[:200]}")
            return []

    def _build_prompt(self, frames: List[Frame], multi_event: bool = True) -> List[dict]:
        content = []
        for i, frame in enumerate(frames):
            content.append({"type": "image"})
        if multi_event:
            prompt_text = """請分析這些監控影片畫面，針對本片段所有可疑行為，輸出 JSON 陣列，每個元素為一事件。

輸出格式（務必是有效的 JSON 陣列）：
[
  {
    "summary": "事件摘要（簡短描述發生了什麼）",
    "zone": "區域（例如：hallway, parking, entrance）",
    "activity": "活動類型（例如：walking, fighting, loitering, vandalism）",
    "objects": ["物體1", "物體2"],
    "person_count": 人數（整數）
  }
]

範例：
[
  {
    "summary": "有人在走廊徘徊",
    "zone": "hallway",
    "activity": "loitering",
    "objects": ["person", "door"],
    "person_count": 1
  },
  {
    "summary": "有人在停車場打架",
    "zone": "parking",
    "activity": "fighting",
    "objects": ["person", "car"],
    "person_count": 3
  }
]

請只輸出 JSON 陣列，不要有其他說明文字。"""
        else:
            prompt_text = """請分析這些監控影片畫面，並以 JSON 格式輸出事件描述。

輸出格式（務必是有效的 JSON）：
{
    "summary": "事件摘要（簡短描述發生了什麼）",
    "zone": "區域（例如：hallway, parking, entrance）",
    "activity": "活動類型（例如：walking, fighting, loitering, vandalism）",
    "objects": ["物體1", "物體2"],
    "person_count": 人數（整數）
}

範例：
{
    "summary": "有人在走廊徘徊",
    "zone": "hallway",
    "activity": "loitering",
    "objects": ["person", "door"],
    "person_count": 1
}

請只輸出 JSON，不要有其他說明文字。"""
        content.append({
            "type": "text",
            "text": prompt_text
        })
        messages = [{"role": "user", "content": content}]
        return messages

    def _parse_response(self, response: str, video_path: str) -> dict:
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            data = json.loads(response)
            event_id = f"evt_{uuid.uuid4().hex[:8]}"
            return {
                "event_id": event_id,
                "video_path": video_path,
                "timestamp": datetime.now().isoformat(),
                "summary": data.get("summary", ""),
                "zone": data.get("zone"),
                "activity": data.get("activity"),
                "objects": data.get("objects"),
                "person_count": data.get("person_count"),
                "confidence": 0.8,
                "raw_output": response,
                "processed_at": datetime.now().isoformat()
            }
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 解析失敗: {e}")
            return {
                "event_id": f"evt_{uuid.uuid4().hex[:8]}",
                "video_path": video_path,
                "timestamp": datetime.now().isoformat(),
                "summary": response[:200],
                "zone": None,
                "activity": None,
                "objects": None,
                "person_count": None,
                "confidence": 0.5,
                "raw_output": response,
                "processed_at": datetime.now().isoformat()
            }
