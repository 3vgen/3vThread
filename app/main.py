import uvicorn
from fastapi import FastAPI
from app.db.connection import engine
from app.db.base import Base
from app.user.routers import router as user_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Сюда потом добавлю подключение redis, и мб очередь сообщений
    print("Приложение запускается.")
    yield
    # Shutdown
    await engine.dispose()
    print("Приложение остановлено, соединение с БД закрыто.")


app = FastAPI(title="test", lifespan=lifespan)
app.include_router(user_router, prefix="/auth", tags=["API"])


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Слушать все интерфейсы (чтобы был доступен с других устройств)
        port=80,  # Указываем порт явно
        reload=True  # Автоперезагрузка при изменениях
    )