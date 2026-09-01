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


class ImageProcessingError(ApplicationError):
    code = "image_processing_error"


class StorageError(ApplicationError):
    code = "storage_error"


# ─────────────────────────────────────────
# Application exceptions
# ─────────────────────────────────────────


class ForbiddenError(ApplicationError):
    code = "forbidden"


class NotFoundError(ApplicationError):
    code = "not_found"


class ConflictError(ApplicationError):
    code = "conflict"

    def __init__(
        self,
        detail: str,
        *,
        conflict: str | None = None,
    ) -> None:
        self.conflict = conflict
        super().__init__(detail)

    def to_dict(self) -> dict[str, str]:
        body = super().to_dict()

        if self.conflict is not None:
            body["conflict"] = self.conflict

        return body


class ValidationError(ApplicationError):
    code = "validation_error"


class ImageTooLargeError(ImageProcessingError):
    code = "image_too_large"


class InvalidImageError(ImageProcessingError):
    code = "invalid_image"


class ImageDimensionError(ImageProcessingError):
    code = "image_dimensions_too_large"


class InvalidStorageKeyError(StorageError):
    code = "invalid_storage_key"


class InvalidCursorError(ApplicationError):
    code = "invalid_cursor"
