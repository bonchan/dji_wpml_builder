from dataclasses import dataclass, field
from typing import List

from dji_wpml.enums.general_enums import *

@dataclass
class ActionActuatorFuncParam:
    pass

@dataclass
class TakePhoto(ActionActuatorFuncParam):
    payload_position_index: int
    file_suffix: str
    payload_lens_index: str # ImageFormat: Storage type of photo
    use_global_payload_lens_index: bool

@dataclass
class StartRecord(ActionActuatorFuncParam):
    payload_position_index: int
    file_suffix: str
    payload_lens_index: ImageFormat # Storage type of photo
    use_global_payload_lens_index: bool
    
@dataclass
class StopRecord(ActionActuatorFuncParam):
    payload_position_index: int
    payload_lens_index: ImageFormat # Storage type of photo

@dataclass
class Focus(ActionActuatorFuncParam):
    payload_position_index: int
    is_point_focus: bool
    focus_x: float
    focus_y: float
    focus_region_width: float
    focus_region_height: float
    is_infinite_focus: bool

@dataclass
class Zoom(ActionActuatorFuncParam):
    payload_position_index: int
    focal_length: float

@dataclass
class CustomDirName(ActionActuatorFuncParam):
    payload_position_index: int
    directory_name: str

@dataclass
class GimbalRotate(ActionActuatorFuncParam):
    payload_position_index: int = None
    gimbal_heading_yaw_base: str = "north"
    gimbal_rotate_mode: str = "absoluteAngle"
    gimbal_pitch_rotate_enable: bool = False
    gimbal_pitch_rotate_angle: float = None
    gimbal_roll_rotate_enable: bool = False
    gimbal_roll_rotate_angle: float = None
    gimbal_yaw_rotate_enable: bool = False
    gimbal_yaw_rotate_angle: float = None
    gimbal_rotate_time_enable: bool = False
    gimbal_rotate_time: float = None

@dataclass
class GimbalEvenlyRotate(ActionActuatorFuncParam):
    payload_position_index: int
    gimbal_pitch_rotate_angle: float

@dataclass
class RotateYaw(ActionActuatorFuncParam):
    aircraft_heading: float
    aircraft_path_mode: RotationMode

@dataclass
class Hover(ActionActuatorFuncParam):
    hover_time: float

@dataclass
class AccurateShoot(ActionActuatorFuncParam):
    pass

@dataclass
class OrientedShoot(ActionActuatorFuncParam):
    gimbal_pitch_rotate_angle: float
    gimbal_yaw_rotate_angle: float
    focus_x: int
    focus_y: int
    focus_region_width: int
    focus_region_height: int
    focal_length: float
    aircraft_heading: float
    accurate_frame_valid: bool
    payload_position_index: int
    payload_lens_index: ImageFormat
    use_global_payload_lens_index: bool
    target_angle: float
    action_uuid: str
    image_width: int
    image_height: int
    af_pos: int
    gimbal_port: int
    oriented_camera_type: int
    oriented_file_path: str
    oriented_file_md5: str
    oriented_file_size: str
    oriented_file_suffix: str
    oriented_camera_apertue: int
    oriented_camera_luminance: int
    oriented_camera_shutter_time: float
    oriented_camera_iso: int
    oriented_photo_mode: CapturingMode

@dataclass
class Focus(ActionActuatorFuncParam):
    payload_position_index: int
    payload_lens_index: ImageFormat
    use_global_payload_lens_index: float
    pano_shot_sub_mode: PanoramaPhotoMode

@dataclass
class RecordPointCloud(ActionActuatorFuncParam):
    payload_position_index: int
    record_point_cloud_operate: PointCloudOperation

@dataclass
class Megaphone(ActionActuatorFuncParam):
    pass

@dataclass
class Searchlight(ActionActuatorFuncParam):
    pass

@dataclass
class ActionTrigger:
    action_trigger_type: TriggerType
    action_trigger_param: float

@dataclass
class Action:
    action_id: int
    action_actuator_func: ActionActuatorFunc
    action_actuator_func_param: ActionActuatorFuncParam

@dataclass
class ActionGroup: 
    action_group_id: int
    action_group_start_index: int
    action_group_end_index: int
    action_group_mode: ActionGroupMode
    action_trigger: ActionTrigger
    actions: List = field(default_factory=list)
