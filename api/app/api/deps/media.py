from typing import Annotated

from fastapi import Depends

from app.api.deps.images import ImageProcessorDep
from app.api.deps.object_storage import ObjectStorageDep
from app.domains.media.service import MediaService


def get_media_service(
    storage: ObjectStorageDep,
    image_processor: ImageProcessorDep,
) -> MediaService:
    return MediaService(
        storage=storage,
        image_processor=image_processor,
    )


MediaServiceDep = Annotated[
    MediaService,
    Depends(get_media_service),
]
