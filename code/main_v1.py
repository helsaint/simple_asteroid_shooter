from settings import *
from sprites.meteor import Meteor
from sprites.stars import Star
from sprites.spaceship import Spaceship
from text.score import ScoreDisplay
from text.level_complete import LevelComplete
from text.death import GameOver
#from collision_handlers.laser_meteor_collisions import LaserMeteorCollision
from collision_handlers.laser_meteor import LaserMeteorCollisionHandler
from collision_handlers.meteor_player import MeteorPlayerCollisionHandler
from supers.super_sprite import SpriteGroup
from visual_effects.effect_manager import VisualEffectManager
from events.event_dispatcher import dispatcher
from events.constants import Events
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
        self.is_game_over = False

        # import graphics and audio files
        from load_resources import audio_files, static_images, animation_files, font_files
        self.audio_files = audio_files
        self.static_images = static_images
        self.animation_files = animation_files
        self.score_display = ScoreDisplay(font_files['font'][0])
        self.level_complete_screen = LevelComplete(font_files['font'][0])
        self.game_over_screen = GameOver(font_files['font'][0])

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

        self.player_group = SpriteGroup()
        self.player_group.add(self.spaceship)

        '''set up handler for sprite by sprite collisions
            keeping it for potential reversion
        '''
        '''
        self.laser_meteor_collision = LaserMeteorCollision(self.spaceship.active_lasers,
                                                        self.meteor_group.sprites,
                                                        self.audio_files['explosion_sound'])
        '''
        '''
        Initialize collision handlers
        Note: world dimensions and grid cell size are parameters for the spatial grid system
        '''
        self.laser_meteor_collision = LaserMeteorCollisionHandler(
            lasers=self.spaceship.active_lasers,
            meteors=self.meteor_group.sprites,
            collision_sound=self.audio_files['explosion_sound'],
            world_height=WINDOW_HEIGHT,
            world_width=WINDOW_WIDTH,
            grid_cell_size=100 # Example cell size, adjust as needed
        )
        self.meteor_player_collision = MeteorPlayerCollisionHandler(
            meteors=self.meteor_group.sprites,
            player=self.player_group.sprites,
            collision_sound=self.audio_files['explosion_sound'],
            world_height=WINDOW_HEIGHT,
            world_width=WINDOW_WIDTH,
            grid_cell_size=100 # Example cell size, adjust as needed
        )
        self.explosion_animation = VisualEffectManager(self.animation_files['explosion'])
        
        '''
        Meteor-Laser Collision Events
        '''
        dispatcher.register_event(Events.METEOR_DESTROYED, play_sound_effect)
        dispatcher.register_event(Events.METEOR_DESTROYED, self.score_display.increment_score)
        dispatcher.register_event(Events.METEOR_DESTROYED,
                                  self.explosion_animation.set_explosion_animation)
        dispatcher.register_event(Events.METEOR_DESTROYED,
                                  self.game_state_manager.increment_score)
        
        '''
        Meteor-Player Collision Events
        '''
        dispatcher.register_event(Events.PLAYER_HIT,
                                  self.game_state_manager.player_hit)
        
        play_music_stream(self.audio_files['background_music'])

    # Update sprites
    def update(self, dt):
        if self.is_level_complete or self.is_game_over:
            return
        self.laser_meteor_collision.update(dt)
        self.meteor_player_collision.update(dt)
        self.spaceship.update(dt)
        self.star_group.update(dt)
        self.meteor_group.update(dt)
        self.explosion_animation.update(dt)
        update_music_stream(self.audio_files['background_music'])

         # This check for level completion happens every frame
        if self.game_state_manager.is_level_complete and not self.is_level_complete:
            self.is_level_complete = True
            # Optional: Add logic to save score, etc. before pausing
        if self.game_state_manager.is_game_over and not self.is_game_over:
            self.is_game_over = True

    # Draw sprites
    def draw(self):
        begin_drawing()
        clear_background(BG_COLOR)
        self.star_group.draw()
        self.spaceship.draw()
        self.meteor_group.draw()
        self.score_display.display_score()
        if self.is_level_complete:
            self.level_complete_screen.draw()
        if self.is_game_over:
            self.game_over_screen.draw()

        end_drawing()

    # Unload resources
    def unload_resources(self):
        unload_music_stream(self.audio_files['background_music'])
        unload_texture(self.static_images['star'])
        unload_texture(self.static_images['ship'])
        unload_texture(self.static_images['meteor'])
        unload_texture(self.static_images['laser'])

    def _transition_to_next_level(self):
        if self.is_level_complete:
            if is_key_pressed(KEY_ENTER):
                self.is_level_complete = False
                self.game_state_manager.transition_to_next_level()
                # Reset score display for the new level
                self.score_display.current_score = 0
                # Reset and add meteors for the new level
                self.meteor_group.clear()
                for i in range(self.game_state_manager.initial_meteor_pool_size):
                    temp_meteor = Meteor(Vector2(randint(0, WINDOW_WIDTH),0),
                                         Vector2(0,1), self.static_images['meteor'])
                    self.meteor_group.add(temp_meteor)

    def run(self):
        while not window_should_close():
            
            if self.game_state_manager.is_game_over:
                break
            dt = get_frame_time()
            # update sprites
            self.update(dt)
            # Main Drawing area
            self.draw()
            # Transition to next level
            self._transition_to_next_level()

        # Unload resources and close window
        self.unload_resources()
        close_audio_device()
        close_window()

if __name__=='__main__':
    game = Game()
    game.run()