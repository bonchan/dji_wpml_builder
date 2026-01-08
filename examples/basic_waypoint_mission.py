import uuid
from datetime import datetime
from dji_wpml.core import KMZGenerator
from dji_wpml.models.mission import MissionConfig
from dji_wpml.models.waypoints import Waypoint
from dji_wpml.enums import DroneModel

def generate_example_mission(file_name):
    # 1. Initialize the Mission Configuration
    config = MissionConfig(
        mission_name="Uali Thermal Survey",
        author="Juan",
        create_time=int(datetime.now().timestamp() * 1000), 
        update_time=int(datetime.now().timestamp() * 1000),
        finish_action="goHome",
        take_off_security_height=60,
        global_transitional_speed=10,
        drone_model = DroneModel.MATRICE_4TD,
        altitude_mode="relativeToStartPoint",
    )

    # 2. Define Waypoints with ALL actions from your reference
    
    # Waypoint 0: Simple Oriented Shoot
    wp0 = Waypoint(
        lat=-26.0207473400126, lon=-65.919250923, height=133.55,
        actions=[
            {
                "type": "orientedShoot", 
                "params": {"pitch": 0, "uuid": str(uuid.uuid4())}
            }
        ]
    )

    # Waypoint 1: Complex Sequence (Gimbal, Oriented Shoot x2, Yaw, Focus, Photo, Zoom)
    wp1 = Waypoint(
        lat=-26.0203563577334, lon=-65.919250923, height=133.55,
        actions=[
            {"type": "gimbalRotate", "params": {"pitch": -45}},
            {"type": "orientedShoot", "params": {"pitch": -45, "uuid": str(uuid.uuid4())}},
            {"type": "orientedShoot", "params": {"pitch": -45, "uuid": str(uuid.uuid4())}},
            {"type": "rotateYaw", "params": {"aircraftHeading": 100, "aircraftPathMode": "counterClockwise"}},
            {"type": "gimbalRotate", "params": {"pitch": -45}},
            {"type": "focus", "params": {"x": 0.25, "y": 0.25}},
            {"type": "takePhoto", "params": {}},
            {"type": "zoom", "params": {"focalLength": 24}}
        ]
    )



    # Waypoint 2: Navigation Point (No actions)
    wp2 = Waypoint(
        lat=-26.0199652851958, lon=-65.919250923, height=133.55
    )

    # 3. Add waypoints to the mission
    config.waypoints = [wp0, wp1, wp2]

    # 4. Generate the KMZ
    generator = KMZGenerator(config)
    generator.build(file_name, output_dir="poc", verify=True, unzip=True)

if __name__ == "__main__":
    datestring = datetime.now().strftime("%Y%m%d%H%M%S")
    generate_example_mission(f'{datestring}.kmz')