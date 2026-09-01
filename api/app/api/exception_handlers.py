from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    ApplicationError,
    ConflictError,
    ForbiddenError,
    ImageDimensionError,
    ImageProcessingError,
    ImageTooLargeError,
    InvalidCursorError,
    InvalidImageError,
    InvalidStorageKeyError,
    NotFoundError,
    StorageError,
    ValidationError,
)

DEFAULT_STATUS_CODE_MAP = {
    ImageProcessingError: 400,
    InvalidCursorError: 400,
    InvalidStorageKeyError: 400,
    ForbiddenError: 403,
    NotFoundError: 404,
    ConflictError: 409,
    ImageTooLargeError: 413,
    ValidationError: 422,
    ImageDimensionError: 413,
    InvalidImageError: 422,
    ApplicationError: 500,
    StorageError: 500,
}


async def application_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    # `exc` should only be `StarletteHTTPException` at runtime
    # this is a workaround to avoid static typechecker issue with
    # add_exception_handler's `exc_class_or_status_code: int | type[Exception]`
    if not isinstance(exc, ApplicationError):
        raise TypeError("application_exception_handler received non-ApplicationError")

    # Most specific exception wins, else Internal Server Error
    for exc_type in type(exc).__mro__:
        if exc_type in DEFAULT_STATUS_CODE_MAP:
            status_code = DEFAULT_STATUS_CODE_MAP[exc_type]
            break
    else:
        status_code = 500

    response = JSONResponse(
        status_code=status_code,
        content=exc.to_dict(),
    )

    return response
