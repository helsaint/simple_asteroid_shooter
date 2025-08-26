from settings import *
from supers.super_sprite import Sprite
from custom_timer import Timer

class Meteor(Sprite):
    def __init__(self, pos: Vector2, direction: Vector2, image_texture: Texture2D):
        self.speed = randint(METEOR_SPEED_RANGE[0], METEOR_SPEED_RANGE[1])
        self.timers = {
            'spawn': Timer(1,True,True, self.spawn)
        }
        super().__init__(pos, self.speed, direction, image_texture)

    def spawn(self):
        if not(self.active):
            self._offscreen()
            self.active = True

    def rotate(self, dt):
        pass

    def update(self,dt):
        self.automated_move(dt)
        self._update_collision_rect()
        self._offscreen()
        for timer in self.timers.values():
            timer.update()
