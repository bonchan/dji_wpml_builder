from jinja2 import Environment, PackageLoader, select_autoescape
from dji_wpml.models.mission_information import MissionInformation


# Initialize the environment
env = Environment(
    loader=PackageLoader("dji_wpml", "templates"),
    autoescape=select_autoescape(['xml']),
    # This helps catch errors if a variable is missing
    trim_blocks=True,
    lstrip_blocks=True
)

def build_template_xml(mission_information: MissionInformation):
    template = env.get_template("template_kml.xml")
    return template.render(
        author=mission_information.author,
        create_time=mission_information.create_time,
        update_time=mission_information.update_time,
        mission_config=mission_information.mission_config,
        template_info=mission_information.template_information 
    )

def build_waylines_xml(mission_information: MissionInformation):
    template = env.get_template("waylines_wpml.xml")
    return template.render(
        author=mission_information.author,
        create_time=mission_information.create_time,
        update_time=mission_information.update_time,
        mission_config=mission_information.mission_config,
        waylines_info=mission_information.waylines_information
    )