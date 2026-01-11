from dataclasses import dataclass, field
from typing import List
from dji_wpml.enums.general_enums import ExecuteHeightMode
from dji_wpml.models.waypoint_info import WaypointInfo
from typing import List, Optional, Dict, Any

@dataclass
class WaylinesInformation:

    template_id: int
    wayline_id: int 
    auto_flight_speed: float
    execute_height_mode: ExecuteHeightMode

    waypoint_info: List[Dict[str, Any]] = field(default_factory=list) # WaypointInfo

