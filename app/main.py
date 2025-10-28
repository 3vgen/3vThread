import uvicorn
from fastapi import FastAPI
from app.db.connection import engine
from app.db.base import Base
from app.user.routers import router as user_router


app = FastAPI(title="test")

app.include_router(user_router, prefix="/auth", tags=["API"])


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Слушать все интерфейсы (чтобы был доступен с других устройств)
        port=80,  # Указываем порт явно
        reload=True  # Автоперезагрузка при изменениях
    )