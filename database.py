# 01. 라이브러리 및 도구 가져오기 (Import)
from sqlalchemy import create_engine, Column, Integer, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
'''
SQLAlchemy: 파이썬 코드로 DB를 다룰 수 있게 해준다. 
SQL 문법을 직접 쓰지 않고도 파이썬 객체로 데이터를 관리할 수 있음.

declarative_base: 나중에 만들 모델 클래스(레코드, 목표)의 부모클래스 역할을 한다
이 부모를 상속받아야 SQLAlchemy가 '아 이 클래스는 DB테이블이구나'라고 인식함.
'''

# 02. DB연결설정 (Engine & Session)
DATABASE_URL = "sqlite:///./water_log.db"
##어떤 DB를 쓸 지 결정: 여기서는 SQLite를 사용하고, 파일 이름은 water_log.db임
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
##Fastapi같은 비동기 환경에서도 여러 요청이 들어와도 문제없도록 설정함 (False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
##모든 테이블 모델의 기초가 되는 클래스를 생성함


# 03. 테이블 설계도 (Models)
# (1) Record: 물 마신 기록 테이블
class Record(Base):
    __tablename__ = "records" # 실제 DB에 생길 테이블 이름
    id = Column(Integer, primary_key=True, index=True) # 고유 번호 (PK)
    amount = Column(Integer) # 마신 양 (정수)
    drunk_at = Column(DateTime, default=datetime.now) # 마신 시각 (기본값은 현재 시간)

# (2) Goal: 하루 목표 테이블
class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    target = Column(Integer) #하루 목표량 (예: 2000ml)
    date = Column(Date) #어느 날짜의 목표인지


# 04. 실제 DB 테이블 생성 (execution)
Base.metadata.create_all(bind=engine)
## 위의 Base를 상속받아 만든 모든 클래스(record, goal) 정보를 읽어서
## 실제 DB 파일(water_log.db)안에 테이블을 만들어라는 명령어


'''
이 코드가 실행되고나면 폴더에 water_log.db라는 파일이 생길 것. 
'''