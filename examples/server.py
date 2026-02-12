from dotenv import load_dotenv
import os
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import traceback

from dji_wpml.core import KMZGenerator
from dji_wpml.models.mission_information import MissionInformation
from dji_wpml.models.mission_config import MissionConfig, DroneInfo, PayloadInfo
from dji_wpml.models.template_information import TemplateInformation
from dji_wpml.models.waylines_information import WaylinesInformation
from dji_wpml.models.waypoint_info import WaypointInfo
from dji_wpml.models.coordinate_parameter_info import CoordinateParameterInfo
from dji_wpml.models.actions import *

from dji_wpml.enums.device_enums import DeviceEnum
from dji_wpml.enums.general_enums import *

from dji_wpml.utils.fh_uploader import FHUploader
from dji_wpml.utils.utils import str_to_bool, normalize_heading

load_dotenv()

app = Flask(__name__)
CORS(app)

STORAGE_PATH = os.getenv("STORAGE_PATH")
STORAGE_GENERATED_WAYLINES_FOLDER = os.getenv("STORAGE_GENERATED_WAYLINES_FOLDER")
output_dir = os.path.join(STORAGE_PATH, STORAGE_GENERATED_WAYLINES_FOLDER)

FH_API_BASE_URL = os.getenv("FH_API_BASE_URL")
FH_PROJECT_UUID = os.getenv("FH_PROJECT_UUID")
FH_ORGANIZATION_KEY = os.getenv("FH_ORGANIZATION_KEY")
FH_UPLOAD = str_to_bool(os.getenv("FH_UPLOAD", "false"))

if FH_API_BASE_URL is None or FH_PROJECT_UUID is None or FH_ORGANIZATION_KEY is None:
    raise ValueError("environment variables not set.")

fh_uploader = FHUploader(FH_API_BASE_URL, FH_PROJECT_UUID, FH_ORGANIZATION_KEY)

