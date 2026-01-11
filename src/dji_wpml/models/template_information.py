from dataclasses import dataclass, field

from dji_wpml.models.coordinate_parameter_info import CoordinateParameterInfo
from dji_wpml.models.payload_param import PayloadParam
from dji_wpml.enums.general_enums import *
from typing import List, Optional, Dict, Any


@dataclass
class TemplateInformation:

    template_type: TemplateType
    template_id: int
    auto_flight_speed: float
    wayline_coordinate_sys_param: CoordinateParameterInfo

    # Common
    payload_param: PayloadParam

    # gimbalPitchMode
    # globalWaypointHeadingParam
    # globalWaypointTurnMode
    # globalUseStraightLine

    # list of Waypoint Info
    waypoint_info: List[Dict[str, Any]] = field(default_factory=list) # WaypointInfo