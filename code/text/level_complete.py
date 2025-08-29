from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK
from settings import draw_text_ex, Fade, draw_rectangle
from settings import LEVEL_TEXT_MESSAGE, LEVEL_TEXT_SIZE, LEVEL_TEXT_WIDTH
from settings import LEVEL_CONTINUE_MESSAGE, LEVEL_CONTINUE_TEXT_SIZE, LEVEL_CONTINUE_TEXT_WIDTH
from settings import LEVEL_TEXT_LOCATION, LEVEL_CONTINUE_TEXT_LOCATION
from settings import LEVEL_TEXT_COLOR, LEVEL_CONTINUE_TEXT_COLOR

class LevelComplete:
    def __init__(self, font):
        self.font = font
        self.message = LEVEL_TEXT_MESSAGE
        self.text_size = LEVEL_TEXT_SIZE
        self.text_width = LEVEL_TEXT_WIDTH
        self.continue_message = LEVEL_CONTINUE_MESSAGE
        self.continue_text_size = LEVEL_CONTINUE_TEXT_SIZE
        self.continue_text_width = LEVEL_CONTINUE_TEXT_WIDTH

    def draw(self):
        draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Fade(BLACK, 0.7))
        draw_text_ex(self.font, self.message, 
                     LEVEL_TEXT_LOCATION, 
                             self.text_size, 0, LEVEL_TEXT_COLOR)
        
        draw_text_ex(self.font, self.continue_message, 
                     LEVEL_CONTINUE_TEXT_LOCATION, 
                             self.continue_text_size, 0, LEVEL_CONTINUE_TEXT_COLOR)