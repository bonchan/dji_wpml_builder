# src/dji_wpml/models/mission.py
from dataclasses import dataclass, field
from dji_wpml.enums.device_enums import DeviceEnum
from typing import Optional, List
from dji_wpml.enums.general_enums import *


@dataclass
class DroneInfo:
    data: DeviceEnum
    @property
    def drone_enum_value(self):
        return self.data.type.type
    @property
    def drone_sub_enum_value(self):
        return self.data.sub_type.sub_type
    
@dataclass
class PayloadInfo:
    data: DeviceEnum
    @property
    def payload_enum_value(self):
        return self.data.type.type
    @property
    def payload_position_index(self):
        return self.data.sub_type.sub_type

@dataclass
class MissionConfig:
    fly_to_wayline_mode: FlyToWaylineMode = FlyToWaylineMode.SAFELY
    finish_action: FinishAction = FinishAction.GO_HOME
    exit_on_rc_lost: ExitOnRCLost = ExitOnRCLost.EXECUTE_LOST_ACTION
    execute_rc_lost_action: ExecuteRCLostAction = ExecuteRCLostAction.GO_BACK
    take_off_security_height: float = 40.0        # Range [8, 1500]
    global_transitional_speed: float = 10.0      # Range [0, 15]
    global_rth_height: float = 60.0             # Range [2, 1500] (From Document 2)
    take_off_ref_point: Optional[tuple] = None
    take_off_ref_point_agl_height: float = None

    drone_info: DroneInfo = None
    payload_info: PayloadInfo = None

    auto_reroute_info: str = None

    def __post_init__(self):
        """Logic to validate requirements between fields."""
        if self.exit_on_rc_lost == ExitOnRCLost.EXECUTE_LOST_ACTION:
            if not self.execute_rc_lost_action:
                raise ValueError("execute_rc_lost_action is required when exit_on_rc_lost is set to executeLostAction")