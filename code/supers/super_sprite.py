from settings import Vector2, Texture2D, Rectangle
from settings import draw_texture_v, is_key_down, Vector2Normalize
from settings import WHITE, KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, WINDOW_HEIGHT, WINDOW_WIDTH
from random import randint


''' 
Sprite is a parent class for all sprites.
draw() if the Sprite.active = True draw it.
manual_move() checks raylib functions is_key_down()
 to move the sprites via keyboard.
automated_move() used for meteors and stars and laser
 sprites.
_update_collision_rect() raylib requires rectangles
 as unlike pygame-ce the texture itself cannot be used
 so each object, where we care about collisions we have
 to include a Rectangle().These rectangle positions
 obviously have to be updated.

'''
class Sprite:
    def __init__(self, pos: Vector2, speed: int, direction: Vector2, image_texture: Texture2D):
        self.texture = image_texture
        self.pos = pos
        self.speed = speed
        self.active = True
        self.destroyed_by_player = False
        self.width = image_texture.width
        self.height = image_texture.height
        self.collision_rect = Rectangle(self.pos.x, self.pos.y,
                                        self.texture.width, self.texture.height)
        self.direction = Vector2Normalize(direction)

    def draw(self):
        if self.active:
            draw_texture_v(self.texture, self.pos, WHITE)
    
    def manual_move(self, dt):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)
        self.pos.x += dt*self.speed*self.direction.x
        if self.pos.x  <= 0:
            self.pos.x = 0
        if self.pos.x >= WINDOW_WIDTH-self.texture.width:
            self.pos.x = WINDOW_WIDTH-self.texture.width

    def automated_move(self, dt):
        self.pos.y += dt*self.speed*self.direction.y
        self.pos.x += dt*self.speed*self.direction.x

    def _update_collision_rect(self):
        self.collision_rect.x = self.pos.x
        self.collision_rect.y = self.pos.y

    def _offscreen(self):
        if (self.pos.y > WINDOW_HEIGHT) or (self.active == False):
            self.pos.y = randint(-WINDOW_HEIGHT,0)
            self.pos.x = randint(0,WINDOW_WIDTH-self.width)

    def __auto_rotate(self):
        pass

    def update(self, dt):
        pass

# All sprites will be placed in a group so that we can manage
# them more easily.
class SpriteGroup:
    def __init__(self):
        self.sprites = []

    def add(self, sprite):
        self.sprites.append(sprite)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)
    
    def draw(self):
        for sprite in self.sprites:
            sprite.draw()