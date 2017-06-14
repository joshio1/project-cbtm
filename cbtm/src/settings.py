import ConfigParser
import utils
import os

_config = ConfigParser.RawConfigParser(allow_no_value=True)
project_folder = utils.get_parent_abs(utils.get_parent_abs(__file__))
settings_path = project_folder+os.path.sep+"settings.cfg"
_config.readfp(open(settings_path))

def get(section,key):
    try:
        return _config.get(section, key)
    except:
        return ""