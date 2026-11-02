"""Utilities for handling Telegram location information."""

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt


@dataclass(frozen=True, slots=True)
class TelegramLocationInfo:
    latitude: float
    longitude: float


def build_location_info(
    latitude: float,
    longitude: float,
) -> TelegramLocationInfo:
    """Build validated Telegram location information."""
    for name, value in (("latitude", latitude), ("longitude", longitude)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number.")

    if not -90 <= latitude <= 90:
        raise ValueError("latitude must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise ValueError("longitude must be between -180 and 180.")

    return TelegramLocationInfo(float(latitude), float(longitude))


def calculate_distance(
    first: TelegramLocationInfo,
    second: TelegramLocationInfo,
) -> float:
    """Calculate the distance between two locations in meters."""
    if not isinstance(first, TelegramLocationInfo):
        raise TypeError("first must be TelegramLocationInfo.")

    if not isinstance(second, TelegramLocationInfo):
        raise TypeError("second must be TelegramLocationInfo.")

    earth_radius = 6_371_000

    lat1 = radians(first.latitude)
    lat2 = radians(second.latitude)
    delta_lat = radians(second.latitude - first.latitude)
    delta_lon = radians(second.longitude - first.longitude)

    haversine = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    central_angle = 2 * asin(sqrt(min(1.0, haversine)))

    return earth_radius * central_angle
