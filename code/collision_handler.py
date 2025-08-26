from settings import check_collision_recs
from sprites.explosions import Explosions
from events.event_dispatcher import dispatcher
class LaserMeteorCollision:
    def __init__(self, lasers, meteors, explosion_sound):
        self.lasers = lasers
        self.meteors = meteors
        self.explosion_sound = explosion_sound

    '''Check for collisions between meteor sprites and
    laser sprites. Because we are reusing sprites
    we have to keep track of which sprite is active
    and which isn't. Once a laser hits a meteor both
    need to not appear anymore so we set their attribute
    active to False.'''
    def _check_collision(self) -> bool:
        for laser in self.lasers:
            if not(laser.active):
                continue
            for meteor in self.meteors:
                if not(meteor.active):
                    continue
                # check_collision_recs is a raylib library
                if(check_collision_recs(laser.collision_rect, 
                                        meteor.collision_rect)) and meteor.active:
                    laser.active = False
                    meteor.active = False
                    meteor.destroyed_by_player = True
                    # dispatch collision event
                    dispatcher.dispatch_event("collision", 
                                              {"explosion_sound": self.explosion_sound,
                                               "increment score": 1,
                                               "pos": (meteor.pos.x, meteor.pos.y),
                                               })
                    return True
        return False            
        
    '''If a collision happens play explosion sound.
    Go through each explosion animation sprite and
    use the sprite parent class to update and draw
    the animations.'''
    def update(self,dt): 
        if self._check_collision():
            pass