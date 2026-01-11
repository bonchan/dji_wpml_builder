from dataclasses import dataclass, field

from dji_wpml.enums.general_enums import *

@dataclass
class CoordinateParameterInfo:
    coordinate_mode: LatitudeAndLongitudeCoordinateSystem = LatitudeAndLongitudeCoordinateSystem.WGS84
    height_mode: ReferencePlaneForWaypointElevation = None
    positioning_type: LatitudeAndLongitudeAndAltitudeDataSources = None
    global_shoot_height: float = None
    surface_follow_mode_enable: bool = None
    surface_relative_height: float = None
