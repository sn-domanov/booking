from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

from app.core.config import Settings
from app.core.exceptions import (
    ImageDimensionError,
    ImageTooLargeError,
    InvalidImageError,
)
from app.infrastructure.image.types import ImageSpec, ProcessedImage


class PillowImageProcessor:
    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self.settings = settings
        Image.MAX_IMAGE_PIXELS = self.settings.max_image_pixels

    def process(
        self,
        content: bytes,
        spec: ImageSpec,
    ) -> ProcessedImage:
        self._validate_size(content)
        image = self._open(content)

        try:
            self._validate_dimensions(image)
            image = self._normalize(image, spec)

            return self._encode(image, spec)
        finally:
            image.close()

    def _validate_size(self, content: bytes) -> None:
        if len(content) > self.settings.max_upload_size_bytes:
            raise ImageTooLargeError("Image file is too large")

    def _open(self, content: bytes) -> Image.Image:
        try:
            image = Image.open(BytesIO(content))

            # Validate structure
            image.verify()
        except (UnidentifiedImageError, OSError) as exc:
            raise InvalidImageError("Invalid image file") from exc

        # verify() invalidates the image, so reopen it.
        try:
            return Image.open(BytesIO(content))
        except (UnidentifiedImageError, OSError) as exc:
            raise InvalidImageError("Invalid image file") from exc

    def _validate_dimensions(self, image: Image.Image) -> None:
        if (
            image.width > self.settings.max_image_dimension
            or image.height > self.settings.max_image_dimension
        ):
            raise ImageDimensionError("Image dimensions are too large")

    def _normalize(
        self,
        image: Image.Image,
        spec: ImageSpec,
    ) -> Image.Image:
        image = ImageOps.exif_transpose(image)

        image = ImageOps.fit(
            image,
            (spec.width, spec.height),
            method=Image.Resampling.LANCZOS,
        )

        if spec.format == "JPEG":
            return self._flatten_alpha(image)

        return image.convert("RGB")

    def _flatten_alpha(self, image: Image.Image) -> Image.Image:
        image = image.convert("RGBA")

        background = Image.new(
            "RGB",
            image.size,
            (255, 255, 255),
        )
        background.paste(
            image,
            mask=image.getchannel("A"),
        )

        return background

    def _encode(
        self,
        image: Image.Image,
        spec: ImageSpec,
    ) -> ProcessedImage:
        output = BytesIO()

        image.save(
            output,
            format=spec.format,
            quality=spec.quality,
            optimize=True,
        )

        return ProcessedImage(
            content=output.getvalue(),
            content_type=self._content_type(spec.format),
        )

    @staticmethod
    def _content_type(image_format: str) -> str:
        return {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "WEBP": "image/webp",
            "AVIF": "image/avif",
        }[image_format]
