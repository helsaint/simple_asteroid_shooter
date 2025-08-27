from settings import *
from sprites.meteor import Meteor
from sprites.stars import Star
from sprites.spaceship import Spaceship
from text.score import ScoreDisplay
from text.level_complete import LevelComplete
from collision_handler import LaserMeteorCollision
from supers.super_sprite import SpriteGroup
from visual_effects.effect_manager import VisualEffectManager
from events.event_dispatcher import dispatcher
from audio.play_sound import play_sound_effect
from game_state_manager import load_levels_config, GameStateManager

class Game:
    def __init__(self):
        # Initialize audio visual elements
        init_window(WINDOW_WIDTH,WINDOW_HEIGHT, "Space Shooter")
        init_audio_device()

        # Load level configuration and game state management
        level_config_data = load_levels_config()
        self.game_state_manager = GameStateManager(level_config_data)

        # Game state flag
        self.is_level_complete = False

        # import graphics and audio files
        from load_resources import audio_files, static_images, animation_files, font_files
        self.audio_files = audio_files
        self.static_images = static_images
        self.animation_files = animation_files
        self.score_display = ScoreDisplay(font_files['font'][0])
        self.level_complete = LevelComplete(font_files['font'][0])

        # Import sprites
        self.spaceship = Spaceship(Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100), 
                      PLAYER_SPEED,self.static_images['ship'], self.static_images['laser'],
                      self.audio_files['laser_sound'])
        # setup star background
        self.star_group = SpriteGroup()
        for i in range(STARS_PER_CHUNK):
            self.star_group.add(Star(Vector2(randint(0, WINDOW_WIDTH),
                                             randint(0, WINDOW_HEIGHT)),
                                             PLAYER_SPEED, self.static_images['star']))
       
        '''
        Set up meteors to shoot and add them to the meteor group
        '''
        self.meteor_group = SpriteGroup()
        for i in range(self.game_state_manager.initial_meteor_pool_size):
            temp_meteor = Meteor(Vector2(randint(0, WINDOW_WIDTH),0),
                                 Vector2(0,1), self.static_images['meteor'])
            self.meteor_group.add(temp_meteor)

        # set up handler for collisions
        self.laser_meteor_collision = LaserMeteorCollision(self.spaceship.active_lasers,
                                                        self.meteor_group.sprites,
                                                        self.audio_files['explosion_sound'])
        
        self.explosion_animation = VisualEffectManager(self.animation_files['explosion'])
        
        # set up events for event dispatcher
        dispatcher.register_event("meteor destroyed", play_sound_effect)
        dispatcher.register_event("meteor destroyed", self.score_display.increment_score)
        dispatcher.register_event("meteor destroyed",
                                  self.explosion_animation.set_explosion_animation)
        dispatcher.register_event("meteor destroyed",
                                  self.game_state_manager.increment_score)
        
        play_music_stream(self.audio_files['background_music'])

    # Update sprites
    def update(self, dt):
        if self.is_level_complete:
            return
        self.laser_meteor_collision.update(dt)
        self.spaceship.update(dt)
        self.star_group.update(dt)
        self.meteor_group.update(dt)
        self.explosion_animation.update(dt)
        update_music_stream(self.audio_files['background_music'])

         # This check for level completion happens every frame
        if self.game_state_manager.is_level_complete and not self.is_level_complete:
            self.is_level_complete = True
            # Optional: Add logic to save score, etc. before pausing

    # Draw sprites
    def draw(self):
        begin_drawing()
        clear_background(BG_COLOR)
        self.star_group.draw()
        self.spaceship.draw()
        self.meteor_group.draw()
        self.score_display.display_score()
        if self.is_level_complete:
            self.level_complete.draw()

        end_drawing()

    # Unload resources
    def unload_resources(self):
        unload_music_stream(self.audio_files['background_music'])
        unload_texture(self.static_images['star'])
        unload_texture(self.static_images['ship'])
        unload_texture(self.static_images['meteor'])
        unload_texture(self.static_images['laser'])

    def run(self):
        while not window_should_close():
            dt = get_frame_time()

            # update sprites
            self.update(dt)

            # Main Drawing area
            self.draw()

        # Unload resources and close window
        self.unload_resources()
        close_audio_device()
        close_window()

if __name__=='__main__':
    game = Game()
    game.run()