from enum import Enum


class FlyToWaylineMode(Enum):
    SAFELY = "safely"
    POINT_TO_POINT = "pointToPoint"

class FinishAction(Enum):
    GO_HOME = "goHome"
    NO_ACTION = "noAction"
    AUTO_LAND = "autoLand"
    GOTO_FIRST_WAYPOINT = "gotoFirstWaypoint"

class ExitOnRCLost(Enum):
    GO_CONTINUE = "goContinue"
    EXECUTE_LOST_ACTION = "executeLostAction"

class ExecuteRCLostAction(Enum):
    GO_BACK = "goBack"
    LANDING = "landing"
    HOVER = "hover"

class TemplateType(Enum):
    WAYPOINT = "waypoint"
    MAPPING2D = "mapping2d"
    MAPPING3D = "mapping3d"
    MAPPING_STRIP = "mappingStrip"

class GlobalWaypointTurnMode(Enum):
    COORDINATE_TURN = "coordinateTurn"
    TO_POINT_AND_STOP_WITH_DISCONTINUITY_CURVATURE = "toPointAndStopWithDiscontinuityCurvature"
    TO_POINT_AND_STOP_WITH_CONTINUITY_CURVATURE = "toPointAndStopWithContinuityCurvature"
    TO_POINT_AND_PASS_WITH_CONTINUITY_CURVATURE = "toPointAndPassWithContinuityCurvature"

class GimbalPitchMode(Enum):
    MANUAL = "manual"
    USE_POINT_SETTING = "usePointSetting"

class ShootType(Enum):
    TIME = "time"
    DISTANCE = "distance"

class ExecuteHeightMode(Enum):
    WGS84 = "WGS84"
    RELATIVE_TO_START_POINT = "relativeToStartPoint"

class ImageFormat(Enum):
    WIDE = "wide"
    ZOOM = "zoom"
    IR = "ir"
    NARROW_BAND = "narrow_band"
    VISIBLE = "visable"

class ScanningMode(Enum):
    REPETITIVE = "repetitive"
    NON_REPETITIVE = "nonRepetitive"

class SamplingRate(Enum):
    _60000 = 60000
    _80000 = 80000
    _120000 = 120000
    _160000 = 160000
    _180000 = 180000
    _240000 = 240000

class LiDARReturnMode(Enum):
    SINGLE_RETURN_STRONGEST = "singleReturnStrongest"
    DUAL_RETURN = "dualReturn"
    TRIPLE_RETURN = "tripleReturn"

class PayloadMeteringMode(Enum):
    AVERAGE = "average"
    SPOT = "spot"

class PayloadFocusMode(Enum):
    FIRST_POINT = "firstPoint"
    CUSTOM = "custom"

class LatitudeAndLongitudeCoordinateSystem(Enum):
    WGS84 = "WGS84"

class ReferencePlaneForWaypointElevation(Enum):
    EGM96 = "EGM96"
    RELATIVE_TO_START_POINT = "relativeToStartPoint"
    ABOVE_GROUND_LEVEL = "aboveGroundLevel"
    REAL_TIME_FOLLOW_SURFACE = "realTimeFollowSurface"

class LatitudeAndLongitudeAndAltitudeDataSources(Enum):
    GPS = "GPS"
    RTK_BASE_STATION = "RTKBaseStation"
    QIAN_XUN = "QianXun"
    CUSTOM = "Custom"

class YawAngleModeOfDrone(Enum):
    FIXED = "fixed"
    FOLLOWWAYLINE = "followWayline"

class ActionGroupMode(Enum):
    SEQUENCE = "sequence"

class TriggerType(Enum):
    REACH_POINT = "reachPoint"
    BETWEEN_ADJACENT_POINTS = "betweenAdjacentPoints"
    MULTIPLE_TIMING = "multipleTiming"
    MULTIPLE_DISTANCE = "multipleDistance"

class ActionActuatorFunc(Enum):
    TAKE_PHOTO = "takePhoto"
    START_RECORD = "startRecord"
    STOP_RECORD = "stopRecord"
    FOCUS = "focus"
    ZOOM = "zoom"
    CUSTOM_DIR_NAME = "customDirName"
    GIMBAL_ROTATE = "gimbalRotate"
    ROTATE_YAW = "rotateYaw"
    HOVER = "hover"

class RotationMode(Enum):
    CLOCKWISE = "clockwise"
    COUNTER_CLOCKWISE = "counterClockwise"

class CapturingMode(Enum):
    NORMAL_PHOTO = "normalPhoto"
    LOW_LIGHT_SMART_SHOOTING = "lowLightSmartShooting"

class PanoramaPhotoMode(Enum):
    PANO_SHOT_360 = "panoShot_360"

class PointCloudOperation(Enum):
    START_RECORD = "startRecord"
    PAUSE_RECORD = "pauseRecord"
    RESUME_RECORD = "resumeRecord"
    STOP_RECORD = "stopRecord"




