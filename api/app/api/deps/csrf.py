from typing import Annotated

from fastapi import Depends, Request
from fastapi_csrf_protect import CsrfProtect

_UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


async def require_csrf(
    request: Request,
    csrf_protect: Annotated[CsrfProtect, Depends()],
) -> None:
    if request.method in _UNSAFE_METHODS:
        await csrf_protect.validate_csrf(request)


CsrfDep = Annotated[
    None,
    Depends(require_csrf),
]
