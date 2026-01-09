import streamlit as st
import requests
import os

VQA_API_URL = os.getenv("VQA_API_URL", "http://localhost:8000/api/vqa")

st.set_page_config(page_title="VQA 查詢系統", layout="wide")
st.title("安防監控 VQA 查詢系統")

# 查詢輸入區
query = st.text_input("請輸入查詢問題（如：昨天下午大廳有異常活動嗎？）", "")

if st.button("送出查詢") and query.strip():
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
            answer = data.get("answer", "")
            st.subheader("AI 回答")
            st.success(answer)
            st.subheader("檢索事件列表")
            cols = st.columns(2)
            for idx, evt in enumerate(events):
                with cols[idx % 2]:
                    st.markdown(f"- {evt.get('timestamp', '')} | {evt.get('description', '')} (score: {evt.get('score', '')})")
                    if evt.get("image_url"):
                        st.image(evt["image_url"], caption="event snapshot", width=400)
            # 回饋區
            st.subheader("本次回答是否滿意？")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 滿意"):
                    requests.post(VQA_API_URL + "/feedback", json={
                        "query": query,
                        "answer": answer,
                        "feedback": "satisfied"
                    })
                    st.info("感謝您的回饋！")
            with col2:
                if st.button("👎 不滿意"):
                    feedback_text = st.text_input("請簡述不滿意原因", key="fb")
                    if st.button("送出不滿意回饋"):
                        requests.post(VQA_API_URL + "/feedback", json={
                            "query": query,
                            "answer": answer,
                            "feedback": "unsatisfied",
                            "comment": feedback_text
                        })
                        st.info("已收到您的意見，感謝！")
        except Exception as e:
            st.error(f"查詢失敗：{e}")

st.caption("© 2025 VQA Multi-Agent Squad")
