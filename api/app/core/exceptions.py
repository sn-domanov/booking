# ─────────────────────────────────────────
# Base exceptions
# ─────────────────────────────────────────


class ApplicationError(Exception):
    code: str = "error"

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "detail": self.detail,
        }


# ─────────────────────────────────────────
# Application exceptions
# ─────────────────────────────────────────


class NotFoundError(ApplicationError):
    code = "not_found"
