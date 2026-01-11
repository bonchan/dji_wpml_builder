# src/dji_wpml/models/mission.py
from dataclasses import dataclass, field
from typing import List
from dji_wpml.models.mission_config import MissionConfig
from dji_wpml.models.template_information import TemplateInformation
from dji_wpml.models.waylines_information import WaylinesInformation

@dataclass
class MissionInformation:
    # Template.kml
    author: str
    create_time: int
    update_time: int

    # Common
    mission_config: MissionConfig

    # Template.kml
    template_information: TemplateInformation

    # Waylines.wpml
    waylines_information: WaylinesInformation

    