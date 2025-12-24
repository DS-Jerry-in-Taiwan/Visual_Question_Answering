import cv2
from typing import List
from src.vlm.models import Frame, VideoMetadata
from src.vlm.exceptions import VideoReadError
import argparse
import json
from src.vlm.client import VLMClient

class Config:
    max_frames = 16

class VideoProcessor:
    """
    VideoProcessor: 影片讀取、幀採樣與元資料擷取。
    """
    def __init__(self, config):
        self.config = config

    def get_video_metadata(self, video_path: str) -> VideoMetadata:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise VideoReadError(f"無法開啟影片: {video_path}")
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return VideoMetadata(
            duration=duration,
            fps=fps,
            frame_count=frame_count,
            resolution=f"{width}x{height}"
        )

    def process_video(self, video_path: str) -> List[Frame]:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise VideoReadError(f"無法開啟影片: {video_path}")
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_count = min(self.config.max_frames, frame_count)
        interval = max(frame_count // sample_count, 1)
        frames = []
        for i in range(sample_count):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
            ret, frame = cap.read()
            if not ret:
                continue
            image_path = f"/tmp/frame_{i}.jpg"
            cv2.imwrite(image_path, frame)
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            frames.append(Frame(frame_id=i, timestamp=timestamp, image_path=image_path))
        cap.release()
        return frames

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Processor CLI")
    parser.add_argument("--input", required=True, help="Input video file path")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--max_frames", type=int, default=16, help="Max frames to sample")
    args = parser.parse_args()

    config = Config()
    config.max_frames = args.max_frames

    processor = VideoProcessor(config)
    try:
        metadata = processor.get_video_metadata(args.input)
        frames = processor.process_video(args.input)
        from src.vlm.config import VLMConfig
        vlm_client = VLMClient(VLMConfig())
        vlm_events = vlm_client.process_frames(frames, args.input, segment_size=1)
        output = {
            "metadata": metadata.model_dump(),
            "events": vlm_events
        }
        with open(args.output, "w") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Output written to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
