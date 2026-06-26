"""Helper utilities for the TryFi integration."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    COLLAR_MODEL_MINI,
    COLLAR_MODEL_SERIES_1,
    COLLAR_MODEL_SERIES_2,
    COLLAR_MODEL_SERIES_3,
    DOMAIN,
    MANUFACTURER,
    MODEL,
)


def resolve_collar_model(module_id: str | None) -> str:
    """Map a collar's moduleId prefix to a human-friendly model name.

    The prefixes mirror the hardware generations the API exposes (see
    FiDevice.supportsAdvancedBehaviorStats). An unknown but present moduleId is
    treated as the current generation (Series 3); a missing moduleId falls back
    to the generic model.
    """
    if not module_id:
        return MODEL
    if module_id.startswith("FC1"):
        return COLLAR_MODEL_SERIES_1
    if module_id.startswith("FC2"):
        return COLLAR_MODEL_SERIES_2
    if module_id.startswith("M1"):
        return COLLAR_MODEL_MINI
    return COLLAR_MODEL_SERIES_3


def collar_device_info(pet: Any) -> DeviceInfo:
    """Build consistent device registry info for a pet's collar.

    Every collar entity must use this so the device's model, serial number and
    firmware version stay consistent regardless of which entity registers the
    device first.
    """
    device = getattr(pet, "device", None)
    module_id = getattr(device, "moduleId", None) if device else None

    info = DeviceInfo(
        identifiers={(DOMAIN, pet.petId)},
        name=pet.name,
        manufacturer=MANUFACTURER,
        model=resolve_collar_model(module_id),
    )

    # The moduleId is the collar's hardware identifier and the API's canonical
    # handle for the physical device, so expose it as the serial number.
    if module_id:
        info["serial_number"] = module_id

    build_id = getattr(device, "buildId", None) if device else None
    if build_id is not None:
        info["sw_version"] = build_id

    return info
