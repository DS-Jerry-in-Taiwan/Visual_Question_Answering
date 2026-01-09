import os

DIRS = [
    "Anomaly-Videos-Part-1",
    "chroma_db",
    "configs",
    "docs",
    "frontend",
    "output",
    "reports",
    "scripts",
    "src",
    "static",
    "tests/data",
    "tests/integration",
    "tests/reports",
    "tests/unit"
]

def ensure_dirs():
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        print(f"已建立/確認目錄: {d}")

def main():
    ensure_dirs()
    print("請將影片檔案放入 Anomaly-Videos-Part-1 目錄。")
    print("如需自訂 config，請參考 configs/default.yaml。")

if __name__ == "__main__":
    main()