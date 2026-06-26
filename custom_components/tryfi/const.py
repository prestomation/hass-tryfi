"""Constants for the TryFi integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "tryfi"

# Configuration
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_POLLING_RATE: Final = "polling"
DEFAULT_POLLING_RATE: Final = 60

# Sensor constants
SENSOR_STATS_BY_TIME: Final = ["DAILY", "WEEKLY", "MONTHLY"]
SENSOR_STATS_BY_TYPE: Final = ["STEPS", "DISTANCE", "SLEEP", "NAP", "GOAL"]

# Device info
MANUFACTURER: Final = "TryFi"
# Generic fallback model, used when the collar generation can't be determined
# from the moduleId.
MODEL: Final = "Smart Dog Collar"

# Collar models, resolved from the moduleId prefix (see resolve_collar_model).
COLLAR_MODEL_SERIES_1: Final = "Series 1 Collar"
COLLAR_MODEL_SERIES_2: Final = "Series 2 Collar"
COLLAR_MODEL_MINI: Final = "Mini Collar"
COLLAR_MODEL_SERIES_3: Final = "Series 3 Collar"
