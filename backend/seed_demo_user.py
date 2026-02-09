"""Add demo user for quick login. Run: python seed_demo_user.py"""
import asyncio
from app.database import init_db, AsyncSessionLocal
from app.models.user import User
from app.utils.auth import hash_password

async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        r = await db.execute(select(User).where(User.email == "demo@test.com"))
        if r.scalar_one_or_none():
            print("Demo user already exists!")
            return
        user = User(
            email="demo@test.com",
            hashed_password=hash_password("demo123"),
        )
        db.add(user)
        await db.commit()
        print("Demo user created: demo@test.com / demo123")

if __name__ == "__main__":
    asyncio.run(seed())
