import pytest

from app.core.slug import SLUG_MAX_LENGTH, make_slug


@pytest.mark.parametrize(
    ("name", "suffix", "expected"),
    [
        ("Quiet City Retreat", None, "quiet-city-retreat"),
        ("Quiet City Retreat", 1, "quiet-city-retreat-2"),
        ("Quiet City Retreat", 2, "quiet-city-retreat-3"),
        ("Český Krumlov", None, "cesky-krumlov"),
        ("São Paulo Apartment", None, "sao-paulo-apartment"),
    ],
)
def test_make_slug(
    name: str,
    suffix: int,
    expected: str,
) -> None:
    assert make_slug(name, suffix) == expected


def test_make_slug_respects_max_length() -> None:
    name = "Beautiful Apartment " * 10

    slug = make_slug(name, 0)

    assert len(slug) <= SLUG_MAX_LENGTH


def test_make_slug_reserves_space_for_suffix() -> None:
    name = "Beautiful Apartment " * 10

    slug = make_slug(name, 1)

    assert len(slug) <= SLUG_MAX_LENGTH
    assert slug.endswith("-2")
