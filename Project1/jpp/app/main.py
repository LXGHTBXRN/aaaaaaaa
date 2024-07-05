from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from databases import Database
from parsers import parse_job_offers, parse_resumes
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:3xc1s10N(*@localhost:5432/postgres"

# Создаем движок для SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем базу данных для FastAPI
database = Database(DATABASE_URL)

# Создаем базовый класс для объявления моделей
Base = declarative_base()

# Определяем модели данных
class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    additional = Column(ARRAY(String))
    salary = Column(String)
    link = Column(String)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    position = Column(String)
    additional = Column(Text)
    skills = Column(ARRAY(String))
    link = Column(String)

# Создаем экземпляр приложения FastAPI и шаблонов Jinja2
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Функция для создания таблиц в базе данных
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Устанавливаем соединение с базой данных при запуске приложения
@app.on_event("startup")
async def startup():
    await database.connect()
    await create_tables()

# Закрываем соединение с базой данных при остановке приложения
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Определяем маршруты и обработчики запросов
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/job_offers")
async def job_offers(request: Request, query: str = None):
    try:
        job_list = []
        if query:
            job_list = parse_job_offers(query)
            async with database.transaction():
                async with engine.begin() as conn:
                    for job in job_list:
                        await conn.execute(JobOffer.__table__.insert().values(
                            title=job['title'],
                            company=job['company'],
                            additional=job['additional'],
                            salary=job['salary'],
                            link=job['link']
                        ))
        else:
            async with engine.begin() as conn:
                stmt = select(JobOffer)
                result = await conn.execute(stmt)
                job_list = result.fetchall()
        return templates.TemplateResponse("job_offers.html", {"request": request, "job_offers": job_list, "query": query})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resumes")
async def resumes(request: Request):
    try:
        default_query = "python developer"
        resumes_list = parse_resumes(default_query)
        async with database.transaction():
            async with engine.begin() as conn:
                for resume in resumes_list:
                    await conn.execute(Resume.__table__.insert().values(
                        title=resume['title'],
                        position=resume['position'],
                        additional=resume['additional'],
                        skills=resume['skills'],
                        link=resume['link']
                    ))
        return templates.TemplateResponse("resumes.html", {"request": request, "resumes": resumes_list, "query": default_query})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
