# Phase 1 - Step 1.5：執行指令

## 📦 一、環境與專案準備

### 1.1 切換到專案根目錄

```bash
cd Visual_Question_Answering\(VQA\)
```
> 確認目錄下已存在：
> - `src/retrieval/`
> - `src/pipeline/`
> - `tests/unit/`
> - `tests/integration/`

### 1.2 啟用虛擬環境（如有）

```bash
python -m venv .venv
source .venv/bin/activate
```

### 1.3 安裝必要套件

```bash
pip install -U pip
pip install transformers torch torchvision
pip install qwen-vl-utils
pip install accelerate bitsandbytes
pip install opencv-python pillow
pip install sentence-transformers
pip install chromadb
pip install pytest pytest-asyncio pytest-cov
pip install flake8 mypy black isort
pip install pydantic pydantic-settings
```

### 1.4 驗證套件安裝

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import transformers; print(f'Transformers version: {transformers.__version__}')"
python -c "from sentence_transformers import SentenceTransformer; print('OK')"
python -c "import chromadb; print('OK')"
```

## 🏗 二、階段 1：VLM 影片解析模組開發指令

### 2.1 建立目錄與基本檔案

```bash
mkdir -p src/vlm
mkdir -p tests/unit/vlm
touch src/vlm/__init__.py src/vlm/config.py src/vlm/models.py src/vlm/exceptions.py src/vlm/video_processor.py src/vlm/client.py
touch tests/unit/vlm/__init__.py tests/unit/vlm/test_config.py tests/unit/vlm/test_models.py tests/unit/vlm/test_video_processor.py tests/unit/vlm/test_client.py
tree src/vlm
tree tests/unit/vlm
```

### 2.2~2.7（略，詳見原始指令檔）

## 🏗 三、階段 2：Retrieval 索引功能補完指令

### 3.1 建立新檔案

```bash
touch src/retrieval/embedding.py
touch src/retrieval/vectorstore.py
touch tests/unit/retrieval/test_embedding.py
touch tests/unit/retrieval/test_vectorstore.py
```

### 3.2~3.5（略，詳見原始指令檔）

## 🏗 四、階段 3：E2E 驗證腳本指令

### 4.1 建立腳本與資料目錄

```bash
mkdir -p scripts data/events data/test_queries reports
touch scripts/vlm_process_video.py scripts/rag_index_events.py scripts/rag_query_test.py scripts/verify_e2e_full.py
touch data/test_queries/queries.json
chmod +x scripts/*.py
```

### 4.2~4.6（略，詳見原始指令檔）

## 🧪 五、整合測試指令

### 5.1~5.2（略，詳見原始指令檔）

## 🧹 六、程式碼品質與靜態檢查

### 6.1~6.4（略，詳見原始指令檔）

## 📥 七、綜合指令（Makefile）

### 7.1~7.2（略，詳見原始指令檔）

## 📋 八、標準驗收執行步驟

### 步驟 1~8（略，詳見原始指令檔）

---
