import streamlit as st
# from utils import generate_email

def intro():
    import streamlit as st
    st.title("BaroLetter Prompt Feedback")
    st.markdown("우리함께 프롬프트를 만들어보아요! 👋")
    st.sidebar.success("테스트시작 하기 전 성함과 소속팀을 입력하시고, 테스트 항목을 선택하세요.")
    st.divider()
    st.markdown(
        """

        **👈 옆에 메뉴에서 테스트할 메뉴를 선택합니다.**

        
        현재 이메일 작성, 레터 분석 및 회신, Proofreading 테스트를 진행하고 있습니다.

        
        ### 바로레터 개발 문서

        - Check out [Baroletter (개발중)](https://ntest.daewooenc.com/brls)
    """
    )