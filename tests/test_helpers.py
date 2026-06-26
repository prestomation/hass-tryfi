"""Test TryFi helper utilities."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from custom_components.tryfi.const import DOMAIN
from custom_components.tryfi.helpers import collar_device_info, resolve_collar_model


@pytest.mark.parametrize(
    ("module_id", "expected"),
    [
        ("FC1ABC123", "Series 1 Collar"),
        ("FC2ABC123", "Series 2 Collar"),
        ("M1ABC123", "Mini Collar"),
        ("FC3ABC123", "Series 3 Collar"),
        ("SOMETHINGELSE", "Series 3 Collar"),
        (None, "Smart Dog Collar"),
        ("", "Smart Dog Collar"),
    ],
)
def test_resolve_collar_model(module_id, expected) -> None:
    """The collar model is derived from the moduleId prefix."""
    assert resolve_collar_model(module_id) == expected


def test_collar_device_info_full() -> None:
    """A pet with a collar gets model, serial number and firmware version."""
    pet = Mock()
    pet.petId = "pet-1"
    pet.name = "Rex"
    pet.breed = "Australian Cattle Dog"
    pet.device = Mock()
    pet.device.moduleId = "FC2XYZ"
    pet.device.buildId = "4.16.61"

    info = collar_device_info(pet)

    assert info["identifiers"] == {(DOMAIN, "pet-1")}
    assert info["name"] == "Rex"
    assert info["manufacturer"] == "TryFi"
    assert info["model"] == "Series 2 Collar"
    assert info["serial_number"] == "FC2XYZ"
    assert info["sw_version"] == "4.16.61"
    # Breed must never leak into the model.
    assert "Australian Cattle Dog" not in info["model"]


def test_collar_device_info_no_device() -> None:
    """A pet without a collar falls back to the generic model."""
    pet = Mock()
    pet.petId = "pet-2"
    pet.name = "Spot"
    pet.device = None

    info = collar_device_info(pet)

    assert info["model"] == "Smart Dog Collar"
    assert "serial_number" not in info
    assert "sw_version" not in info


def test_collar_device_info_missing_module_id() -> None:
    """A collar without a moduleId still resolves to the generic model."""
    pet = Mock()
    pet.petId = "pet-3"
    pet.name = "Buddy"
    pet.device = Mock()
    pet.device.moduleId = None
    pet.device.buildId = None

    info = collar_device_info(pet)

    assert info["model"] == "Smart Dog Collar"
    assert "serial_number" not in info
    assert "sw_version" not in info
