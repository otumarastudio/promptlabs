# init_db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pytz
from datetime import datetime

Base = declarative_base()

# 한국 시간대(KST) 설정
kst = pytz.timezone('Asia/Seoul')

class PromptCategory(Base):
    __tablename__ = 'prompt_category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100))
    prompts = relationship("Prompt", back_populates="category")

class Prompt(Base):
    __tablename__ = 'prompts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    generated_date = Column(DateTime, default=datetime.now(kst))
    system_prompt = Column(Text)
    user_prompt = Column(Text)
    model = Column(String(50))
    temperature = Column(Float)
    maximum_length = Column(Integer)
    category_id = Column(Integer, ForeignKey('prompt_category.id'))
    test_results = relationship("TestResult", back_populates="prompt")
    category = relationship("PromptCategory", back_populates="prompts")

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tester_name = Column(String(50))
    tester_team = Column(String(50))
    test_date = Column(DateTime, default=datetime.now(kst))
    input = Column(Text)
    output = Column(Text)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    user_confirmation = Column(Boolean)
    user_feedback = Column(Text)
    prompt = relationship("Prompt", back_populates="test_results")

def init_db():
    # 데이터베이스 파일 경로 설정
    db_path = 'sqlite:///database/app_data.db'
    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
