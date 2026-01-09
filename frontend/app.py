import streamlit as st
import requests
import os
import math

VQA_API_URL = os.getenv("VQA_API_URL", "http://localhost:8000/api/vqa")

st.set_page_config(page_title="VQA 查詢系統 v2", layout="wide")
st.title("安防監控 VQA 查詢系統（v2 頁籤分頁/雙欄）")

query = st.text_input("請輸入查詢問題（如：昨天下午大廳有異常活動嗎？）", "")

if st.button("送出查詢", key="v2") and query.strip():
    with st.spinner("查詢中..."):
        try:
            resp = requests.post(
                VQA_API_URL,
                json={"query": query},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            events = data.get("events", [])
            # 僅保留 answer 的值（若 answer 為 dict 則取其 "answer" 欄位）
            answer_val = data.get("answer", "")
            if isinstance(answer_val, dict):
                answer_val = answer_val.get("answer", "")
            answer = answer_val
            col_left, col_right = st.columns([1, 2])
            with col_left:
                st.subheader("AI 摘要")
                # 僅顯示 LLM 結論，不顯示事件明細
                summary = answer.split("回答問題：")[-1].strip() if "回答問題：" in answer else answer
                st.success(summary)
            with col_right:
                st.subheader("事件列表")
                page_size = 4
                total_pages = math.ceil(len(events) / page_size)
                if total_pages == 0:
                    st.info("查無事件")
                else:
                    tabs = st.tabs([f"第 {i+1} 頁" for i in range(total_pages)])
                    for page_idx, tab in enumerate(tabs):
                        with tab:
                            start = page_idx * page_size
                            end = min(start + page_size, len(events))
                            page_events = events[start:end]
                            grid = [page_events[i:i+2] for i in range(0, len(page_events), 2)]
                            for row in grid:
                                cols = st.columns(2)
                                for idx, evt in enumerate(row):
                                    with cols[idx]:
                                        eid = evt.get('id', '')
                                        ts = evt.get('timestamp', '') or '不明'
                                        desc = evt.get('description', '')
                                        score = evt.get('score', '')
                                        try:
                                            score = f"{float(score):.4f}"
                                        except Exception:
                                            pass
                                        st.markdown(
                                            f"**事件編號：** {eid}<br>"
                                            f"**時間：** {ts}<br>"
                                            f"**描述：** {desc}<br>"
                                            f"**分數：** {score}",
                                            unsafe_allow_html=True
                                        )
                                        if evt.get("image_url"):
                                            st.image(evt["image_url"], caption="event snapshot", width=200)
            # 回饋區
            st.subheader("本次回答是否滿意？")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 滿意", key="v2-sat"):
                    requests.post(VQA_API_URL + "/feedback", json={
                        "query": query,
                        "answer": answer,
                        "feedback": "satisfied"
                    })
                    st.info("感謝您的回饋！")
            with col2:
                if st.button("👎 不滿意", key="v2-unsat"):
                    feedback_text = st.text_input("請簡述不滿意原因", key="v2-fb")
                    if st.button("送出不滿意回饋", key="v2-fb-btn"):
                        requests.post(VQA_API_URL + "/feedback", json={
                            "query": query,
                            "answer": answer,
                            "feedback": "unsatisfied",
                            "comment": feedback_text
                        })
                        st.info("已收到您的意見，感謝！")
        except Exception as e:
            st.error(f"查詢失敗：{e}")

st.caption("© 2025 VQA Multi-Agent Squad v2")
