from settings import *
from supers.super_sprite import Sprite

class Star(Sprite):
    def __init__(self, pos: Vector2, speed:int, image_location: Texture2D):
        self.direction = Vector2(0,1)
        super().__init__(pos, speed, self.direction, image_location)

    def automated_move(self,dt):
        self.pos.y += dt*self.speed*self.direction.y

    def update(self,dt):
        self.automated_move(dt)
        self._offscreen()