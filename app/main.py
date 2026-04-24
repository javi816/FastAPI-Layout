from fastapi import FastAPI
from app.core.handlers.domain_exception import (
    domain_exception_handler
)
from app.core.auth.firebase_init import init_firebase
from app.core.exceptions.base import DomainException

from app.modules.auth.router import router as auth_router

app = FastAPI()

app.add_exception_handler(
    DomainException,
    domain_exception_handler
)

@app.on_event("startup")
async def startup_event():
    init_firebase()

app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)