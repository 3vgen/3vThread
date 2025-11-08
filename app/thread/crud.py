from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.thread.model import Thread


async def create_thread(db: AsyncSession, name: str, email: str) -> Thread:
    thread = Thread(name=name, email=email)
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread


async def get_thread(db: AsyncSession, thread_id: int) -> Thread:
    result = await db.execute(select(Thread).filter(Thread.id == thread_id))
    return result.scalars().first()


async def delete_thread(db: AsyncSession, thread: Thread):
    await db.delete(thread)
    await db.commit()
