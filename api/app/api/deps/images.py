from typing import Annotated

from fastapi import Depends

from app.api.deps.settings import SettingsDep
from app.infrastructure.image.pillow import PillowImageProcessor
from app.infrastructure.image.protocol import ImageProcessor


def get_image_processor(settings: SettingsDep) -> ImageProcessor:
    return PillowImageProcessor(
        settings=settings,
    )


ImageProcessorDep = Annotated[
    ImageProcessor,
    Depends(get_image_processor),
]
