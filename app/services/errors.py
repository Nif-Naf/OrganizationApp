from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class UnexpectedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problem on the server. See logs.",
        )


class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized request. Denied.",
        )


class CompanyNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
