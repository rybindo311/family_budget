from typing import List, Optional

from fastapi import Depends, FastAPI, Query, HTTPException

from database import SessionDep
from schemas import TransactionCreate, TransactionResponse, TransictionFilters
from services import TransactionsService

app = FastAPI()


@app.get("/")
def hello() -> dict:
    return {"message": "Hello World!!!"}

@app.get("/hello/{name}")
def hello_name(name: str) -> dict:
    return {"message": f"Hello {name}!"}
    
@app.post("/transaction/", response_model=TransactionResponse)
async def post_transactions (
    session: SessionDep,
    data: TransactionCreate,
    user_id: int) -> TransactionResponse:
    
    service = TransactionsService(session)
    
    transaction = await service.create_transaction(
        data,
        user_id=user_id
    )
        
    return TransactionResponse.model_validate(transaction)
    
@app.get("/transactions/", response_model=List[TransactionResponse])
async def get_transactions(
    session: SessionDep,
    filters: TransictionFilters = Query()
    ) -> List[TransactionResponse]:
    
    service = TransactionsService(session)

    transactions = await service.get_transactions(
        **filters.model_dump(exclude_none=True)
    )

    return [
        TransactionResponse.model_validate(transaction)
        for transaction in transactions
    ]

