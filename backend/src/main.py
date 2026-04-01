from functools import wraps
from typing import List

from fastapi import FastAPI, HTTPException

from database import SessionDep
from schemas import TransactionCreate, TransactionResponse
from services import TransactionsService

app = FastAPI()


@app.get("/")
def hello() -> dict:
    return {"message": "Hello World!"}

@app.get("/hello/{name}")
def hello_name(name: str) -> dict:
    return {"message": f"Hello {name}!"}
    
@app.post("/transaction/", response_model=TransactionResponse)
async def post_transactions (
    data: TransactionCreate,
    user_id: int,
    session: SessionDep) -> TransactionResponse:
    
    service = TransactionsService(session)
    
    transaction = await service.create_transaction(
        data,
        user_id=user_id
    )
        
    response = TransactionResponse.model_validate(transaction)
        
    return response
    
@app.get("/transactions/")
async def get_transactions(
    user_ids: List[int],
    session: SessionDep) -> List[TransactionResponse]:
    
    service = TransactionsService(session)

    transactions = await service.get_transactions(
        user_ids=user_ids
    )

    return [
        TransactionResponse.model_validate(t)
        for t in transactions
    ]