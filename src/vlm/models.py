from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Frame(BaseModel):
    frame_id: int
    timestamp: float
    image_path: str

class VideoMetadata(BaseModel):
    duration: float
    fps: float
    frame_count: int
    resolution: str

class VLMResult(BaseModel):
    event_id: str
    video_path: str
    timestamp: str
    summary: str
    zone: Optional[str]
    activity: Optional[str]
    objects: List[str]
    person_count: int
    raw_output: str
    processed_at: datetime

    def to_indexable_text(self) -> str:
        return f"{self.summary} | {self.zone} | {self.activity} | {', '.join(self.objects)}"
