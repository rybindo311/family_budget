from functools import wraps
from typing import List

from fastapi import FastAPI, HTTPException

from database import SessionDep
from schemas import TransactionCreate, TransactionResponse
from services import TransactionsService

app = FastAPI()

def http_error_handler (func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
    return wrapper

@app.get("/")
def hello() -> dict:
    return {"message": "Hello World!"}

@app.get("/hello/{name}")
def hello_name(name: str) -> dict:
    return {"message": f"Hello {name}!"}
    
@http_error_handler
@app.post("/transaction/", response_model=TransactionResponse)
async def post_transaction (
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
    
@http_error_handler
@app.get("/transactions/")
async def get_transactions(
    user_id: int,

    session: SessionDep) -> List[TransactionResponse]:
    
    servise = TransactionsService(session)

    transactions = await servise.get_transactions(
        user_id
    )