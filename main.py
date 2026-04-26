# 01. 필요한 도구들 가져오기 (Import)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Record
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# 02. DB 세션 관리 (get_db)
def get_db():
    db = SessionLocal() #DB일꾼 소환!
    try:
        yield db #일꾼을 api 함수에 빌려준다
    finally:
        db.close() #작업이 끝나면 일꾼을 돌려보내고 연결을 끊는다. 
## api가 호출될 때마다 DB에 연결하고 끝나면 안전하게 닫아주는 역할을 한다
## 사유: 연결을 안닫으면 나중에 DB가 과부하 걸릴 수 있음. 


# 03. 데이터 검증 모델 (Pydantic)
class RecordCreate(BaseModel):
    amount: int
## 사용자가 데이터를 보낼 때 {"amount":250}처럼 정수형(int) amount를 꼭 포함해야한다는 규칙을 정함
## 만약 문자를 보내면 에러를 뱉는다. 

# 04. api 경로 설정
@app.get("/")
def root():
    return {"message:": "Water Log API 시작!"}
## 브라우저에서 주소를 치고 들어오면 잘 작동하고 있다고 인사하는 페이지


# 05. POST: 물마신 기록 저장
@app.post("/records")
def create_records(record: RecordCreate, db: Session = Depends(get_db)):
#api가 실행될 때 자동에서 위에서 만든 get_db를 실행해서, db변수에 연결정보를 넣어줌

    #1: DB에 넣을 객체 만들기 (사용자가 준 amount + 현재 시간)
    new_record = Record(amount=record.amount, drunk_at = datetime.now())
    
    #2. DB 일꾼에게 이거 추가하라고 함 (장바구니 담고)
    db.add(new_record)

    #3. (진짜로저장) (장바구니 결제~! 느낌)
    db.commit()

    #4. 방금 저장된 데이터(id 등)을 다시 불러와서 동기화
    db.refresh(new_record)

    #5. 저장된 결과를 사용자에게 보여줌
    return new_record



# 06. READ: 저장된 기록 조회하기
@app.get("/records")
def get_records(db: Session = Depends(get_db)):
    return db.query(Record).all()


# 07. UPDATE: 기록 수정
@app.put("/records/{record_id}")
def update_records(record_id: int, record: RecordCreate, db: Session = Depends(get_db)):
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if not db_record:
        return {"error": "기록을 찾을 수 없어요"}
    db_record.amount = record.amount
    db.commit()
    db.refresh(db_record)
    return db_record

# 08. DELETE: 기록 삭제
@app.delete("/records/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(Record).filter(Record.id == record_id).first()
    if not db_record:
        return {"error": "기록을 찾을 수 없어요"}
    db.delete(db_record)
    db.commit()
    return {"message": "삭제 완료"}