@app.route('/generate-mission', methods=['POST'])
def generate_mission():
    """
    Endpoint that receives mission parameters in JSON,
    generates a KMZ file using dji_wpml_builder, and returns the file.
    """
    
    # 1. Get parameters from the request body
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid JSON: 'god knows whats missing"}), 400

    # Create a temporary directory to store the generated file
    # This ensures we don't clutter the server and handles concurrent requests safely
    # temp_dir = tempfile.mkdtemp()
    
    try:
        filename = f"{data.get('missionName', 'mission')}.kmz"
        # output_path = os.path.join(temp_dir, filename)
        print(f"Processing Mission: {filename}")

        mission_config = MissionConfig(
            # fly_to_wayline_mode=FlyToWaylineMode(m_config_data['flyToWaylineMode']),
            # finish_action=FinishAction(m_config_data['finishAction']),
            # exit_on_rc_lost=ExitOnRCLost(m_config_data['exitOnRCLost']),
            # execute_rc_lost_action=ExecuteRCLostAction(m_config_data['executeRCLostAction']),
            # take_off_security_height=m_config_data['takeOffSecurityHeight'],
            # global_transitional_speed=m_config_data['globalTransitionalSpeed'],
            # global_rth_height=m_config_data['globalRTHHeight'],
            # take_off_ref_point=m_config_data.get('takeOffRefPoint'), # Safe .get()
            # take_off_ref_point_agl_height=m_config_data.get('takeOffRefPointAGLHeight'),

            # Dynamic Injection
            # drone_info=DroneInfo(data=drone_enum),
            # payload_info=PayloadInfo(data=payload_enum),
            # FIXME
            drone_info = DroneInfo(data=DeviceEnum.M4TD),
            # FIXME
            payload_info =  PayloadInfo(data=DeviceEnum.M4TD_CAMERA),
            auto_reroute_info=None,
        )


        # --- 2. Iterate Waypoints & Actions ---

        print(f"--- WAYPOINT EXECUTION ---")
        waypoints_info_list = []

        # 2. Iterate through the cameras
        waypoints = data.get('waypoints', [])
        
        for idx, wp in enumerate(waypoints):
            # Extract Position
            lat = wp['position']['latitude']
            lon = wp['position']['longitude']
            altitude = wp['position']['altitude']
            heightAboveGround = wp['position']['heightAboveGround']
            
            print(f" -> Adding Waypoint for index '{idx}': Lat={lat}, Lon={lon}, Altitude={altitude}")

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
                            aircraft_heading=normalize_heading(params.get('aircraftHeading', 0)),
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

            wp_info = WaypointInfo(
                index=idx,
                latitude=lat,
                longitude=lon,
                height=heightAboveGround, # wp.get('executeHeight', 0.0),
                ellipsoid_height=altitude, # wp.get('ellipsoidHeight', 0.0),
                waypoint_speed=10, # wp.get('waypointSpeed', 0.0),
                
                # Heading Logic
                waypoint_heading_param=0, # wp.get('waypointHeadingParam', {}).get('waypointHeadingAngle', 0),
                use_global_heading_param=False, # Could check logic here
                
                # Turn Logic
                waypoint_turn_param=0, # wp.get('waypointTurnParam', {}).get('waypointTurnDampingDist', 0),
                use_global_turn_param=False,
                
                use_straight_line=1, # bool(wp.get('useStraightLine', 1)),
                is_risky=0, # bool(wp.get('isRisky', 0)),

                use_global_height = True,
                use_global_speed = True,
                gimbal_pitch_angle = 0.0,
                quick_ortho_mapping_enable = False,
                quick_ortho_mapping_pitch = 0.0,

                action_group=action_group_obj,
            )
            waypoints_info_list.append(wp_info)


        wayline_coord_param = CoordinateParameterInfo(
            height_mode=ReferencePlaneForWaypointElevation.ABOVE_GROUND_LEVEL,
            positioning_type=LatitudeAndLongitudeAndAltitudeDataSources.RTK_BASE_STATION,
            global_shoot_height=data.get('groundLevel', 0.0),
            surface_follow_mode_enable=0,
            surface_relative_height=0.0
        )

        template_information = TemplateInformation(
            template_type=TemplateType.WAYPOINT,
            template_id=0, # folder_data.get('templateId', 0),
            auto_flight_speed=10.0, # folder_data.get('autoFlightSpeed', 10.0),
            wayline_coordinate_sys_param=wayline_coord_param,
            payload_param=None, # Add parsing here if needed
            waypoint_info=waypoints_info_list
        )

        waylines_information = WaylinesInformation(
            template_id=0, # folder_data.get('templateId', 0),
            wayline_id=0, # folder_data.get('waylineId', 0),
            auto_flight_speed=10.0, # folder_data.get('autoFlightSpeed', 10.0),
            execute_height_mode=ExecuteHeightMode.RELATIVE_TO_START_POINT,
            waypoint_info=waypoints_info_list
        )

        mission_information = MissionInformation(
            author='Juan', # document.get('author', 'Unknown'),
            create_time=None, # document.get('createTime', 0),
            update_time=None, # document.get('updateTime', 0),
            mission_config=mission_config,
            template_information=template_information,
            waylines_information=waylines_information
        )

        generator = KMZGenerator(mission_information)
        full_path = generator.build(filename, output_dir=output_dir, verify=True, unzip=True)

        if FH_UPLOAD:
            fh_uploader.upload_file(full_path)

        # 3. Schedule cleanup of the file after the response is sent
        # @after_this_request
        # def cleanup(response):
        #     try:
        #         shutil.rmtree(temp_dir)
        #     except Exception as e:
        #         app.logger.error(f"Error cleaning up temp dir: {e}")
        #     return response

        # 4. Send the file back to the client
        # return send_file(
        #     output_path,
        #     mimetype='application/vnd.google-earth.kmz',
        #     as_attachment=True,
        #     download_name=filename
        # )
        return jsonify({"status": "ok", "filename": filename}), 200

    except Exception as e:
        # Clean up in case of error
        # shutil.rmtree(temp_dir, ignore_errors=True)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)