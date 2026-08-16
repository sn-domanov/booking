from typing import Protocol


class ObjectStorage(Protocol):
    async def put(
        self,
        *,
        storage_key: str,
        content: bytes,
        content_type: str,
    ) -> None: ...

    async def delete(
        self,
        *,
        storage_key: str,
    ) -> None: ...

    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str: ...
