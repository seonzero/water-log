from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message:": "Water Log API 시작!"}