from environment import CONFIG_MAP_MESSAGE, CONFIG_MAP_FILE_PATH


def get_config_map():
    """ Extract the k8s config map message from the config 
        map file or the environment variable 
    """
    config_map_message = CONFIG_MAP_MESSAGE
    if CONFIG_MAP_FILE_PATH:
        try:
            with open(CONFIG_MAP_FILE_PATH, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading config map file: {e}")
            return None
    return config_map_message or "No config map message"
