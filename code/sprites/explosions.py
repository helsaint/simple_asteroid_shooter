from settings import *
from supers.super_animated_sprite import Animated_Sprite

class Explosions(Animated_Sprite):
    def __init__(self, pos: Vector2, image_texture: list[Vector2]):
        super().__init__(pos, image_texture)