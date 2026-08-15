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


# ─────────────────────────────────────────
# Application exceptions
# ─────────────────────────────────────────


class NotFoundError(ApplicationError):
    code = "not_found"


class ValidationError(ApplicationError):
    code = "validation_error"


class ImageTooLargeError(ImageProcessingError):
    code = "image_too_large"


class InvalidImageError(ImageProcessingError):
    code = "invalid_image"


class ImageDimensionError(ImageProcessingError):
    code = "image_dimensions_too_large"
