"""Скрипт для заполнения БД тестовыми данными в dev-среде"""
import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.src.config import settings
from backend.src.models import BaseOrm, UsersOrm, FamiliesOrm, TransactionsOrm


async def seed_database():
    """Заполняет БД тестовыми данными"""
    
    environment = settings.ENVIRONMENT
    if environment not in ["dev", "local", "test"]:
        print(f"⚠️  Skipping seed data in {environment} mode")
        return
    
    print("🌱 Seeding test data...")
    

    DATABASE_URL = settings.DATABASE_URL
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(UsersOrm))
        existing_users = result.scalars().first()
        
        if existing_users:
            print("📊 Database already contains data, skipping seed")
            return
        
        try:
            # 1. Создаем семьи
            family1 = FamiliesOrm(
                name="Ивановы",
                admin_id=1,  # временно, будет обновлено после создания админа
                is_active=True
            )
            family2 = FamiliesOrm(
                name="Петровы",
                admin_id=2,
                is_active=True
            )
            
            session.add_all([family1, family2])
            await session.flush()
            
            # 2. Создаем пользователей
            users = [
                UsersOrm(
                    username="ivan",
                    family_id=family1.id
                ),
                UsersOrm(
                    username="anna",
                    family_id=family1.id
                ),
                UsersOrm(
                    username="petr",
                    family_id=family2.id
                ),
                UsersOrm(
                    username="maria",
                    family_id=family2.id
                ),
                UsersOrm(
                    username="guest",
                    family_id=None
                )
            ]
            
            session.add_all(users)
            await session.flush()
            
            # Обновляем admin_id для семей
            family1.admin_id = users[0].id  # Иван - админ семьи Ивановых
            family2.admin_id = users[2].id  # Петр - админ семьи Петровых
            
            # 3. Создаем транзакции для пользователей
            now = datetime.now(timezone.utc)
            categories = ["food", "transport", "entertainment", "utilities", "shopping"]
            
            transactions = []
            
            # Для Ивана
            for i in range(10):
                transactions.append(
                    TransactionsOrm(
                        user_id=users[0].id,
                        date=now - timedelta(days=i),
                        sum=100 + i * 50,
                        category=categories[i % len(categories)]
                    )
                )
            
            # Для Анны
            for i in range(8):
                transactions.append(
                    TransactionsOrm(
                        user_id=users[1].id,
                        date=now - timedelta(days=i),
                        sum=50 + i * 30,
                        category=categories[(i + 1) % len(categories)]
                    )
                )
            
            # Для Петра
            for i in range(12):
                transactions.append(
                    TransactionsOrm(
                        user_id=users[2].id,
                        date=now - timedelta(days=i),
                        sum=200 + i * 40,
                        category=categories[(i + 2) % len(categories)]
                    )
                )
            
            # Для Марии
            for i in range(6):
                transactions.append(
                    TransactionsOrm(
                        user_id=users[3].id,
                        date=now - timedelta(days=i),
                        sum=80 + i * 25,
                        category=categories[(i + 3) % len(categories)]
                    )
                )
            
            session.add_all(transactions)
            await session.commit()
            
            print(f"✅ Seeded successfully:")
            print(f"   - {len([family1, family2])} families")
            print(f"   - {len(users)} users")
            print(f"   - {len(transactions)} transactions")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Seeding failed: {str(e)}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    # Для запуска скрипта отдельно
    asyncio.run(seed_database())