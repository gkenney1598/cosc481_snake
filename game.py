from pyray import *
from settings import *
from components.snake import Snake
from components.food import Food, FruitType
from components.button import Button
from enums import Screens
from screens.startup_screen import StartupScreen
from screens.instruction_screen import InstructionScreen
from screens.gameover_screen import GameOverScreen
from screens.game_screen import GameScreen

# TODO:
# debug when dev mode when switching fruit
# rebrand as the very hungry caterpillar
# make prettier
# add background  music

class Game():
    def __init__(self, high_score = 0):

        self.startup_screen = StartupScreen()
        self.instruction_screen = InstructionScreen()
        self.gameover_screen = GameOverScreen()
        self.game_screen = GameScreen()
        self.current_screen = Screens.STARTUP

        self.score = 0
        self.high_score = high_score

    def startup(self):
        self.instruction_screen.startup()
        self.game_screen.startup()

    def update(self):
        match self.current_screen:
            case Screens.STARTUP:
                self.current_screen = self.startup_screen.update()
            case Screens.INSTRUCTIONS:
                self.current_screen = self.instruction_screen.update()
            case Screens.GAME:
                self.current_screen, self.score = self.game_screen.update(self.score)
            case Screens.GAMEOVER:
                if self.gameover_screen.is_restarted():
                    self.restart_game()

    def draw(self):
        match self.current_screen:
            case Screens.STARTUP:
                self.startup_screen.draw()
            case Screens.INSTRUCTIONS:
                self.instruction_screen.draw(self.food.sprites, self.food.frame_rec)
            case Screens.GAME:
                self.game_screen.draw(self.score, self.high_score)
            case Screens.GAMEOVER:
                self.gameover_screen.draw(self.score, self.high_score)

    def draw(self):
        match self.current_screen:
            case Screens.STARTUP:
                self.startup_screen.draw()
            case Screens.INSTRUCTIONS:
                self.instruction_screen.draw(self.food.sprites, self.food.frame_rec)
            case Screens.GAME:
                self.game_screen.draw(self.score, self.high_score)
            case Screens.GAMEOVER:
                self.gameover_screen.draw(self.score, self.high_score)

    def shutdown(self):
        self.game_screen.shutdown()

    def restart_game(self):
        if self.score > self.high_score: self.high_score = self.score
        self.__init__(self.high_score)
        self.startup()
        self.current_screen = Screens.GAME
