from settings import WINDOW_HEIGHT, WINDOW_WIDTH, BLACK
from settings import draw_text_ex, Fade, draw_rectangle
from settings import GAME_OVER_TEXT_MESSAGE, GAME_OVER_TEXT_SIZE, GAME_OVER_TEXT_WIDTH
from settings import GAME_OVER_TEXT_LOCATION, GAME_OVER_TEXT_COLOR

class GameOver:
    def __init__(self, font):
        self.font = font
        self.message = GAME_OVER_TEXT_MESSAGE
        self.text_size = GAME_OVER_TEXT_SIZE
        self.text_width = GAME_OVER_TEXT_WIDTH
        self.text_location = GAME_OVER_TEXT_LOCATION
        self.text_color = GAME_OVER_TEXT_COLOR
        
    def draw(self):
        draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, Fade(BLACK, 0.7))
        draw_text_ex(self.font, self.message, self.text_location, 
                     self.text_size,0, self.text_color)
