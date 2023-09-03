import os

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PWD']}@db/fastapidb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class UserCreate(BaseModel):
    name: str
    age: int


@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.post("/users/")
def create_user(name: str = Form(...), age: int = Form(...)):
    db = SessionLocal()
    db_user = User(name=name, age=age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # POSTからGETにリダイレクトするにはステータスコードを設定
    return RedirectResponse('/', status_code=302)


@app.post("/users/delete/{id}")
def delete_user(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return RedirectResponse("/", status_code=303)
