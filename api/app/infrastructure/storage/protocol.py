from collections.abc import Sequence
from typing import Protocol


class ObjectStorage(Protocol):
    def get_url(
        self,
        *,
        storage_key: str,
    ) -> str: ...

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

    async def delete_many(
        self,
        *,
        storage_keys: Sequence[str],
    ) -> None: ...

    async def clear(
        self,
        *,
        prefix: str | None = None,
    ) -> None: ...
