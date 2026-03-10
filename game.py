from pyray import *
from settings import *
from components.snake import Snake
from components.food import Food
from components.button import Button

#Additional features inspo: some sort of rarity with fruits: some give more points, some give a power up. adjust speed

class GameScreen(enumerate):
    STARTUP = 0
    INSTRUCTIONS = 1
    GAME = 2
    PAUSE = 3
    GAMEOVER = 4

class Game():
    def __init__(self):
        self.frames_counter = 0
        self.pause = False
        self.food = Food()
        self.snake = Snake()
        self.current_screen = GameScreen.STARTUP
        self.start_button = Button("Start", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 40), 150, 30, PURPLE, WHITE)
        self.instructions_button = Button("Instructions", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 80), 150, 30, PURPLE, WHITE)
        self.start_button_instructions = Button("Start", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT - 60), 150, 30, PURPLE, WHITE)
        self.restart_button = Button("Restart", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 30), 150, 30, PURPLE, WHITE)
        self.score = 0
        self.eatfx = None

    def startup(self):
        self.snake.startup()
        self.food.startup()
        self.eatfx = load_sound(str(THIS_DIR) + "/resources/eat.wav")

    def update(self):
        if self.current_screen == GameScreen.STARTUP:
            self.update_startup()
        if self.current_screen == GameScreen.INSTRUCTIONS:
            self.update_instructions()
        if self.current_screen == GameScreen.GAME:
            self.update_game()      
        if self.current_screen == GameScreen.GAMEOVER:
            self.update_gameover()

    def draw(self):   
        if self.current_screen == GameScreen.STARTUP:
            self.draw_startup()
        if self.current_screen == GameScreen.INSTRUCTIONS:
            self.draw_instructions()
        if self.current_screen == GameScreen.GAME:
            self.draw_game()
        if self.current_screen == GameScreen.GAMEOVER:
            self.draw_gameover()

    def shutdown(self):
        self.food.shutdown()
        unload_sound(self.eatfx)

    #collision logic
    def wall_collision(self):
        if self.snake.snake[0].rect.x > SCREENWIDTH - OFFSET.x or self.snake.snake[0].rect.y > SCREENHEIGHT - OFFSET.y or self.snake.snake[0].rect.x < 0 or self.snake.snake[0].rect.y < OFFSET_TOP:
            return True
        
    def eat_fruit(self):
        if check_collision_recs(self.snake.snake[0].rect, self.food.rect):
            self.snake.snake[self.snake.counterTail].rect.x = self.snake.snake_position[self.snake.counterTail-1].x
            self.snake.snake[self.snake.counterTail].rect.y = self.snake.snake_position[self.snake.counterTail-1].y
            self.snake.counterTail += 1
            self.score += 10
            self.food.active = False
            play_sound(self.eatfx)

    #Update and draw functions by screen
    def draw_startup(self):
        draw_text("Snake", int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 60), 60, DARKPURPLE)
        self.start_button.draw()
        self.instructions_button.draw()
    
    def update_startup(self):
        if self.start_button.is_clicked():
            self.current_screen = GameScreen.GAME
        if self.instructions_button.is_clicked():
            self.current_screen = GameScreen.INSTRUCTIONS
    
    def update_instructions(self):
        if self.start_button_instructions.is_clicked():
            self.current_screen = GameScreen.GAME

    def draw_instructions(self):
        draw_text("Use Arrow Keys to Move", int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2 - 80), 20, DARKGRAY)
        draw_text("Eat the Red Squares to Grow", int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2 - 50), 20, DARKGRAY)
        draw_text("Don't Run into the Walls or Yourself!", int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2), 20, DARKGRAY)
        draw_text("Press \"P\" to Pause", int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2 + 50), 20, DARKGRAY)
        self.start_button_instructions.draw()

    def update_game(self):
            if is_key_pressed(KeyboardKey.KEY_P):
                self.pause = not self.pause

            if not self.pause:
                self.snake.update()
            
                if self.snake.self_collision():
                    self.current_screen = GameScreen.GAMEOVER  

                if self.wall_collision():
                    self.current_screen = GameScreen.GAMEOVER   

                self.food.update(self.snake.snake_position, self.snake.counterTail)

                self.eat_fruit()
    
    def draw_game(self):
        self.snake.draw()
        self.food.draw()

        draw_text("Snake", int(SCREENWIDTH/2 - 100), 25, 50, DARKPURPLE)
        draw_text(str(self.score), int(SCREENWIDTH/3 * 2), 25, 50, DARKPURPLE)

        for i in range(SCREENWIDTH//SQUARE_SIZE + 1):
            draw_line_v(Vector2(i*SQUARE_SIZE + OFFSET.x/2, OFFSET.y/2 + OFFSET_TOP), Vector2(i*SQUARE_SIZE + OFFSET.x/2, SCREENHEIGHT - OFFSET.y/2), BROWN)

        for i in range((SCREENHEIGHT-OFFSET_TOP)//SQUARE_SIZE + 1):
            draw_line_v(Vector2(OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), Vector2(SCREENWIDTH - OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), BROWN)
    
    def update_gameover(self):
        if is_key_pressed(KeyboardKey.KEY_ENTER) or self.restart_button.is_clicked():
            self.__init__()
            self.startup()
            self.current_screen = GameScreen.GAME
    
    def draw_gameover(self):
        draw_text("Game Over", int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2 - 60), 60, DARKPURPLE)
        self.restart_button.draw()
