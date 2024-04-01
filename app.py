# https://claude.ai/chat/9771b639-b9b7-40c5-b8c0-70c858e97c84 여기 링크 참고해서 진행.

import streamlit as st
from database.db_operations import create_prompt, get_prompts_by_category, create_test_result, get_test_results_by_prompt
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from prompts import system_prompt_1, user_prompt_1
from views import intro

try:
  client = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
  client = AsyncOpenAI()

model_list = ["gpt-3.5-turbo", "gpt-4", "gpt-4-0125-preview"]

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
        with st.expander("실행 될 Prompt 자세히 보기"):
            tab1, tab2, tab3, tab4 = st.tabs(["Prompt-1", "Prompt-2", "Prompt-3","Prompt-4"])

        with tab1:
            st.text_area("System Prompt", system_prompt_1)
            st.text_area("User Prompt", user_prompt_1)
                            
                # 사용자로부터 숫자 입력받기
            st.text("Parameters")
            with st.container(border=True):
                model = st.selectbox("GPT Model", model_list, index=None, placeholder="gpt-4")
                temperature = st.slider('Temperature', 0.0, 1.0, 0.5, step=0.1)
                top_p = st.slider('Top_P', 0.0, 1.0, 1.0, step=0.1)
                max_tokens = st.slider('Maximum Length', 0, 4000, 2000, step=100)
                st.divider()
                st.markdown(
                    f"""
        🌡️ Temperature : {temperature}

        🎲 Top_P : {top_p}

        📏 Maximum Length : {max_tokens}
        """
        )
        
        sender = st.text_input("보내는 사람 이름")
        reciepent = st.text_input("받는 사람 이름")
        purpose = st.text_area("이메일 작성 목적")
        additional = st.text_area("참고 이메일(Optional)")
        tone = st.selectbox("어조",
   ("Casual", "Professional", "Formal"),
   index=None,
   placeholder="Professional",
)

        language = st.selectbox(
        "출력언어",
        ("English", "French", "Russian"),
        index=None,
        placeholder="English"
)
 
        with st.sidebar:
            # 얘들을 입력 항목들로 채워주자.
            st.divider()

            st.subheader("만족하는 결과를 체크하고 투표")
            vote_1 = st.checkbox("1번 결과")
            vote_2 = st.checkbox("2번 결과")
            vote_3 = st.checkbox("3번 결과")
            vote_4 = st.checkbox("4번 결과")
            vote = st.button("vote")
            # 버튼을 누르면 email 결과물에 대한 투표 결과가 저장 됨. (csv에 저장하면 될 듯.)

        async def generate_email(system_prompt, user_prompt, model, temperature, topp, max_tokens):
            stream = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=topp
            )
            generated_text = st.empty()
            streamed_text = ""
            async for chunk in stream:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content is not None:
                    streamed_text += chunk_content
                    generated_text.markdown(streamed_text)
                    await asyncio.sleep(0.05)

        async def main():
            await generate_email(system_prompt_1, user_prompt_1, model_list[0], 0.5, 1, 1000)

        generate = st.button("생성 시작", type='primary', use_container_width=True)

        if generate:
            asyncio.run(main())
            
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
    "테스트할 항목 선택": intro,
    "이메일 생성": gen_email,
    "레터 분석": letter_analysis,
    "Proofreading": proofreading
}


#사이드바 제목
with st.sidebar: 
    st.title("BAROLETTER PROMPT FEEDBACK 📝")
    st.divider()


user_name = st.sidebar.text_input("테스터 이름 : ")
user_team = st.sidebar.text_input("소속팀 : ")
test_name = st.sidebar.selectbox("선택하여 테스트 진행", page_names_to_funcs.keys())
page_names_to_funcs[test_name]()
