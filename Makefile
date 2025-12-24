.PHONY: help install test lint format clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安裝所有依賴
	pip install -r requirements.txt

test:  ## 執行所有測試
	pytest tests/ -v

test-unit:  ## 執行單元測試
	pytest tests/unit/ -v

test-integration:  ## 執行整合測試
	pytest tests/integration/ -v -s

test-coverage:  ## 執行測試並生成覆蓋率報告
	pytest tests/ --cov=src --cov-report=html --cov-report=term -v

lint:  ## 執行程式碼檢查
	flake8 src/ tests/ scripts/ --max-line-length=100
	mypy src/ scripts/ --ignore-missing-imports

format:  ## 格式化程式碼
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

clean:  ## 清理臨時檔案
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf chroma_db_test
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +

test-vlm:  ## 測試 VLM 模組
	pytest tests/unit/vlm/ -v

test-vlm-cov:  ## VLM 模組測試覆蓋率
	pytest tests/unit/vlm/ --cov=src/vlm --cov-report=term --cov-report=html -v

test-retrieval:  ## 測試 Retrieval 模組
	pytest tests/unit/retrieval/ -v

test-retrieval-cov:  ## Retrieval 模組測試覆蓋率
	pytest tests/unit/retrieval/ --cov=src/retrieval --cov-report=term --cov-report=html -v

test-e2e:  ## 執行 E2E 驗證腳本
	python scripts/verify_e2e_full.py

benchmark:  ## 執行效能基準測試
	python scripts/benchmark_performance.py

clean-data:  ## 清理測試資料
	rm -rf ./data/events/*.json
	rm -rf ./chroma_db_test
	rm -rf ./reports/*.md

clean-models:  ## 清理下載的模型（謹慎使用）
	@echo "警告: 此操作將刪除快取的模型"
	@read -p "確定要繼續嗎？ [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf ~/.cache/huggingface/; \
	fi

ci-step15:  ## CI：Phase 1 Step 1.5 完整驗證
	$(MAKE) lint
	$(MAKE) test-vlm-cov
	$(MAKE) test-retrieval-cov
	$(MAKE) test-integration

VIDEO_PATH ?= /path/to/test/video.mp4
QUERY ?= 有人在做什麼？
