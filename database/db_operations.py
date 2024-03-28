# db_operations.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from .init_db import Base, Prompt, PromptCategory, TestResult

# # 데이터베이스 세션 설정
# engine = create_engine('sqlite:///database/app_data.db')
# Session = sessionmaker(bind=engine)

# # 한국 시간대 설정
# kst = pytz.timezone('Asia/Seoul')

def create_prompt(system_prompt, user_prompt, model, temperature, maximum_length, category_name):
    """새로운 프롬프트를 생성하고 데이터베이스에 저장합니다."""
    category = session.query(PromptCategory).filter_by(category_name=category_name).first()
    if not category:
        category = PromptCategory(category_name=category_name)
        session.add(category)
        session.commit()
    
    prompt = Prompt(
        generated_date=datetime.now(kst),
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=temperature,
        maximum_length=maximum_length,
        category=category
    )
    session.add(prompt)
    session.commit()
    session.close()

def get_prompts_by_category(category_name):
    """주어진 카테고리 이름에 해당하는 모든 프롬프트를 조회합니다."""
    session = Session()
    category = session.query(PromptCategory).filter_by(category_name=category_name).first()
    if category:
        prompts = session.query(Prompt).filter_by(category_id=category.id).all()
        session.close()
        return prompts
    session.close()
    return []

def create_test_result(tester_name, tester_team, input, output, prompt_id, user_confirmation, user_feedback):
    """새로운 테스트 결과를 생성하고 데이터베이스에 저장합니다."""
    session = Session()
    test_result = TestResult(
        tester_name=tester_name,
        tester_team=tester_team,
        test_date=datetime.now(kst),
        input=input,
        output=output,
        prompt_id=prompt_id,
        user_confirmation=user_confirmation,
        user_feedback=user_feedback
    )
    session.add(test_result)
    session.commit()
    session.close()

def get_test_results_by_prompt(prompt_id):
    """특정 프롬프트 ID에 해당하는 모든 테스트 결과를 조회합니다."""
    session = Session()
    results = session.query(TestResult).filter_by(prompt_id=prompt_id).all()
    session.close()
    return results


def create_prompt_category(category_name):
    """새로운 프롬프트 카테고리를 생성하고 데이터베이스에 저장합니다."""
    session = Session()
    # 카테고리 중복 체크
    existing_category = session.query(PromptCategory).filter_by(category_name=category_name).first()
    if not existing_category:
        new_category = PromptCategory(category_name=category_name)
        session.add(new_category)
        session.commit()
        print(f"Category '{category_name}' added successfully.")
    else:
        print(f"Category '{category_name}' already exists.")
    session.close()
