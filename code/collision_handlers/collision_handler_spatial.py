from pyray import Vector2 # Assuming Vector2 is part of pyray
from events.event_dispatcher import dispatcher
from events.constants import Events # Using constants for event names
from spatial.grid import Grid # Import the new Grid system

# Assuming check_collision_recs is a direct import from raylib or a settings file
# If check_collision_recs is part of pyray, you might import it as:
# from pyray import check_collision_recs
# Or if it's in settings:
# from settings import check_collision_recs

# For this example, let's assume it's directly available or imported like this:
def check_collision_recs(rect1, rect2) -> bool:
    """
    Placeholder for pyray's check_collision_recs function.
    In your actual code, this would be imported directly from pyray or your settings.
    """
    # Assuming rects have x, y, width, height attributes
    return (rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.y + rect1.height > rect2.y)

class LaserMeteorCollision:
    """
    Handles collision detection between lasers and meteors,
    using a spatial grid for optimized checks.
    """
    def __init__(self, lasers, meteors, explosion_sound, 
                 world_width: int, world_height: int, grid_cell_size: int):
        """
        Initializes the collision handler.

        Args:
            lasers (list): List of laser objects.
            meteors (list): List of meteor objects.
            explosion_sound: The sound to play on meteor destruction.
            world_width (int): The total width of the game world (e.g., screen width).
            world_height (int): The total height of the game world (e.g., screen height).
            grid_cell_size (int): The size of each cell in the spatial grid.
        """
        self.lasers = lasers
        self.meteors = meteors
        self.explosion_sound = explosion_sound
        
        # Initialize the spatial grid
        self.collision_grid = Grid(world_width, world_height, grid_cell_size)
        print(f"LaserMeteorCollision handler initialized with Grid. Grid cell size: {grid_cell_size}.")

    def _update_grid(self):
        """
        Clears the grid and re-adds all active meteors to their current cells.
        This must be done each frame to account for moving objects.
        """
        self.collision_grid.clear()
        for meteor in self.meteors:
            if meteor.active:
                self.collision_grid.add_object(meteor)

    def _check_meteor_laser_collision(self) -> bool:
        """
        Checks for collisions between active meteors and active lasers,
        leveraging the spatial grid to reduce unnecessary checks.

        Returns:
            bool: True if any collision was detected and handled, False otherwise.
        """
        found_any_collision_this_frame = False
        
        # Step 1: Update the grid with all active meteors' current positions
        self._update_grid()

        # Step 2: Iterate through lasers and check for collisions with nearby meteors
        for laser in self.lasers:
            if not laser.active:
                continue # Skip inactive lasers

            # Get only the meteors that are potentially near this laser
            # (i.e., in the same or adjacent grid cells)
            potential_meteors = self.collision_grid.get_potential_collisions(laser)

            for meteor in potential_meteors:
                if not meteor.active:
                    continue # Skip inactive meteors in the potential list

                # Perform the precise collision check only on potential candidates
                # Assuming meteor and laser objects have a 'collision_rect' attribute
                if check_collision_recs(laser.collision_rect, meteor.collision_rect):
                    # Collision detected!
                    laser.active = False
                    meteor.active = False
                    meteor.destroyed_by_player = True # Set flag for score/tracking

                    # Dispatch collision event using constants
                    dispatcher.dispatch_event(Events.METEOR_DESTROYED, 
                                            {"explosion_sound": self.explosion_sound,
                                             "increment score": 1, # Example score increment
                                             "pos": (meteor.pos.x, meteor.pos.y)})
                    found_any_collision_this_frame = True
                    # Optimization: A laser can only hit one meteor per frame,
                    # so once it hits, it's inactive, and we can stop checking
                    # this laser against other meteors.
                    break 
        return found_any_collision_this_frame
    
    def update(self, dt): 
        """
        Main update method for the collision handler.
        Calls the internal collision check.
        """
        self._check_meteor_laser_collision()

