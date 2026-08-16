import math

import pytest

from validation import normalize_scale, parse_temperature, validate_temperature


@pytest.mark.parametrize(
    ("scale", "value"),
    [
        ("C", -273.15),
        ("F", -459.67),
        ("K", 0),
        ("RE", -218.52),
        ("R", 0),
        ("DE", 559.725),
        ("DE", -1000),
    ],
)
def test_boundary_and_valid_temperatures_are_accepted(scale, value):
    validate_temperature(value, scale)


@pytest.mark.parametrize(
    ("scale", "value"),
    [
        ("C", -273.16),
        ("F", -459.68),
        ("K", -0.01),
        ("RE", -218.53),
        ("R", -0.01),
        ("DE", 559.726),
        ("DE", 600),
    ],
)
def test_values_beyond_physical_limits_are_rejected(scale, value):
    with pytest.raises(ValueError):
        validate_temperature(value, scale)


def test_parse_temperature_with_dot():
    assert parse_temperature("36.6") == pytest.approx(36.6)


def test_parse_temperature_with_comma():
    assert parse_temperature("36,6") == pytest.approx(36.6)


@pytest.mark.parametrize("value", ["abc", "12..5", "--25", ""])
def test_invalid_numeric_input_is_rejected(value):
    with pytest.raises(ValueError, match="числовое"):
        parse_temperature(value)


@pytest.mark.parametrize("value", ["nan", "inf", "+inf", "-inf"])
def test_non_finite_values_are_rejected(value):
    with pytest.raises(ValueError, match="конечным"):
        parse_temperature(value)


def test_validate_temperature_rejects_non_finite_float():
    with pytest.raises(ValueError, match="конечным"):
        validate_temperature(math.inf, "C")


def test_unknown_scale_is_rejected():
    with pytest.raises(ValueError, match="Неизвестная"):
        normalize_scale("X")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("c", "C"),
        ("Re", "RE"),
        ("réaumur", "RE"),
        ("делиль", "DE"),
    ],
)
def test_scale_normalization(raw, expected):
    assert normalize_scale(raw) == expected
