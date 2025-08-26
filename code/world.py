from settings import *
from random import randint

class Chunk:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stars = []
        self._generate_stars()
        
    def _generate_stars(self):
        # Create deterministic seed from chunk coordinates
        seed = 5
        
        # Generate random stars within chunk
        for _ in range(STARS_PER_CHUNK):
            self.stars.append((
                randint(0, CHUNK_SIZE),
                randint(0, CHUNK_SIZE),
                (randint(200, 255), randint(200, 255), randint(200, 255))
            ))

class World:
    def __init__(self):
        self.loaded_chunks = {}
        self.world_offset = Vector2(0, 0)
        
    def get_chunk_key(self, chunk_x, chunk_y):
        return f"{chunk_x},{chunk_y}"
    
    def get_current_chunks(self, position):
        chunk_x = int((position.x + self.world_offset.x) // CHUNK_SIZE)
        chunk_y = int((position.y + self.world_offset.y) // CHUNK_SIZE)
        return chunk_x, chunk_y
    
    def update_chunks(self, position):
        current_chunk_x, current_chunk_y = self.get_current_chunks(position)
        
        # Unload distant chunks
        for key in list(self.loaded_chunks.keys()):
            chunk_x, chunk_y = map(int, key.split(','))
            if (abs(chunk_x - current_chunk_x) > RENDER_DISTANCE or 
                abs(chunk_y - current_chunk_y) > RENDER_DISTANCE):
                del self.loaded_chunks[key]
        
        # Load new chunks
        for x in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for y in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                chunk_key = self.get_chunk_key(current_chunk_x + x, current_chunk_y + y)
                if chunk_key not in self.loaded_chunks:
                    self.loaded_chunks[chunk_key] = Chunk(current_chunk_x + x, current_chunk_y + y)
    
    def check_world_offset(self, position):
        global_position = position + self.world_offset
        if abs(global_position.x) > WORLD_THRESHOLD or abs(global_position.y) > WORLD_THRESHOLD:
            self.world_offset += position
            return Vector2(0, 0)
        return position