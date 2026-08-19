from io import BytesIO
from pathlib import Path

TEST_IMAGE = Path(__file__).parents[1] / "assets" / "test_image.jpg"


def image_upload(
    path: Path = TEST_IMAGE,
    *,
    content_type: str = "image/jpeg",
) -> dict:
    return {
        "file": (
            path.name,
            BytesIO(path.read_bytes()),
            content_type,
        ),
    }
