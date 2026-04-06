from pyray import *
from settings import * 
from enums import Screens, ScoreMode, FruitType
from components.Snake import Snake
from components.food import Food, FruitType

class GameScreen():
    def __init__(self):
        self.frames_counter = 0
        self.pause = False
        self.food = Food()
        self.snake = Snake()
        self.score_mode = ScoreMode.NORMAL
        self.eatfx = None
        self.dev_mode = False

    def startup(self):
        self.snake.startup()
        self.food.startup()
        self.eatfx = load_sound(str(THIS_DIR) + "/resources/eat.wav")

    def update(self, score):
        if is_key_pressed(KeyboardKey.KEY_P):
            self.pause = not self.pause

        if not self.pause:
            self.snake.update()
        
            if self.snake.self_collision():
                return Screens.GAMEOVER, score

            if self.wall_collision():
                return Screens.GAMEOVER, score

            self.food.update(self.snake.snake_position, self.snake.counterTail, self.dev_mode)

            score = self.eat_fruit(score)

        if is_key_pressed(KeyboardKey.KEY_D):
            self.dev_mode = not self.dev_mode

        if self.dev_mode:
            if is_key_pressed(KeyboardKey.KEY_RIGHT_BRACKET):
                self.snake.move_time *= .9
            if is_key_pressed(KeyboardKey.KEY_LEFT_BRACKET):
                self.snake.move_time *= 1.1
        
        return Screens.GAME, score

    def draw(self, score, high_score):
        if self.dev_mode:
            self.snake.draw_hit_box()
            self.food.draw_hit_box()
            draw_text("DEV MODE", 10, 10, SMALL_FONT_SIZE, RED)
            draw_text("SNAKE SPEED: " + str(round(1/self.snake.move_time * SQUARE_SIZE, 2)), 10, 40, SMALL_FONT_SIZE, RED)

        draw_text("SNAKE", int(SCREENWIDTH/2 - 100), 25, LARGE_FONT_SIZE, TEXT_COLOR)
        draw_text("SCORE: " + str(score), int(SCREENWIDTH - 200), 10, SMALL_FONT_SIZE, TEXT_COLOR)
        draw_text("HIGH SCORE: " + str(high_score), int(SCREENWIDTH - 200), 40, SMALL_FONT_SIZE, TEXT_COLOR)

        for i in range(SCREENWIDTH//SQUARE_SIZE + 1):
            draw_line_v(Vector2(i*SQUARE_SIZE + OFFSET.x/2, OFFSET.y/2 + OFFSET_TOP), Vector2(i*SQUARE_SIZE + OFFSET.x/2, SCREENHEIGHT - OFFSET.y/2), BROWN)

        for i in range((SCREENHEIGHT-OFFSET_TOP)//SQUARE_SIZE + 1):
            draw_line_v(Vector2(OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), Vector2(SCREENWIDTH - OFFSET.x/2, i*SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP), BROWN)

        self.snake.draw()
        self.food.draw(self.dev_mode)

        if self.pause:
            draw_text("PAUSED", int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 60), LARGE_FONT_SIZE, TEXT_COLOR)

    def shutdown(self):
        self.food.shutdown()
        unload_sound(self.eatfx)

    def wall_collision(self):
        if self.snake.snake[0].rect.x > SCREENWIDTH - OFFSET.x or self.snake.snake[0].rect.y > SCREENHEIGHT - OFFSET.y or self.snake.snake[0].rect.x < 0 or self.snake.snake[0].rect.y < OFFSET_TOP:
            return True
        
    def eat_fruit(self, score):
        if check_collision_recs(self.snake.snake[0].rect, self.food.rect):
            self.snake.snake[self.snake.counterTail].rect.x = self.snake.snake_position[self.snake.counterTail-1].x
            self.snake.snake[self.snake.counterTail].rect.y = self.snake.snake_position[self.snake.counterTail-1].y
            self.snake.counterTail += 1
            new_score = self.update_score(score)
            self.food.active = False
            self.food.move = False
            play_sound(self.eatfx)
            self.power_up(self.food.cur_sprite)
            return new_score
        return score

    def update_score(self, score):
        match self.score_mode:
            case ScoreMode.NORMAL:
                score += 10
            case ScoreMode.DOUBLE:
                score = int(score * 2)
                self.score_mode = ScoreMode.NORMAL
            case ScoreMode.HALF:
                score = int(score * 0.5)
                self.score_mode = ScoreMode.NORMAL
        return score

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
