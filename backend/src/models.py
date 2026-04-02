from typing import Annotated, List, Optional
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase, 
    mapped_column, 
    Mapped, 
    relationship
)

intpk = Annotated[int, mapped_column(primary_key=True)]
str_100 = Annotated[str, 100]
str_256 = Annotated[str, 256]


class BaseOrm(DeclarativeBase):
    type_annotation_map = {
        str_100: String(100),
    }


class TransactionsOrm(BaseOrm):
    __tablename__ = "transactions"

    transaction_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    amount: Mapped[int]
    category: Mapped[str_100]
    
    user: Mapped["UsersOrm"] = relationship(back_populates="transactions")
    

class UsersOrm(BaseOrm):
    __tablename__ = "users"
    
    user_id: Mapped[intpk]
    username: Mapped[str_100]
    family_id: Mapped[Optional[int]] = mapped_column(ForeignKey("families.id", ondelete="SET NULL"), nullable=True)
    
    family: Mapped[Optional["FamiliesOrm"]] = relationship(back_populates="users")
    transactions: Mapped[List["TransactionsOrm"]] = relationship(back_populates="user")

    
class FamiliesOrm(BaseOrm):
    __tablename__ = "families"
    
    family_id: Mapped[intpk]
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str_100]
    is_active: Mapped[bool]
    
    users: Mapped[List["UsersOrm"]] = relationship(back_populates="family")
    admin: Mapped["UsersOrm"] = relationship(foreign_keys=[admin_id])

