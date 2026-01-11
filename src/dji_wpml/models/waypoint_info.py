from dataclasses import dataclass, field

from dji_wpml.models.coordinate_parameter_info import CoordinateParameterInfo
from dji_wpml.models.actions import ActionGroup
from dji_wpml.enums.general_enums import *

@dataclass
class WaypointInfo:
    is_risky: bool
    longitude: float
    latitude: float
    index: int
    use_global_height: bool
    ellipsoid_height: float
    height: float
    use_global_speed: bool
    waypoint_speed: float
    use_global_heading_param: bool
    waypoint_heading_param: float
    use_global_turn_param: bool
    waypoint_turn_param: float
    use_straight_line: bool
    gimbal_pitch_angle: float
    quick_ortho_mapping_enable: bool
    quick_ortho_mapping_pitch: float

    action_group: ActionGroup