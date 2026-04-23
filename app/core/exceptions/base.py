class DomainException(Exception):
    """Base class for domain errors"""

    def __init__(
            self,
            message: str,
            code: str = "domain_error",
            status_code: int = 400,
            details: dict | None = None
            ):

        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)
