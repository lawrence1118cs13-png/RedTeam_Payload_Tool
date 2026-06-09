import streamlit as st
import requests

# 設定網頁標題與外觀
st.set_page_config(page_title="Red Team Payload Tool", page_icon="🛡️", layout="centered")

st.title("🛡️ Red Team Payload Generator")
st.markdown("這是一個基於 FastAPI 後端的紅隊 Payload 自動生成與編碼測試工具。")

# 建立輸入區塊
with st.container():
    st.subheader("1. 輸入攻擊參數")
    raw_payload = st.text_area("請輸入原始 Payload:", value="' OR 1=1--", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        max_len = st.number_input("最大長度限制 (WAF 模擬):", min_value=10, max_value=200, value=50)
    with col2:
        enc_type = st.selectbox("特徵編碼轉換方式:", ["none", "sqli"])

# 建立按鈕與串接後端 API
if st.button("🚀 生成繞過 Payload", type="primary"):
    if not raw_payload.strip():
        st.warning("⚠️ Payload 不能為空白喔！")
    else:
        with st.spinner("API 處理中..."):
            # 準備要傳給 FastAPI 的資料格式
            api_url = "http://127.0.0.1:8000/api/v1/generate"
            payload_data = {
                "payload": raw_payload,
                "max_length": int(max_len),
                "encode_type": enc_type
            }
            
            try:
                # 發送 POST 請求給後端
                response = requests.post(api_url, json=payload_data)
                result = response.json()
                
                if response.status_code == 200:
                    st.success("✅ 生成成功！")
                    st.markdown("### 輸出結果")
                    st.code(result.get("generated_payload"), language="sql")
                    st.info(f"📏 最終長度: {result.get('final_length')} 字元")
                else:
                    # 觸發後端寫好的例外處理
                    st.error(f"❌ 發生錯誤: {result.get('detail')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 無法連線到後端伺服器！請確認 FastAPI (uvicorn) 是否已啟動。")