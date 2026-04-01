from dataclasses import dataclass


@dataclass
class ServiceConfig:
    """Configuration for service endpoints"""
    game_data_endpoint: str
    commands_endpoint: str
    players_endpoint: str
    characters_endpoint: str
    rooms_endpoint: str
    areas_endpoint: str
    items_endpoint: str
    mobiles_endpoint: str
    skills_endpoint: str
    socials_endpoint: str
