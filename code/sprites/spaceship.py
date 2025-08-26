from settings import *
from custom_timer import Timer
from supers.super_sprite import Sprite
from sprites.lasers import Laser

class Spaceship(Sprite):
    def __init__(self, pos: Vector2, speed: int, ship_texture: Texture2D, 
                 laser_texture: Texture2D, laser_sound: Texture2D):
        self.speed = speed
        self.laser_sound = laser_sound
        self.direction = Vector2(0,0)
        self.laser_texture = laser_texture
        self.active_lasers = []
        self.can_shoot = True
        self.timer = Timer(LASER_TIMER_COOLDOWN, False, False, self.laser_cooldown)
        super().__init__(pos, self.speed, self.direction, ship_texture)

    def shoot(self, dt):
        laser_start_pos = Vector2Add(self.pos, 
                                         Vector2(self.texture.width/2, -1*self.texture.height/2))
        if is_key_pressed(KEY_SPACE) and self.can_shoot:
            laser_sprite = self.__recycled_laser()
            if laser_sprite:
                laser_sprite.active = True
                laser_sprite.pos = laser_start_pos
            else:
                laser_sprite = Laser(laser_start_pos, Vector2(0,0), self.laser_texture)
                self.active_lasers.append(laser_sprite)
            play_sound(self.laser_sound)
            self.timer.activate()
            self.laser_cooldown()
        
    def __recycled_laser(self):
        for laser in self.active_lasers:
            if not(laser.active):
                laser.collision_rect.x = self.pos.x
                laser.collision_rect.y = self.pos.y
                return laser
        return None
    
    def laser_cooldown(self):
        self.can_shoot = not(self.can_shoot)
        
    def manual_move(self, dt):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction = Vector2Normalize(self.direction)
        self.pos.x += dt*self.speed*self.direction.x
        if self.pos.x  <= 0:
            self.pos.x = 0
        if self.pos.x >= WINDOW_WIDTH-self.texture.width:
            self.pos.x = WINDOW_WIDTH-self.texture.width

    # Don't want to create too many sprites to limit memory usage
    # So lasers that are inactive will be saved and reused

    def update(self, dt):
        self.timer.update()
        self._update_collision_rect()
        for laser in self.active_lasers:
            if laser.pos.y < 0:
                laser.active = False
                continue
            elif laser.active:
                laser.draw()
                laser.update(dt)
        self.shoot(dt)
        self.manual_move(dt)
