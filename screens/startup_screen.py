from pyray import *
from settings import *
from components.button import Button
from enums import Screens

class StartupScreen():
    def __init__(self):
        self.start_button = Button("Start", BUTTON_X, int(SCREENHEIGHT/2 + 40), BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, WHITE)
        self.instructions_button = Button("Instructions", BUTTON_X, int(SCREENHEIGHT/2 + 80), BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, WHITE)
    
    def update(self):
        if self.start_button.is_clicked():
            return Screens.GAME
        if self.instructions_button.is_clicked():
            return Screens.INSTRUCTIONS
        return Screens.STARTUP

    def draw(self):
        draw_text("THE VERY HUNGRY ", int(SCREENWIDTH/2 - 300), int(SCREENHEIGHT/2 - 90), LARGE_FONT_SIZE, TEXT_COLOR)
        draw_text("SNAKE", int(SCREENWIDTH/2 - 115), int(SCREENHEIGHT/2 - 30), LARGE_FONT_SIZE, TEXT_COLOR)
        self.start_button.draw()
        self.instructions_button.draw()