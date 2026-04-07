"""
Скрипт для заполнения базы данных тестовыми данными
"""

import asyncio
import random
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

# Импорт моделей
from config import settings
from models import UsersOrm, FamiliesOrm, TransactionsOrm, BaseOrm




engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def seed_database():
    """Заполнение базы данных тестовыми данными"""
    
    async with async_session() as session:
        # Проверяем, есть ли уже данные
        result = await session.execute(select(UsersOrm).limit(1))
        if result.first():
            print("База данных уже содержит данные. Скрипт не будет выполнен.")
            return
        
        print("Начинаем заполнение базы данных...")

        # 1. Создаём пользователей
        users_data = [
            {"username": "Иванова Мария", "family_id": None},
            {"username": "Иванов Алексей", "family_id": None},
            {"username": "Петров Иван", "family_id": None},
            {"username": "Петрова Дарья", "family_id": None},
            {"username": "Петров Алексей", "family_id": None},
            {"username": "Сидоров Виталий", "family_id": None},
            {"username": "Шишкина Инна", "family_id": None},
        ]
        
        users = []
        for user_data in users_data:
            user = UsersOrm(**user_data)
            session.add(user)
            users.append(user)
        
        await session.flush()
        print(f"✓ Создано {len(users)} пользователей")
        
        # 2. Создаём семьи
        families_data = [
            {"name": "Ивановы", "is_active": True, "admin_id": users[0].user_id},
            {"name": "Петровы", "is_active": True, "admin_id": users[2].user_id},
            {"name": "Сидоровы", "is_active": True, "admin_id": users[4].user_id},
        ]
        
        families = []
        for family_data in families_data:
            family = FamiliesOrm(**family_data)
            session.add(family)
            families.append(family)
        
        await session.flush()  # Чтобы получить family_id
        print(f"✓ Создано {len(families)} семей")
        
        # 3. Добавляем пользователей в семьи
        users[0].family_id = families[0].family_id
        users[1].family_id = families[0].family_id
        users[2].family_id = families[1].family_id
        users[3].family_id = families[1].family_id
        users[4].family_id = families[1].family_id
        users[5].family_id = families[2].family_id
        
        # 4. Создаём транзакции
        categories = ["Еда", "Транспорт", "Развлечения", "Здоровье", "Образование", "Коммуналка"]
        
        transactions = []
        start_date = datetime.now() - timedelta(days=30)
        
        for user in users:
            if user.user_id is None:
                continue
                
            # Для каждого пользователя создаём от 3 до 10 транзакций
            num_transactions = random.randint(3, 10)
            
            for _ in range(num_transactions):
                random_days = random.randint(0, 30)
                random_date = start_date + timedelta(days=random_days)
                
                transaction = TransactionsOrm(
                    user_id=user.user_id,
                    date=random_date,
                    amount=random.randint(100, 10000),
                    category=random.choice(categories)
                )
                session.add(transaction)
                transactions.append(transaction)
        
        await session.commit()
        print(f"✓ Создано {len(transactions)} транзакций")
        
        # Выводим статистику
        print("\n" + "="*50)
        print("СТАТИСТИКА ЗАПОЛНЕНИЯ:")
        print("="*50)
        print(f"Семьи: {len(families)}")
        print(f"Пользователи: {len(users)}")
        print(f"Транзакции: {len(transactions)}")
        
        # Детализация по семьям
        print("\nДетализация по семьям:")
        for family in families:
            family_users = [u for u in users if u.family_id == family.family_id]
            family_transactions = 0
            for user in family_users:
                family_transactions += sum(1 for t in transactions if t.user_id == user.user_id)
            
            print(f"  {family.name}:")
            print(f"    - Пользователей: {len(family_users)}")
            print(f"    - Транзакций: {family_transactions}")
            print(f"    - Администратор: {next(u.username for u in users if u.user_id == family.admin_id)}")


async def main():
    try:
        await seed_database()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())