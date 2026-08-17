from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ImageSpec:
    width: int
    height: int
    format: str = "WEBP"
    quality: int = 85


@dataclass(frozen=True, slots=True)
class ProcessedImage:
    content: bytes
    content_type: str
