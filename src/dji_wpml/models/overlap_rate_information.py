from dataclasses import dataclass, field

from dji_wpml.enums.general_enums import *

@dataclass
class OverlapRateInformation:
    ortho_lidar_overlap_h: int
    ortho_lidar_overlap_w: int
    ortho_camera_overlap_h: int
    ortho_camera_overlap_w: int
    inclined_lidar_overlap_h: int
    inclined_lidar_overlap_w: int
    inclined_camera_overlap_h: int
    inclined_camera_overlap_w: int
    