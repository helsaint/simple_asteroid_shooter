from settings import draw_text_ex, SCORE_LOCATION, SCORE_FONT_SIZE, SCORE_SPACING, SCORE_COLOR

class ScoreDisplay:
    def __init__(self, font):
        self.font = font
        self.current_score = 0

    def increment_score(self, data):
        increment_value = data["increment score"]
        self.current_score = self.current_score + increment_value

    def display_score(self):
        draw_text_ex(self.font, str(self.current_score), SCORE_LOCATION, 
                         SCORE_FONT_SIZE, SCORE_SPACING, SCORE_COLOR)