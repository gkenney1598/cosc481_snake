from pyray import *
from settings import *
from components.snake import Snake
from components.food import Food, FruitType
from components.button import Button

# TODO:
# debug moving sprite to not be in snake tail
# debug watermelon being spawned half off the map
# high score feature
# get rid of magic numbers
# refactor to different game screen classes

class ScoreMode(enumerate):
    NORMAL = 0
    DOUBLE = 1
    HALF = 2

class Game():
    def __init__(self):
        #TODO: organize init by game screen or create classes for each screen cuz this is getting long
        self.frames_counter = 0
        self.pause = False
        self.food = Food()
        self.snake = Snake()
        self.current_screen = GameScreen.STARTUP
        #start up screen inits
        self.start_button = Button("Start", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 40), 150, 30, PURPLE, WHITE)
        self.instructions_button = Button("Instructions", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 80), 150, 30, PURPLE, WHITE)
        #instruction screen inits
        self.start_button_instructions = Button("Start", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT - 60), 150, 30, PURPLE, WHITE)
        #game over screen inits
        self.restart_button = Button("Restart", int(SCREENWIDTH/2 - 75), int(SCREENHEIGHT/2 + 30), 150, 30, PURPLE, WHITE)
        self.score = 0
        self.score_mode = ScoreMode.NORMAL
        self.eatfx = None
        self.fruit_instruction_dest = Rectangle(100, 0, SQUARE_SIZE * 2, SQUARE_SIZE * 2)
        self.key_image = None
        self.key_rect = None
        self.key_dest = Rectangle(90, 575, 50, 50)
        self.dev_mode = False

    def startup(self):
        self.snake.startup()
        self.food.startup()
        self.eatfx = load_sound(str(THIS_DIR) + "/resources/eat.wav")
        self.key_image = load_texture(str(THIS_DIR) + "/resources/key.jpg")
        self.key_rect = Rectangle(0.0, 0.0, float(self.key_image.width), float(self.key_image.height))
        self.key_dest.width = int(self.key_rect.width * 0.2)
        self.key_dest.height = int(self.key_rect.height * 0.2)

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
        match self.current_screen:
            case GameScreen.STARTUP:
                self.draw_startup()
            case GameScreen.INSTRUCTIONS:
                self.draw_instructions()
            case GameScreen.GAME:
                self.draw_game()
            case GameScreen.GAMEOVER:
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
            self.update_score()
            self.food.active = False
            self.food.move = False
            play_sound(self.eatfx)
            self.power_up(self.food.cur_sprite)
    
    def update_score(self):
        match self.score_mode:
            case ScoreMode.NORMAL:
                self.score += 10
            case ScoreMode.DOUBLE:
                self.score = int(self.score * 2)
                self.score_mode = ScoreMode.NORMAL
            case ScoreMode.HALF:
                self.score = int(self.score * 0.5)
                self.score_mode = ScoreMode.NORMAL

    def power_up(self, fruit_type):
        match fruit_type:
            case FruitType.APPLE:
                #so that eating the apple doesn't reset the snake speed if dev mode is on so the game can be played at slower speed for testing
                if not self.dev_mode:
                    self.snake.move_time = SNAKE_MOVE_TIME
            case FruitType.ORANGE:
                self.snake.move_time *= .99
            case FruitType.PEAR:
                self.score_mode = ScoreMode.DOUBLE
            case FruitType.STRAWBERRY:
                self.score_mode = ScoreMode.HALF

    #Update and draw functions by screen
    def draw_startup(self):
        draw_text("SNAKE", int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 60), 60, DARKPURPLE)
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
        for i, food in enumerate(self.food.sprites):
            self.fruit_instruction_dest.y = 100+i*75
            draw_texture_pro(food, self.food.frame_rec, self.fruit_instruction_dest, Vector2(0.0, 0.0), 0.0, RAYWHITE)
            draw_text(SPRITE_POWERS[i], 175, 125+i*75, 20, DARKGRAY)
        draw_texture_pro(self.key_image, self.key_rect, self.key_dest, Vector2(0.0, 0.0), 0.0, RAYWHITE)
        draw_text("Move", 200, 600, 20, DARKGRAY)
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

                self.food.update(self.snake.snake_position, self.snake.counterTail, self.dev_mode)

                self.eat_fruit()

            if is_key_pressed(KeyboardKey.KEY_D):
                self.dev_mode = not self.dev_mode
                print("switch dev")

            if self.dev_mode:
                if is_key_pressed(KeyboardKey.KEY_RIGHT_BRACKET):
                    self.snake.move_time *= .9
                if is_key_pressed(KeyboardKey.KEY_LEFT_BRACKET):
                    self.snake.move_time *= 1.1
    
    def draw_game(self):

        self.snake.draw()
        self.food.draw(self.dev_mode)

        if self.dev_mode:
            self.snake.draw_hit_box()
            self.food.draw_hit_box()
            draw_text("DEV MODE", 10, 10, 20, RED)
            draw_text("SNAKE SPEED: " + str(round(1/self.snake.move_time * SQUARE_SIZE, 2)), 10, 40, 20, RED)

        draw_text("SNAKE", int(SCREENWIDTH/2 - 100), 25, 50, DARKPURPLE)
        draw_text(str(self.score), int(SCREENWIDTH/3 * 2 - 25), 25, 50, DARKPURPLE)

        for i in range(SCREENWIDTH//SQUARE_SIZE + 1):
            draw_line_v(Vector2(i*SQUARE_SIZE + OFFSET.x/2, OFFSET.y/2 + OFFSET_TOP), Vector2(i*SQUARE_SIZE + OFFSET.x/2, SCREENHEIGHT - OFFSET.y/2), BROWN)

        for i in range((SCREENHEIGHT-OFFSET_TOP)//SQUARE_SIZE + 1):
            draw_line_v(Vector2(OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), Vector2(SCREENWIDTH - OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), BROWN)
        if self.pause:
            draw_text("PAUSED", int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 60), 60, DARKPURPLE)
    
    def update_gameover(self):
        if is_key_pressed(KeyboardKey.KEY_ENTER) or self.restart_button.is_clicked():
            self.__init__()
            self.startup()
            self.current_screen = GameScreen.GAME
    
    def draw_gameover(self):
        draw_text("GAME OVER", int(SCREENWIDTH/2 - 175), int(SCREENHEIGHT/2 - 60), 60, DARKPURPLE)
        self.restart_button.draw()
