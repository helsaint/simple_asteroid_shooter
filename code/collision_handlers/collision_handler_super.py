from spatial.grid import Grid # Import the new Grid system
from settings import check_collision_recs

class CollisionHandler:
    def __init__(self, objs1, objs2, collision_sound,
                 world_width: int, world_height: int, grid_cell_size: int):
        self.objs1 = objs1
        self.objs2 = objs2
        self.collision_sound = collision_sound
        self.collision_grid = Grid(world_width, world_height, grid_cell_size)

    def _update_grid(self):
        """
        Clears the grid and re-adds all active meteors to their current cells.
        This must be done each frame to account for moving objects.
        """
        self.collision_grid.clear()
        for obj1 in self.objs1:
            if obj1.active:
                self.collision_grid.add_object(obj1)
    
    def _check_collisions(self) -> bool:
        found_any_collision_this_frame = False
        collision_x_pos = None
        collision_y_pos = None

        self._update_grid()

        for obj2 in self.objs2:
            if not obj2.active:
                continue # Skip inactive objects
            
            potential_objs1 = self.collision_grid.get_potential_collisions(obj2)

            for obj1 in potential_objs1:
                if not obj1.active:
                    continue # Skip inactive objects

                if check_collision_recs(obj2.collision_rect, obj1.collision_rect):
                    # Collision detected!
                    obj2.active = False
                    obj1.active = False
                    obj1.destroyed_by_player = True

                    found_any_collision_this_frame = True
                    collision_x_pos = obj1.pos.x
                    collision_y_pos = obj1.pos.y
                    break # Assuming one collision per obj2 per frame
        return found_any_collision_this_frame, collision_x_pos, collision_y_pos

    def update(self, dt):
        """
        Main update method for the collision handler.
        Calls the internal collision check.
        """
        is_collision, x, y = self._check_collisions()
        self.dispatch_events(is_collision, x, y)

    def dispatch_events(self, event, x, y):
        if event:
            # Handle collision event
            pass