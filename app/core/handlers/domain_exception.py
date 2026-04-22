import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions.base import DomainException

logger = logging.getLogger(__name__)

async def domain_exception_handler(
    request: Request,
    exc: DomainException
):
    logger.warning(
        f"DomainException | code={exc.code} "
        f"| message={exc.message} "
        f"| path={request.url.path}"
    )
    
    content = {
        "error": exc.code,
        "message": exc.message
    }
    
    if exc.details:
        content["details"]= exc.details
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )