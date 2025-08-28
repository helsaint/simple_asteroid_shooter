from math import floor, ceil

class Grid:
    """
    Implements a simple 2D grid-based spatial partitioning system.
    It divides the game world into cells and stores objects within those cells.
    This helps optimize collision detection by reducing the number of objects
    to check for any given object.
    """
    def __init__(self, world_width: int, world_height: int, cell_size: int):
        """
        Initializes the grid.

        Args:
            world_width (int): The total width of the game world (e.g., screen width).
            world_height (int): The total height of the game world (e.g., screen height).
            cell_size (int): The size (width and height) of each square cell in the grid.
                             A good starting point is often slightly larger than your average object size.
        """
        if cell_size <= 0:
            raise ValueError("Cell size must be a positive integer.")
        if world_width <= 0 or world_height <= 0:
            raise ValueError("World dimensions must be positive integers.")

        self.cell_size = cell_size
        self.grid_width = ceil(world_width / cell_size)
        self.grid_height = ceil(world_height / cell_size)
        
        # self.cells will store a dictionary where keys are (col, row) tuples
        # and values are lists of objects currently in that cell.
        self.cells = {}
        self.clear() # Initialize all cells as empty

        print(f"Grid initialized: {self.grid_width}x{self.grid_height} cells, each {cell_size}x{cell_size}.")

    def _get_cell_coordinates(self, position) -> tuple[int, int]:
        """
        Calculates the grid cell coordinates (column, row) for a given world position.

        Args:
            position: A Vector2-like object with .x and .y attributes
                      representing the object's center in world coordinates.

        Returns:
            tuple[int, int]: The (column, row) coordinates of the cell.
        """
        cell_x = floor(position.x / self.cell_size)
        cell_y = floor(position.y / self.cell_size)
        return (cell_x, cell_y)

    def add_object(self, obj):
        """
        Adds an object to the grid based on its current position.
        Objects are expected to have a 'position' attribute (e.g., Vector2).

        Args:
            obj: The game object to add (e.g., a Meteor instance).
        """
        if not hasattr(obj, 'pos') or not hasattr(obj.pos, 'x') or not hasattr(obj.pos, 'y'):
            raise AttributeError("Object must have a 'position' attribute with 'x' and 'y'.")

        cell_x, cell_y = self._get_cell_coordinates(obj.pos)
        
        # Clamp coordinates to ensure they are within grid bounds
        # This handles objects that might slightly go off-screen
        cell_x = max(0, min(cell_x, self.grid_width - 1))
        cell_y = max(0, min(cell_y, self.grid_height - 1))

        # Add the object to the list associated with its cell
        # Using .append() is efficient for adding to the end of a list.
        self.cells[(cell_x, cell_y)].append(obj)

    def clear(self):
        """
        Clears all objects from all grid cells.
        This should be called at the beginning of each frame's collision update
        to ensure objects are re-added at their new positions.
        """
        # Re-initialize all cells as empty lists
        for col in range(self.grid_width):
            for row in range(self.grid_height):
                self.cells[(col, row)] = []

    def get_potential_collisions(self, obj):
        """
        Returns a list of objects that are in the same cell as the given object
        or in its immediate neighboring cells. These are the objects that are
        "potential" collision candidates and need further precise checking.

        Args:
            obj: The game object for which to find potential collisions.

        Returns:
            list: A list of unique game objects that are potentially colliding.
                  The object itself is included in this list, which should be
                  filtered out by the caller if not desired (e.g., self-collision).
        """
        if not hasattr(obj, 'pos') or not hasattr(obj.pos, 'x') or not hasattr(obj.pos, 'y'):
            raise AttributeError("Object must have a 'pos' attribute with 'x' and 'y'.")

        potential_collisions = set() # Use a set to automatically handle duplicates and improve lookup speed

        obj_cell_x, obj_cell_y = self._get_cell_coordinates(obj.pos)

        # Iterate through the object's cell and its 8 neighbors (3x3 area)
        for dx in range(-1, 2):  # -1, 0, 1
            for dy in range(-1, 2):  # -1, 0, 1
                neighbor_cell_x = obj_cell_x + dx
                neighbor_cell_y = obj_cell_y + dy

                # Check if the neighbor cell is within the grid bounds
                if 0 <= neighbor_cell_x < self.grid_width and \
                   0 <= neighbor_cell_y < self.grid_height:
                    
                    # Add all objects from this neighbor cell to our set
                    # The .get() method is safer for cells that might not have been explicitly initialized
                    # though clear() handles this.
                    for candidate_obj in self.cells.get((neighbor_cell_x, neighbor_cell_y), []):
                        potential_collisions.add(candidate_obj)

        return list(potential_collisions)

