from fastapi import FastAPI
from app.core.handlers.domain_exception import (
    domain_exception_handler
)
from app.core.exceptions.base import DomainException

app = FastAPI()

app.add_exception_handler(
    DomainException,
    domain_exception_handler
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)