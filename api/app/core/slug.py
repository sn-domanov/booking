from slugify import slugify

SLUG_MAX_LENGTH = 80


def make_slug(name: str, suffix: int | None = None) -> str:
    # Suffix starts with "-2" for the first duplicate
    suffix_text = "" if suffix is None else f"-{suffix + 1}"

    base_max_length = SLUG_MAX_LENGTH - len(suffix_text)

    base_slug = slugify(
        name,
        max_length=base_max_length,
        word_boundary=True,
    )

    return base_slug + suffix_text
