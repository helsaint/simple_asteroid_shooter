from events.event_dispatcher import dispatcher
from events.constants import Events
from collision_handlers.collision_handler_super import CollisionHandler

class MeteorPlayerCollisionHandler(CollisionHandler):
    def __init__(self, meteors, player, collision_sound,
                 world_width: int, world_height: int, grid_cell_size: int):
        super().__init__(meteors, player, collision_sound,
                         world_width, world_height, grid_cell_size)
        
    def dispatch_events(self, event, x, y):
         if event:
             dispatcher.dispatch_event(Events.PLAYER_HIT, 
                                       {"pos": (x, y),
                                        "increment_lives": -1,
                                        })