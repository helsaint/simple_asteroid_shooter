from settings import *
from sprites.meteor import Meteor
from sprites.stars import Star
from sprites.spaceship import Spaceship
from text.score import ScoreDisplay
from collision_handler import LaserMeteorCollision
from supers.super_sprite import SpriteGroup
from visual_effects.effect_manager import VisualEffectManager
from events.event_dispatcher import dispatcher
from audio.play_sound import play_sound_effect

class Game:
    def __init__(self):
        # Initialize audio visual elements
        init_window(WINDOW_WIDTH,WINDOW_HEIGHT, "Space Shooter")
        init_audio_device()

        # import graphics and audio files
        from load_resources import audio_files, static_images, animation_files, font_files
        self.audio_files = audio_files
        self.static_images = static_images
        self.animation_files = animation_files
        self.score_display = ScoreDisplay(font_files['font'][0])
        

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
        # set up meteors to shoot    
        meteor_1 = Meteor(Vector2(100,0), Vector2(0,1),
                             self.static_images['meteor'])
        meteor_2 = Meteor(Vector2(500,0), Vector2(0,1),
                             self.static_images['meteor'])
        meteor_3 = Meteor(Vector2(700,0), Vector2(0,1),
                             self.static_images['meteor'])
        
        # Sprite Groups used to manage multiple sprites
        self.meteor_group = SpriteGroup()
        self.meteor_group.add(meteor_1)
        self.meteor_group.add(meteor_2)
        self.meteor_group.add(meteor_3)

        # set up handler for collisions
        self.laser_meteor_collision = LaserMeteorCollision(self.spaceship.active_lasers,
                                                        self.meteor_group.sprites,
                                                        self.audio_files['explosion_sound'])
        
        self.explosion_animation = VisualEffectManager(self.animation_files['explosion'])
        
        # set up events for event dispatcher
        dispatcher.register_event("collision", play_sound_effect)
        dispatcher.register_event("collision", self.score_display.increment_score)
        dispatcher.register_event("collision",
                                  self.explosion_animation.set_explosion_animation)
        
        play_music_stream(self.audio_files['background_music'])
    def run(self):
        while not window_should_close():
            dt = get_frame_time()

            # update sprites
            self.laser_meteor_collision.update(dt)
            self.spaceship.update(dt)
            self.star_group.update(dt)
            self.meteor_group.update(dt)
            self.explosion_animation.update(dt)
            update_music_stream(self.audio_files['background_music'])

            # Main Drawing area
            begin_drawing()
            clear_background(BG_COLOR)
            self.star_group.draw()
            self.spaceship.draw()
            self.meteor_group.draw()
            self.score_display.display_score()
            end_drawing()

        unload_music_stream(self.audio_files['background_music'])
        unload_texture(self.static_images['star'])
        unload_texture(self.static_images['ship'])
        unload_texture(self.static_images['meteor'])
        unload_texture(self.static_images['laser'])
        close_audio_device()
        close_window()

if __name__=='__main__':
    game = Game()
    game.run()