import os
import json
from datetime import datetime
from dataclasses import asdict
from pprint import pprint
from dji_wpml.core import KMZGenerator
from dji_wpml.models.mission_information import MissionInformation
from dji_wpml.models.mission_config import MissionConfig, DroneInfo, PayloadInfo
from dji_wpml.models.template_information import TemplateInformation
from dji_wpml.models.waylines_information import WaylinesInformation
from dji_wpml.models.waypoint_info import WaypointInfo
from dji_wpml.models.coordinate_parameter_info import CoordinateParameterInfo
from dji_wpml.models.actions import *



# from dji_wpml.models.waypoints import Waypoint
from dji_wpml.enums.device_enums import DeviceEnum
from dji_wpml.enums.general_enums import *

def generate_example_mission(file_name, mission_information):
    generator = KMZGenerator(mission_information)
    generator.build(file_name, output_dir="poc", verify=True, unzip=True)



def iterate_wpml_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    document = data['document']
    m_config_data = document['missionConfig']
    folder_data = document['folder']
    waypoints_data = document['folder']['placemarks']

    # Resolve Drone Enum (91-1 -> M3TD)
    # drone_enum = get_device_enum(
    #     m_config_data['droneInfo']['droneEnumValue'],
    #     m_config_data['droneInfo']['droneSubEnumValue'],
    #     DeviceDomainEnum.DRONE
    # )

    # # Resolve Payload Enum (81-0 -> M3TD_CAMERA)
    # payload_enum = get_device_enum(
    #     m_config_data['payloadInfo']['payloadEnumValue'],
    #     m_config_data['payloadInfo']['payloadSubEnumValue'],
    #     DeviceDomainEnum.PAYLOAD
    # )

    mission_config = MissionConfig(
        fly_to_wayline_mode=FlyToWaylineMode(m_config_data['flyToWaylineMode']),
        finish_action=FinishAction(m_config_data['finishAction']),
        exit_on_rc_lost=ExitOnRCLost(m_config_data['exitOnRCLost']),
        execute_rc_lost_action=ExecuteRCLostAction(m_config_data['executeRCLostAction']),
        take_off_security_height=m_config_data['takeOffSecurityHeight'],
        global_transitional_speed=m_config_data['globalTransitionalSpeed'],
        global_rth_height=m_config_data['globalRTHHeight'],
        take_off_ref_point=m_config_data.get('takeOffRefPoint'), # Safe .get()
        take_off_ref_point_agl_height=m_config_data.get('takeOffRefPointAGLHeight'),
        # Dynamic Injection
        # drone_info=DroneInfo(data=drone_enum),
        # payload_info=PayloadInfo(data=payload_enum),
        # FIXME
        drone_info = DroneInfo(data=DeviceEnum.M3TD),
        # FIXME
        payload_info =  PayloadInfo(data=DeviceEnum.M3TD_CAMERA),
        auto_reroute_info=None,
    )


    # --- 2. Iterate Waypoints & Actions ---

    print(f"--- WAYPOINT EXECUTION ---")
    waypoints_info_list = []

    for wp in waypoints_data:
        idx = wp['index']
        coords = wp.get('point', {}).get('coordinates', "0,0") # Handle nested point
        print(f"Processing WP {idx} at {coords}")

        # 2a. Parse Action Group (if exists)
        action_group_obj = None
        if wp.get('actionGroup'):
            raw_group = wp['actionGroup']
            raw_actions = raw_group['actions']
            
            print(f"  [Action Group {raw_group['actionGroupId']}] executing {len(raw_actions)} tasks:")
            
            # New list for Action Objects (Don't overwrite the loop variable!)
            action_objects = []
            
            for act_idx, act in enumerate(raw_actions):
                func_name = act['actionActuatorFunc']
                params = act.get('actionActuatorFuncParam', {})
                
                # Create Enum safely
                try:
                    act_func_enum = ActionActuatorFunc(func_name)
                except ValueError:
                    print(f"  Warning: Unknown function {func_name}")
                    continue

                param_obj = None
                payload_position_index=params.get('payloadPositionIndex', 0)

                # --- ACTION FACTORY SWITCH ---
                if act_func_enum == ActionActuatorFunc.TAKE_PHOTO:
                    param_obj = TakePhoto(
                        payload_position_index=payload_position_index,
                        file_suffix = None,
                        payload_lens_index = [ImageFormat.ZOOM.value],
                        use_global_payload_lens_index=params.get('useGlobalPayloadLensIndex', 1)
                    )
                elif act_func_enum == ActionActuatorFunc.START_RECORD:
                    param_obj = StartRecord(
                        payload_position_index=payload_position_index
                    )
                elif act_func_enum == ActionActuatorFunc.STOP_RECORD:
                    param_obj = StopRecord(
                        payload_position_index=payload_position_index
                    )
                elif act_func_enum == ActionActuatorFunc.FOCUS:
                    param_obj = Focus(
                        payload_position_index=payload_position_index,
                        payload_lens_index = [ImageFormat.ZOOM.value],
                        use_global_payload_lens_index=params.get('useGlobalPayloadLensIndex', 1),
                        pano_shot_sub_mode = None
                    )
                elif act_func_enum == ActionActuatorFunc.ZOOM:
                    param_obj = Zoom(
                        payload_position_index=payload_position_index,
                        focal_length=params.get('focalLength', 0)
                    )
                elif act_func_enum == ActionActuatorFunc.GIMBAL_ROTATE:
                    param_obj = GimbalRotate(
                        gimbal_rotate_mode=params.get('gimbalRotateMode', 'absoluteAngle'),
                        gimbal_pitch_rotate_enable=params.get('gimbalPitchRotateEnable', 0),
                        gimbal_pitch_rotate_angle=params.get('gimbalPitchRotateAngle', 0),
                        gimbal_yaw_rotate_enable=params.get('gimbalYawRotateEnable', 0),
                        gimbal_yaw_rotate_angle=params.get('gimbalYawRotateAngle', 0),
                        payload_position_index=payload_position_index
                    )
                elif act_func_enum == ActionActuatorFunc.ROTATE_YAW:
                    param_obj = RotateYaw(
                        aircraft_heading=params.get('aircraftHeading', 0),
                        aircraft_path_mode=params.get('aircraftPathMode', 'clockwise')
                    )
                elif act_func_enum == ActionActuatorFunc.HOVER:
                    param_obj = Hover(
                        hover_time=params.get('hoverTime', 0)
                    )
                elif act_func_enum == ActionActuatorFunc.ORIENTED_SHOOT:
                    # Add OrientedShoot mapping if your class supports it
                    param_obj = TakePhoto(payload_position_index=0) # Fallback

                if param_obj:
                    action_objects.append(
                        Action(
                            action_id=act_idx,
                            action_actuator_func=act_func_enum,
                            action_actuator_func_param=param_obj
                        )
                    )

            # Create the ActionGroup Object
            action_group_obj = ActionGroup(
                action_group_id=raw_group['actionGroupId'],
                action_group_start_index=raw_group.get('actionGroupStartIndex', idx),
                action_group_end_index=raw_group.get('actionGroupEndIndex', idx),
                action_group_mode=ActionGroupMode(raw_group.get('actionGroupMode', 'sequence')),
                action_trigger=ActionTrigger(
                    action_trigger_type=TriggerType.REACH_POINT,
                    action_trigger_param=None
                ),
                actions=action_objects
            )

        # 2b. Parse Waypoint Parameters
        # Safely extract coordinate string "lon,lat"
        coord_str = wp.get('point', {}).get('coordinates', "0,0")
        lon, lat = map(float, coord_str.split(','))

        wp_info = WaypointInfo(
            index=idx,
            latitude=lat,
            longitude=lon,
            height=wp.get('executeHeight', 0.0),
            ellipsoid_height=wp.get('ellipsoidHeight', 0.0),
            waypoint_speed=wp.get('waypointSpeed', 0.0),
            
            # Heading Logic
            waypoint_heading_param=wp.get('waypointHeadingParam', {}).get('waypointHeadingAngle', 0),
            use_global_heading_param=False, # Could check logic here
            
            # Turn Logic
            waypoint_turn_param=wp.get('waypointTurnParam', {}).get('waypointTurnDampingDist', 0),
            use_global_turn_param=False,
            
            use_straight_line=bool(wp.get('useStraightLine', 1)),
            is_risky=bool(wp.get('isRisky', 0)),

            use_global_height = True,
            use_global_speed = True,
            gimbal_pitch_angle = 0.0,
            quick_ortho_mapping_enable = False,
            quick_ortho_mapping_pitch = 0.0,

            action_group=action_group_obj,
        )

        waypoints_info_list.append(wp_info)


    # --- 3. Assemble Final Objects ---
    wayline_coord_param = CoordinateParameterInfo(
        height_mode=ExecuteHeightMode(folder_data.get('executeHeightMode')),
        positioning_type=LatitudeAndLongitudeAndAltitudeDataSources.RTK_BASE_STATION,
        global_shoot_height=0.0,
        surface_follow_mode_enable=bool(folder_data.get('realTimeFollowSurfaceByFov', 0)),
        surface_relative_height=0.0
    )

    template_information = TemplateInformation(
        template_type=TemplateType.WAYPOINT,
        template_id=folder_data.get('templateId', 0),
        auto_flight_speed=folder_data.get('autoFlightSpeed', 10.0),
        wayline_coordinate_sys_param=wayline_coord_param,
        payload_param=None, # Add parsing here if needed
        waypoint_info=waypoints_info_list
    )

    waylines_information = WaylinesInformation(
        template_id=folder_data.get('templateId', 0),
        wayline_id=folder_data.get('waylineId', 0),
        auto_flight_speed=folder_data.get('autoFlightSpeed', 10.0),
        execute_height_mode=ExecuteHeightMode.RELATIVE_TO_START_POINT,
        waypoint_info=waypoints_info_list
    )

    mission_information = MissionInformation(
        author=document.get('author', 'Unknown'),
        create_time=document.get('createTime', 0),
        update_time=document.get('updateTime', 0),
        mission_config=mission_config,
        template_information=template_information,
        waylines_information=waylines_information
    )

    return mission_information


if __name__ == "__main__":
    json_file_name = 'full_mission.json'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, json_file_name)

    mission_information = iterate_wpml_json(json_file_path)
    pprint(asdict(mission_information), sort_dicts=False)


    datestring = datetime.now().strftime("%Y%m%d%H%M%S")
    generate_example_mission(f'{datestring}.kmz', mission_information)





