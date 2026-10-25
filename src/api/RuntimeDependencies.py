from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeDependencies:
    """Bootstrap-owned collaborators shared by the compatibility API facades."""

    registry_service: object = None
    weather_handler: object = None
