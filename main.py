from pyray import *
from game import Game
from settings import SCREENWIDTH, SCREENHEIGHT, BACKGROUND_COLOR

if __name__ == '__main__':
    init_window(SCREENWIDTH, SCREENHEIGHT, "snake")
    init_audio_device()
    set_target_fps(60)

    current_game = Game()
    current_game.startup()

    while not window_should_close():
        current_game.update()

        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        current_game.draw()
        end_drawing()

    current_game.shutdown()
    close_audio_device()
    close_window()