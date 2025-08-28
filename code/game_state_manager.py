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
        self.current_level = 1
        self.is_level_complete = False
        self.is_player_dead = False
        self.is_game_over = False

        # Get the initial_meteor_pool_size from the loaded config
        # Provide a default of 3 if the key is missing or config_data is None
        #self.initial_meteor_pool_size = config_data.get('initial_meteor_pool_size', 3) if config_data else 3
        self._set_meteors()
        self._set_lives()

    def _set_meteors(self):
        self.initial_meteor_pool_size = self.config_data['levels'][self.current_level
                                                                   -1]['initial_asteroid_pool_size']
        self.asteroids_to_destroy = self.config_data['levels'][self.current_level
                                                               -1]['asteroids_to_destroy']

    def _set_lives(self):
        self.player_initial_life = self.config_data['levels'][self.current_level
                                                               -1]['player_initial_life']

    def _is_game_over(self):
        if (self.is_player_dead or 
            (self.current_level >= len(self.config_data['levels']))):
            self.is_game_over = True

    def increment_score(self, data):
        increment_value = data["increment score"]
        self.current_score = self.current_score + increment_value
        if self.current_score >= self.asteroids_to_destroy:
            self.is_level_complete = True

    def transition_to_next_level(self):
        self._is_game_over()
        print("Game Over", self.current_level, len(self.config_data['levels']),
                  self.is_game_over)
        if self.is_level_complete and not self.is_game_over:
            self.current_level += 1
            self.is_level_complete = False
            self._set_meteors()
