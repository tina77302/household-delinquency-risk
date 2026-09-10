import streamlit as st

st.set_page_config(
    page_title="가계 장기연체 위험 예측",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 가계 장기연체 위험 예측")
st.subheader("미시 패널자료와 머신러닝·딥러닝을 활용한 취약가구 분류")

st.markdown("""
### Research Question

**현재 가구의 재무정보를 활용하여  
다음 해 30일 이상 장기연체 위험가구를 사전에 식별할 수 있는가?**
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("OOT 분석대상", "6,607가구")
col2.metric("실제 장기연체", "173가구")
col3.metric("장기연체율", "2.62%")
col4.metric("최종모형", "XGBoost")
