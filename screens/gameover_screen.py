from pyray import *
from settings import *
from components.button import Button

class GameOverScreen():
    def __init__(self):
        self.restart_button = Button("Restart", BUTTON_X, int(SCREENHEIGHT/2 + 80), BUTTON_WIDTH, BUTTON_HEIGHT, PURPLE, WHITE)

    def is_restarted(self):
        if is_key_pressed(KeyboardKey.KEY_ENTER) or self.restart_button.is_clicked():
            return True
        return False
    
    def draw(self, score, high_score):
        draw_text("GAME OVER", int(SCREENWIDTH/2 - 175), int(SCREENHEIGHT/2 - 60), LARGE_FONT_SIZE, DARKPURPLE)
        draw_text("SCORE: " + str(score), int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2), MEDIUM_FONT_SIZE, DARKPURPLE)
        draw_text("HIGH SCORE: " + str(high_score), int(SCREENWIDTH/2 - 125), int(SCREENHEIGHT/2 + 30), MEDIUM_FONT_SIZE, DARKPURPLE)
        self.restart_button.draw()