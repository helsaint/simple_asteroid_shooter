from settings import Vector2
from settings import WHITE
from settings import draw_texture

class Animated_Sprite:
    def __init__(self, pos: Vector2, image_texture: list[Vector2]):
        self.pos = pos
        self.animation_speed = 5
        self.animation_index = 0
        self.animation_frames = image_texture
        self.active = False

    def update(self, dt):
        if self.animation_index > len(self.animation_frames):
            print("Setting explosion to False ", self.animation_index)
            self.animation_index = 0
            self.active = False
        if self.active:
            self.animation_index += self.animation_speed*dt
            
    def draw(self):
        if self.active:
            index = int(self.animation_index)%len(self.animation_frames)
            draw_texture(self.animation_frames[index],
                         int(self.pos.x),int(self.pos.y), WHITE)
