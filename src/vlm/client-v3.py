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

    def process_frames(self, frames: List[Frame], video_path: str, segment_size: int = 4) -> list:
        """
        將 frames 切分為多個片段，逐段推論，彙整多事件結果。
        segment_size: 每段包含的 frame 數量
        """
        try:
            logger.info(f"開始處理 {len(frames)} 幀，分段大小: {segment_size}")
            all_events = []
            for seg_idx in range(0, len(frames), segment_size):
                segment_frames = frames[seg_idx:seg_idx+segment_size]
                if not segment_frames:
                    continue
                print(f"segment_frames: {segment_frames}")
                try:
                    for frame in segment_frames:
                        print(f"step 0: 檢查 frame.image_path: {frame.image_path}")
                        if not os.path.isfile(frame.image_path):
                            print(f"檔案不存在，跳過: {frame.image_path}")
                            logger.warning(f"檔案不存在，跳過: {frame.image_path}")
                            continue
                        try:
                            from PIL import Image
                            image = Image.open(frame.image_path)
                        except Exception as e:
                            print(f"無法開啟圖片，跳過: {frame.image_path}, error: {e}")
                            logger.warning(f"無法開啟圖片，跳過: {frame.image_path}, error: {e}")
                            continue
                        print("step 1: 準備 prompt")
                        messages = self._build_prompt([frame], multi_event=True)
                        print(f"messages: {messages}")
                        print(f"image type: {type(image)}")
                        print(f"images list type: {[type(img) for img in [image]]}")
                        
                        print("processor id:", id(self.processor))
                        print("processor type:", type(self.processor))
                        print("processor chat_template:", getattr(self.processor, "chat_template", None))
                        print("transformers version:", __import__("transformers").__version__)
                        
                        text = self.processor.apply_chat_template(
                            messages,
                            tokenize=False,
                            add_generation_prompt=True
                        )
                        print(f"text: {repr(text)}")
                        if not text.strip():
                            # 新增：將 messages 輸出到 JSON 檔
                            dump_path = f"/tmp/debug_messages_{frame.frame_id}.json"
                            with open(dump_path, "w", encoding="utf-8") as f:
                                json.dump(messages, f, ensure_ascii=False, indent=2)
                            print(f"已輸出 messages 至 {dump_path}")
                            print(f"警告：產生的 prompt 為空，跳過 frame: {frame}")
                            logger.warning(f"產生的 prompt 為空，跳過 frame: {frame}")
                            continue
                        print("step 2: processor 輸入")
                        inputs = self.processor(
                            text=[text],
                            images=[image],
                            return_tensors="pt"
                        ).to(self.config.device)
                        print(f"inputs.input_ids: {inputs.input_ids}")
                        print("step 3: model generate")
                        with torch.no_grad():
                            generated_ids = self.model.generate(
                                **inputs,
                                max_new_tokens=self.config.max_new_tokens,
                                temperature=self.config.temperature,
                                do_sample=self.config.do_sample,
                                top_p=self.config.top_p
                            )
                        print("generated_ids:", generated_ids)
                        print("decode all:", self.processor.batch_decode(generated_ids, skip_special_tokens=False))

                        generated_ids_trimmed = [
                            out_ids[len(in_ids):]
                            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                        ]
                        print("decode trimmed:", self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=False))
                        print("decode trimmed (skip_special_tokens=True):", self.processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True))
                        print("generated_ids_trimmed:", generated_ids_trimmed)
                        print("generated_ids_trimmed lens:", [len(x) for x in generated_ids_trimmed])

                        output_text = self.processor.batch_decode(
                            generated_ids_trimmed,
                            skip_special_tokens=True,
                            clean_up_tokenization_spaces=False
                        )[0]
                        logger.info(f"VLM 輸出: {output_text}")
                        segment_events = self._parse_multi_event_response(
                            output_text, video_path, seg_idx, [frame]
                        )
                        all_events.extend(segment_events)
                except Exception as inner_e:
                    print(f"!!! Inner error in segment {seg_idx}: {inner_e}")
                    logger.error(f"VLM 單段推理失敗: {inner_e}")
                    continue
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

    def _build_prompt(self, frames: List[Frame], multi_event: bool = False) -> List[dict]:
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
