from enum import Enum
from collections import namedtuple

class WaypointType(Enum):
    WAYPOINT = "waypoint"

class ExecuteAction(Enum):
    GO_HOME = "goHome"
    LANDING = "landing"
    NO_ACTION = "noAction"

class AltitudeMode(Enum):
    EGM96 = "egm96"
    RELATIVE_TO_TAKEOFF = "relativeToTakeoff"

class ActionType(Enum):
    TAKE_PHOTO = "takePhoto"
    START_RECORD = "startRecord"
    STOP_RECORD = "stopRecord"
    GIMBAL_PITCH = "gimbalPitch"
    AIRCRAFT_YAW = "aircraftYaw"


DroneInfo = namedtuple("DroneInfo", ["drone_enum_value", "drone_sub_enum_value", "payload_enum_value"])

x=1000

class DroneModel(Enum):
    # Enterprise Matrice Series
    MATRICE_400 = DroneInfo(103, 0, x)
    MATRICE_350_RTK = DroneInfo(89, 0, x)
    MATRICE_300_RTK = DroneInfo(60, 0, x)
    MATRICE_300 = DroneInfo(67, 0, x)
    MATRICE_30T = DroneInfo(67, 1, x)
    
    # Mavic 3 / Matrice 4 Enterprise (M3E/M3T)
    MAVIC_3E = DroneInfo(77, 0, x)
    MAVIC_3T = DroneInfo(77, 1, x)
    MAVIC_3TA = DroneInfo(77, 3, x)
    
    # Dock Series (Matrice 3D/4D)
    MATRICE_3D = DroneInfo(91, 0, x)
    MATRICE_3TD = DroneInfo(91, 1, 81)
    MATRICE_4D = DroneInfo(100, 0, x)
    MATRICE_4TD = DroneInfo(100, 1, 99)
    
    # New Matrice 4 Series
    MATRICE_4E = DroneInfo(99, 0, x)
    MATRICE_4T = DroneInfo(99, 1, x)