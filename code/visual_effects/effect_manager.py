from settings import Vector2
from sprites.explosions import Explosions

class VisualEffectManager:
    def __init__(self, animation_files):
        self.animation_index = 0
        self.animation_files = animation_files
        self.active_explosions = []

    '''Check to see if any animation sprites are not active.
    If None are we create a new Explosion animation sprite, 
    otherwise we reuse an explosion animation sprite.'''                  
    def set_explosion_animation(self, data):
        pos = data['pos']
        explosion_sprite = self._recycled_explosion(pos[0],pos[1])
        if explosion_sprite:
            explosion_sprite.active = True
            explosion_sprite.pos.x = pos[0]
            explosion_sprite.pos.y = pos[1]
        else:
            explosion_sprite = Explosions(Vector2(pos[0],pos[1]),
                                          self.animation_files)
            explosion_sprite.active = True
            self.active_explosions.append(explosion_sprite)

    '''If an explosion sprite is available,
    active=False, then we reuse the explosion.'''
    def _recycled_explosion(self, x, y):
        for explosion in self.active_explosions:
            if not(explosion.active):
                explosion.pos.x = x
                explosion.pos.y = y
                explosion.active = True
                return explosion
        return None
    
    def update(self,dt):
        for explosion in self.active_explosions:
            explosion.update(dt)
            explosion.draw()