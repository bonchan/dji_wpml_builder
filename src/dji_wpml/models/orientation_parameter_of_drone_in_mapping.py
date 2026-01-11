from dataclasses import dataclass, field

from dji_wpml.enums.general_enums import *

@dataclass
class ORientationParameterOfDroneInMapping:
    mappingHeadingMode: YawAngleModeOfDrone
    mappingHeadingAngle: int