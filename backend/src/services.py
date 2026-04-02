from datetime import datetime
from typing import List

from sqlalchemy import between, func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models import TransactionsOrm, UsersOrm
from schemas import TransactionCreate


class TransactionsService:
    
    def __init__(self, session: AsyncSession):
        self.db = session
        
    async def create_transaction(
                self,
                transaction_data: TransactionCreate,
                user_id: int
    ) -> TransactionsOrm:
        """Создание новой транзакции"""
    
        try:
            new_transaction = TransactionsOrm(
                **transaction_data.model_dump(),
                user_id = user_id
            )
            
            self.db.add(new_transaction)
            await self.db.commit()
            await self.db.refresh(new_transaction)
            
            return new_transaction
        
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка при создании транзакции: {str(e)}")
            
    async def get_transactions(
                self,
                transaction_id: int | None = None,
                user_ids: List[int] | None = None,
                categories: List[str] | None = None,
                from_date: datetime | None = None,
                to_date: datetime | None = None,
                min_sum: int | None = None
    ) -> List[TransactionsOrm]:
        """Поиск транзакций по фильтрам"""
        
        query = select(TransactionsOrm)
            
        conditions = []
            
        if transaction_id is not None:
            conditions.append(TransactionsOrm.transaction_id == transaction_id)
                
        if user_ids is not None:
            conditions.append(TransactionsOrm.user_id.in_(user_ids))

        if from_date is not None and to_date is not None:
            conditions.append(
                between(
                    TransactionsOrm.date, 
                    from_date, 
                    to_date
                )
            )
        else:
            if from_date is not None:
                conditions.append(TransactionsOrm.date >= from_date)
            if to_date is not None:
                conditions.append(TransactionsOrm.date <= to_date)
                
        if categories is not None:
            conditions.append(TransactionsOrm.category.in_(categories))
                
        if min_sum is not None:
            conditions.append(TransactionsOrm.amount >= min_sum)
                        
        if conditions:
            query = query.where(and_(*conditions))
            
        result = await self.db.execute(query)
            
        return result.scalars().all()


class AnalyticService:

    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_statistics (
            self,
            user_id: int,
            categories: List[str] | None = None,
            from_date: datetime | None = None,
            to_date: datetime | None = None
    ) -> dict:
        
        
        query = select(
            UsersOrm.username,
            TransactionsOrm.category,
            func.count(TransactionsOrm),
            func.sum(TransactionsOrm.sum)
        ).join(
            TransactionsOrm, UsersOrm.user_id == TransactionsOrm.user_id
        ).group_by(
            UsersOrm.user_id,
            UsersOrm.username,
            TransactionsOrm.category
        )

        conditions = []

        conditions.append(UsersOrm.user_id == user_id)

        if from_date is not None and to_date is not None:
            conditions.append(
                between(
                    TransactionsOrm.date, 
                    from_date, 
                    to_date
                )
            )
        else:
            if from_date is not None:
                conditions.append(TransactionsOrm.date >= from_date)
            if to_date is not None:
                conditions.append(TransactionsOrm.date <= to_date) 

        if categories is not None:
            conditions.append(TransactionsOrm.category.in_(categories))

        query = query.where(*conditions)

        result = await self.db.execute(query)
 
        return result.all()



        
