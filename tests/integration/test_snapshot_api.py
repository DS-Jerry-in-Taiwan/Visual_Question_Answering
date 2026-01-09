import os
import pytest
from fastapi.testclient import TestClient
from src.api.vqa_api import app

client = TestClient(app)

def test_snapshot_api_success():
    # 測試影片路徑與時間（需有該影片檔案）
    video_path = "Anomaly-Videos-Part-1/Abuse/Abuse001_x264.mp4"
    t = 17.0
    # 若影片不存在則跳過
    if not os.path.exists(video_path):
        pytest.skip(f"測試影片不存在：{video_path}")
    resp = client.get("/api/snapshot", params={"video_path": video_path, "t": t})
    assert resp.status_code == 200
    data = resp.json()
    assert "image_url" in data
    # 檢查圖片檔案是否已產生
    img_path = data["image_url"].lstrip("/")
    assert os.path.exists(img_path)

def test_snapshot_api_fail():
    # 測試不存在的影片
    resp = client.get("/api/snapshot", params={"video_path": "not_exist.mp4", "t": 1.0})
    assert resp.status_code == 404
    data = resp.json()
    assert "error" in data