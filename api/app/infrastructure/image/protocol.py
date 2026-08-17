from typing import Protocol

from app.infrastructure.image.types import ImageSpec, ProcessedImage


class ImageProcessor(Protocol):
    def process(
        self,
        content: bytes,
        spec: ImageSpec,
    ) -> ProcessedImage: ...
