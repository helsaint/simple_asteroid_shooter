from supers.super_sprite import Sprite
from settings import *

class Laser(Sprite):
    def __init__(self, pos: Vector2, direction: Vector2, image_texture: Texture2D):
        self.speed = LASER_SPEED
        super().__init__(pos, self.speed, direction, image_texture)

    def automated_move(self, dt):
        self.pos.y -= dt*self.speed
    
    def update(self,dt):
        self.automated_move(dt)
        self._update_collision_rect()