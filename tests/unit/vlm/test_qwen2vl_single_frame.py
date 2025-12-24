from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image
import torch
import json

def test_qwen2vl_single_frame(model_name, image_path):
    print(f"Loading model: {model_name}")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_name,
        device_map="auto",
        load_in_8bit=True,
        low_cpu_mem_usage=True
    )
    processor = AutoProcessor.from_pretrained(model_name)
    print(f"Loading image: {image_path}")
    image = Image.open(image_path)
    # 仿照主流程，構建 chat template
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "描述圖片中的場景與人物與事件"}
            ]
        }
    ]
    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    print(f"Prompt after chat_template: {repr(text)}")
    print("Preparing inputs...")
    inputs = processor(
        text=[text],
        images=[image],
        return_tensors="pt"
    ).to("cuda" if torch.cuda.is_available() else "cpu")
    print("Running inference...")
    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=512,   # 增加最大生成 token 數
            temperature=0.7,
            do_sample=True
        )
    print("Decoding output...")
    print("----------------- -----------------")
    output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print("Model output:")
    print(output)

if __name__ == "__main__":
    model_name = "Qwen/Qwen2-VL-7B-Instruct"
    image_path = "/tmp/frame_14.jpg"
    # 執行推論流程
    test_qwen2vl_single_frame(model_name, image_path)

    # 以下是 messages/prompt 測試（可保留）
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "請分析這些監控影片畫面，針對本片段所有可疑行為，輸出 JSON 陣列，每個元素為一事件。\n\n輸出格式（務必是有效的 JSON 陣列）：\n[\n  {\n    \"summary\": \"事件摘要（簡短描述發生了什麼）\",\n    \"zone\": \"區域（例如：hallway, parking, entrance）\",\n    \"activity\": \"活動類型（例如：walking, fighting, loitering, vandalism）\",\n    \"objects\": [\"物體1\", \"物體2\"],\n    \"person_count\": 人數（整數）\n  }\n]\n\n範例：\n[\n  {\n    \"summary\": \"有人在走廊徘徊\",\n    \"zone\": \"hallway\",\n    \"activity\": \"loitering\",\n    \"objects\": [\"person\", \"door\"],\n    \"person_count\": 1\n  },\n  {\n    \"summary\": \"有人在停車場打架\",\n    \"zone\": \"parking\",\n    \"activity\": \"fighting\",\n    \"objects\": [\"person\", \"car\"],\n    \"person_count\": 3\n  }\n]\n\n請只輸出 JSON 陣列，不要有其他說明文字。"}
            ]
        }
    ]
    processor = AutoProcessor.from_pretrained(model_name)
    # print(f"messages: {messages}")
    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    print(f"Prompt after chat_template: {repr(text)}")

    with open("/tmp/debug_messages_14.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    print(f"text: {repr(text)}")
