import math

import pytest

from harilebs_core.telegram_locations import (
    TelegramLocationInfo,
    build_location_info,
    calculate_distance,
)


def test_build_location_info():
    assert build_location_info(26.9124, 75.7873) == (
        TelegramLocationInfo(26.9124, 75.7873)
    )


def test_integer_coordinates():
    location = build_location_info(26, 75)
    assert location.latitude == 26.0
    assert location.longitude == 75.0


@pytest.mark.parametrize("latitude", [-90, 90, 0])
def test_valid_latitudes(latitude):
    assert build_location_info(latitude, 0).latitude == latitude


@pytest.mark.parametrize("longitude", [-180, 180, 0])
def test_valid_longitudes(longitude):
    assert build_location_info(0, longitude).longitude == longitude


@pytest.mark.parametrize("latitude", [-90.1, 90.1])
def test_invalid_latitude_range(latitude):
    with pytest.raises(ValueError):
        build_location_info(latitude, 0)


@pytest.mark.parametrize("longitude", [-180.1, 180.1])
def test_invalid_longitude_range(longitude):
    with pytest.raises(ValueError):
        build_location_info(0, longitude)


@pytest.mark.parametrize("value", [True, False, "26", None])
def test_latitude_type(value):
    with pytest.raises(TypeError):
        build_location_info(value, 0)


@pytest.mark.parametrize("value", [True, "75", None])
def test_longitude_type(value):
    with pytest.raises(TypeError):
        build_location_info(0, value)


def test_same_location_distance():
    location = build_location_info(26.9, 75.8)
    assert calculate_distance(location, location) == 0


def test_distance_symmetry():
    first = build_location_info(26.9, 75.8)
    second = build_location_info(28.6, 77.2)
    assert calculate_distance(first, second) == pytest.approx(
        calculate_distance(second, first)
    )


def test_distance_between_known_points():
    jaipur = build_location_info(26.9124, 75.7873)
    delhi = build_location_info(28.6139, 77.2090)
    distance = calculate_distance(jaipur, delhi)
    assert 250_000 < distance < 300_000


def test_distance_is_in_meters():
    first = build_location_info(0, 0)
    second = build_location_info(0, 1)
    assert calculate_distance(first, second) == pytest.approx(
        111_194.9, rel=0.001
    )


def test_antipodal_distance():
    first = build_location_info(0, 0)
    second = build_location_info(0, 180)
    assert calculate_distance(first, second) == pytest.approx(
        math.pi * 6_371_000
    )


def test_invalid_first_location():
    with pytest.raises(TypeError):
        calculate_distance("location", build_location_info(0, 0))


def test_invalid_second_location():
    with pytest.raises(TypeError):
        calculate_distance(build_location_info(0, 0), "location")


def test_equator_distance():
    first = build_location_info(0, 0)
    second = build_location_info(0, 0.5)
    assert 55_000 < calculate_distance(first, second) < 56_000


def test_pole_coordinates():
    location = build_location_info(90, 180)
    assert location.latitude == 90.0
    assert location.longitude == 180.0
