import streamlit as st
from database.db_operations import create_prompt, get_prompts_by_category, create_test_result, get_test_results_by_prompt
from openai import OpenAI
import pandas

model_list = ["gpt-3.5-turbo", "gpt-4", "gpt-4-0125-preview"]

default_prompt = ["This is Default Prompt. You are AI, you can do everyting {hello}"]
# 프롬프트
system_prompt_1 = """
    As an AI language model tasked with composing email in a construction company.
    
    Your task is to compose a formal email, specifying both its title and detailed contents.
    
    Email Requirements:
    
    - Title: Clearly state the subject of the email in the title.
    
    - Contents:
    
    - Introduction: Brief introduction of the purpose of the email.
    
    - Main Body: Detailed explanation of the key points, adhering to the instructions provided.
    
    - Conclusion: Concise closing with a call to action or request for a response.
    
    Guidelines:
    
    - Create an email that is concise, formal, and professional.
    
    - Ensure the message includes all necessary information without adding extraneous details.
    
    - The email should be clear and direct, following business email etiquette.
    
    - Briefly address the previous opponent's email, if there is one.
    
    - Avoid excessive gratitude or pleasantries, focusing instead on the specified information and requests.
    
    - Write the email in {language} with {tone} manners.
    """

user_prompt_1 = """
    <Information>
    
    - Email history for more information: {received}
    
    - The Sender of this email: {sender}
    
    - Recipient: {recipient}
    
    - Content: {content}
    """




# Intro 페이지
def intro():
    import streamlit as st

    st.title("BaroLetter Prompt Engineering")
    st.markdown("우리함께 프롬프트를 만들어보아요! 👋")
    st.sidebar.success("테스트시작 하기 전 성함과 소속팀을 입력하시고, 테스트 항목을 선택하세요.")

    st.markdown(
        """

        **👈 옆에 메뉴에서 테스트할 메뉴를 선택합니다.**

        
        현재 이메일 작성, 레터 분석 및 회신, Proofreading 테스트를 진행하고 있습니다.

        
        ### 바로레터 개발 문서

        - Check out [Baroletter (개발중)](https://streamlit.io)
    """
    )

# 이메일 생성 페이지
def gen_email():
    import streamlit as st
    from urllib.error import URLError

    # 제목과 소개말
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.markdown(
        """내용을 입력하고 생성 버튼을 클릭하면 새로운 생성이 시작됩니다.🚀 

만족스러운 결과물을 제공한 **Prompt**에 대해
1. 복수개 선택🌟
2. 피드백📝을 남기고 
3. 투표하기🗳️를 눌러주세요.

"""
    )

    # 구분선    
    st.divider()

    # 본문
    try:
        st.sidebar.markdown("### 입력 정보")
        with st.expander("실행 될 Prompt 자세히 보기"):
            tab1, tab2, tab3, tab4 = st.tabs(["Prompt-1", "Prompt-2", "Prompt-3","Prompt-4"])

        with tab1:
            st.text_area("System Prompt", system_prompt_1)
            st.text_area("User Prompt", user_prompt_1)
                            
                # 사용자로부터 숫자 입력받기
            st.text("Parameters")
            with st.container(border=True):
                model = st.selectbox("GPT Model", model_list,
   index=None,
   placeholder="gpt-4",
)
                temperature = st.slider('Temperature', 0.0, 1.0, 0.5, step=0.1)
                top_p = st.slider('Top_P', 0.0, 1.0, 1.0, step=0.1)
                maximum_length = st.slider('Maximum Length', 0, 4000, 2000, step=100)
                st.divider()
                st.markdown(
                    f"""
        🌡️ Temperature : {temperature}

        🎲 Top_P : {top_p}

        📏 Maximum Length : {maximum_length}
        """
        )
        
        sender = st.text_input("보내는 사람 이름")
        reciepent = st.text_input("받는 사람 이름")
        purpose = st.text_area("이메일 작성 목적")
        additional = st.text_area("참고 이메일(Optional)")
        tone = st.selectbox("어조",
   ("Casual", "Professional", "Formal"),
   index=None,
   placeholder="이메일 어조 선택.",
)

        language = st.selectbox(
        "출력언어",
        ("English", "French", "Russian"),
        index=None,
        placeholder="출력 언어 선택.",
)

        result = st.write('You selected:', sender, reciepent, purpose, additional, tone, language)

        # 정보들을 담아 생성 시작
        if st.button("생성 시작", type='primary', use_container_width=True):
            result = print(result)
            #여기에 Prompt를 갖고와서 gpt를 넣어서 돌아가게 하면 됩니다.



    except URLError as e:
        st.error(
            """
            **Internet connection reqruied.**

            Connection error: %s
        """
            % e.reason
        )

def letter_analysis():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def proofreading():
    import streamlit as st
    import pandas as pd
    import altair as alt
    from urllib.error import URLError

    try:
        print("this")
    except URLError as e:
        st.error(
            """
            **Internet connection reqruied.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "Click & Select": intro,
    "이메일 생성": gen_email,
    "레터 분석": letter_analysis,
    "Proofreading": proofreading
}

test_name = st.sidebar.selectbox("선택하여 테스트 진행", page_names_to_funcs.keys())
user_name = st.sidebar.text_input("테스터 이름 : ")
user_team = st.sidebar.text_input("소속팀 : ")
page_names_to_funcs[test_name]()

