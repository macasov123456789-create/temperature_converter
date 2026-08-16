import pytest

from converter import convert_temperature


@pytest.mark.parametrize(
    ("value", "from_scale", "to_scale", "expected"),
    [
        (0, "C", "F", 32),
        (100, "C", "F", 212),
        (32, "F", "C", 0),
        (212, "F", "C", 100),
        (0, "C", "K", 273.15),
        (273.15, "K", "C", 0),
        (-273.15, "C", "K", 0),
        (0, "C", "RE", 0),
        (100, "C", "RE", 80),
        (-273.15, "C", "RE", -218.52),
        (0, "C", "R", 491.67),
        (-273.15, "C", "R", 0),
        (100, "C", "R", 671.67),
        (100, "C", "DE", 0),
        (0, "C", "DE", 150),
        (-273.15, "C", "DE", 559.725),
        (80, "RE", "C", 100),
        (491.67, "R", "C", 0),
        (150, "DE", "C", 0),
        (0, "DE", "C", 100),
        (559.725, "DE", "C", -273.15),
    ],
)
def test_known_conversions(value, from_scale, to_scale, expected):
    result = convert_temperature(value, from_scale, to_scale)
    assert result == pytest.approx(expected)


def test_conversion_between_two_non_celsius_scales():
    result = convert_temperature(80, "RE", "F")
    assert result == pytest.approx(212)


def test_rankine_to_kelvin():
    result = convert_temperature(491.67, "R", "K")
    assert result == pytest.approx(273.15)


def test_delisle_to_fahrenheit():
    result = convert_temperature(150, "DE", "F")
    assert result == pytest.approx(32)


def test_same_scale_is_rejected():
    with pytest.raises(ValueError, match="совпадают"):
        convert_temperature(10, "C", "C")
