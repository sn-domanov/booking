from uuid import UUID

from app.domains.media.types import MediaObject
from app.infrastructure.image.protocol import ImageProcessor
from app.infrastructure.image.types import ImageSpec
from app.infrastructure.storage.protocol import ObjectStorage


class MediaService:
    def __init__(
        self,
        storage: ObjectStorage,
        image_processor: ImageProcessor,
    ) -> None:
        self.storage = storage
        self.image_processor = image_processor

    def get_url(self, *, storage_key: str) -> str:
        return self.storage.get_url(storage_key=storage_key)

    async def add_image(
        self,
        *,
        content: bytes,
        storage_prefix: str,
        media_id: UUID,
        spec: ImageSpec,
    ) -> MediaObject:
        processed = self.image_processor.process(content, spec)

        storage_key = f"{storage_prefix}/{media_id}.{spec.format.lower()}"

        await self.storage.put(
            storage_key=storage_key,
            content=processed.content,
            content_type=processed.content_type,
        )

        return MediaObject(
            id=media_id,
            storage_key=storage_key,
            url=self.storage.get_url(storage_key=storage_key),
            content_type=processed.content_type,
        )

    async def replace_image(
        self,
        *,
        content: bytes,
        storage_key: str,
        media_id: UUID,
        spec: ImageSpec,
    ) -> MediaObject:
        processed = self.image_processor.process(content, spec)

        await self.storage.put(
            storage_key=storage_key,
            content=processed.content,
            content_type=processed.content_type,
        )

        return MediaObject(
            id=media_id,
            storage_key=storage_key,
            url=self.storage.get_url(storage_key=storage_key),
            content_type=processed.content_type,
        )

    async def delete_image(self, *, storage_key: str) -> None:
        await self.storage.delete(storage_key=storage_key)
