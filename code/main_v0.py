from settings import *
from simple_asteroid_shooting.code.custom_timer import Timer
from sprite import Star, Spaceship, Meteor
from random import randint, choice
from collision_handler import LaserMeteorCollision

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Destroy Asteroids in the field")
init_audio_device()

from load_resources import static_images, audio_files

spaceship = Spaceship(Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100), 
                      PLAYER_SPEED,static_images['ship'], static_images['laser'],
                      audio_files['laser_sound'])
stars = [Star(Vector2(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)),
              PLAYER_SPEED,static_images['star'])
         for i in range(STARS_PER_CHUNK)]
meteor = Meteor(Vector2(100,400), Vector2(0,0),static_images['meteor'])

# Play background music
play_music_stream(audio_files['background_music'])

while not window_should_close():
    # Check collisions
    # Background music
    update_music_stream(audio_files['background_music'])
    dt = get_frame_time()
    spaceship.update(dt)
    begin_drawing()
    clear_background(BG_COLOR)

    for laser in spaceship.active_lasers:
        if LaserMeteorCollision.check_collision(meteor.collision_rect, 
                                                laser.collision_rect):
            laser.active = False
            print(laser.active)

    for star in stars:
        star.draw()
        star.update(dt)
    spaceship.draw()
    meteor.draw()
    
    end_drawing()
unload_texture(static_images['star'])
unload_texture(static_images['laser'])
unload_texture(static_images['ship'])
close_window()