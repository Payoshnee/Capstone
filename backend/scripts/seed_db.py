import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.models.booking import ExpertProfile, AvailabilitySlot
from app.models.user import User, Profile
from datetime import datetime, timedelta, timezone
import uuid

async def seed():
    print("Connecting to DB...")
    engine = create_async_engine(settings.DATABASE_URL)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Check if users already exist
        res = await session.execute(text("SELECT count(*) FROM expert_profiles"))
        count = res.scalar()
        if count > 0:
            print(f"Database already has {count} experts. Skipping seed to prevent duplicates.")
            return

        print("Seeding dummy experts...")
        experts_data = [
            {
                "id": str(uuid.uuid4()),
                "email": "ananya@example.com",
                "name": "Ananya Sharma",
                "company": "Google",
                "role": "Senior Software Engineer",
                "rating": 4.9,
                "image": "https://i.pravatar.cc/150?u=ananya"
            },
            {
                "id": str(uuid.uuid4()),
                "email": "rohan@example.com",
                "name": "Rohan Mehta",
                "company": "Amazon",
                "role": "SDE III",
                "rating": 4.8,
                "image": "https://i.pravatar.cc/150?u=rohan"
            },
            {
                "id": str(uuid.uuid4()),
                "email": "priya@example.com",
                "name": "Priya Patel",
                "company": "Microsoft",
                "role": "Principal Engineer",
                "rating": 5.0,
                "image": "https://i.pravatar.cc/150?u=priya"
            }
        ]

        for exp in experts_data:
            user = User(id=exp["id"], email=exp["email"], full_name=exp["name"], role="expert")
            profile = Profile(user_id=exp["id"], full_name=exp["name"], avatar_url=exp["image"])
            expert = ExpertProfile(
                id=exp["id"],
                user_id=exp["id"], 
                display_name=exp["name"],
                bio=f"{exp['role']} at {exp['company']}",
                company_title=exp["company"],
                company=exp["company"],
                avg_rating=exp["rating"],
                is_approved=True,
                approved=True
            )
            session.add_all([user, profile, expert])
            await session.flush()

            # Add some slots
            now = datetime.now(timezone.utc)
            for i in range(1, 4):
                slot_time = now + timedelta(days=i, hours=10)
                slot = AvailabilitySlot(
                    expert_id=exp["id"],
                    start_time=slot_time,
                    end_time=slot_time + timedelta(hours=1),
                    is_booked=False
                )
                session.add(slot)

        await session.commit()
        print("Successfully seeded the database!")

if __name__ == "__main__":
    asyncio.run(seed())
