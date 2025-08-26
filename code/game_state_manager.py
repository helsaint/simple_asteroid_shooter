from os.path import join, dirname, abspath
import json

script_dir = dirname(abspath(__file__))
project_folder = dirname(script_dir)

def load_levels_config(file_name="levels.json"):
    config_path = join(project_folder, 'configs', file_name)

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from config file: {config_path}")
        return None
    
class GameStateManager:
    """
    Manages only the initial asteroid pool size from the configuration.
    """
    def __init__(self, config_data):
        self.config_data = config_data
        self.current_score = 0
        self.current_level = 0
        
        # Get the initial_meteor_pool_size from the loaded config
        # Provide a default of 3 if the key is missing or config_data is None
        self.initial_meteor_pool_size = config_data.get('initial_meteor_pool_size', 3) if config_data else 3

    def increment_score(self, amount):
        self.current_score += amount
