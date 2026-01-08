from jinja2 import Environment, PackageLoader, select_autoescape

# Initialize the environment
env = Environment(
    loader=PackageLoader("dji_wpml", "templates"),
    autoescape=select_autoescape(['xml']),
    # This helps catch errors if a variable is missing
    trim_blocks=True,
    lstrip_blocks=True
)

def build_template_xml(config):
    template = env.get_template("template_kml.xml")
    return template.render(
        author=config.author,
        create_time=config.create_time,
        update_time=config.update_time,
        finish_action=config.finish_action,
        take_off_security_height=config.take_off_security_height,
        global_transitional_speed=config.global_transitional_speed,
        drone_enum_value=config.drone_enum_value,
        drone_sub_enum_value=config.drone_sub_enum_value,
        payload_enum_value=config.payload_enum_value,
        payload_position_index=config.payload_position_index,
        altitude_mode=config.altitude_mode,
        waypoints=config.waypoints
    )

def build_waylines_xml(config):
    template = env.get_template("waylines_wpml.xml")
    return template.render(
        author=config.author,
        create_time=config.create_time,
        update_time=config.update_time,
        finish_action=config.finish_action,
        take_off_security_height=config.take_off_security_height,
        global_transitional_speed=config.global_transitional_speed,
        drone_enum_value=config.drone_enum_value,
        drone_sub_enum_value=config.drone_sub_enum_value,
        payload_enum_value=config.payload_enum_value,
        altitude_mode=config.altitude_mode,
        waypoints=config.waypoints
    )