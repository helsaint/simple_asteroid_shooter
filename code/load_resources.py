from os.path import join, dirname, abspath
from settings import load_texture, load_sound, load_music_stream, load_font

script_dir = dirname(abspath(__file__))
project_folder = dirname(dirname(script_dir))

static_images = {
    #'star': load_texture(join('simple_asteroid_shooting', 'images', 'star.png')),
    'star': load_texture(join(project_folder, 'simple_asteroid_shooting','images', 'star.png')),
    'ship': load_texture(join(project_folder, 'simple_asteroid_shooting', 'images', 'spaceship.png')),
    'laser': load_texture(join(project_folder,'simple_asteroid_shooting', 'images', 'laser.png')),
    'meteor': load_texture(join(project_folder, 'simple_asteroid_shooting', 'images', 'meteor.png')), 
}

audio_files = {
    'laser_sound':load_sound(join(project_folder, 'simple_asteroid_shooting', 'audio', 'laser.wav')),
    'background_music': load_music_stream(join(project_folder, 'simple_asteroid_shooting', 'audio', 'music.wav')),
    'explosion_sound': load_sound(join(project_folder, 'simple_asteroid_shooting', 'audio', 'explosion.wav'))
}

animation_files = {
    'explosion': [load_texture(join(project_folder, 'simple_asteroid_shooting', 'images',
                                    'explosion',f'{i}.png')) for i in range(1,28)]
}

font_files = {
    'font':[load_font(join(project_folder, 'simple_asteroid_shooting', 'font',
                           'Stormgace.otf'))]
}