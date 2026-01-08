# src/dji_wpml/models/mission.py
from dataclasses import dataclass, field
from typing import List
from ..enums import DroneModel, ExecuteAction, AltitudeMode

@dataclass
class MissionConfig:
    mission_name: str
    author: str
    create_time: int
    update_time: int
    drone_model: DroneModel
    finish_action: str = "goHome"
    take_off_security_height: int = 60
    global_transitional_speed: int = 10
    altitude_mode: str = "relativeToStartPoint" 
    waypoints: List = field(default_factory=list)

    @property
    def drone_enum_value(self):
        return self.drone_model.value.drone_enum_value

    @property
    def drone_sub_enum_value(self):
        return self.drone_model.value.drone_sub_enum_value
    
    @property
    def payload_enum_value(self):
        return self.drone_model.value.payload_enum_value
    
    @property
    def payload_position_index(self):
        return 0 # self.drone_model.value.payload_position_index
    