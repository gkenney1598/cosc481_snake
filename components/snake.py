from pyray import *
from settings import *

class Snake():
    def __init__(self):
        self.snake = []
        self.snake_position = [Vector2(0,0)] * SNAKE_LENGTH
        self.allow_move = False
        self.counterTail = 1
        self.frames_counter = 0
    
    def startup(self):
        for i in range(SNAKE_LENGTH):
            self.snake_position[i] = Vector2(0, 0)
            self.snake.append(SnakeBlock(RED if i == 0 else DARKGREEN))

    def update(self):
        if self.allow_move:
            if is_key_pressed(KeyboardKey.KEY_RIGHT) and self.snake[0].speed.x == 0:
                self.snake[0].speed = Vector2(SNAKE_SPEED, 0)
                self.allow_move = False
            if is_key_pressed(KeyboardKey.KEY_LEFT) and self.snake[0].speed.x == 0:
                self.snake[0].speed = Vector2(-SNAKE_SPEED, 0)
                self.allow_move = False
            if is_key_pressed(KeyboardKey.KEY_UP) and self.snake[0].speed.y == 0:
                self.snake[0].speed = Vector2(0, -SNAKE_SPEED)
                self.allow_move = False
            if is_key_pressed(KeyboardKey.KEY_DOWN) and self.snake[0].speed.y == 0:
                self.snake[0].speed = Vector2(0, SNAKE_SPEED)
                self.allow_move = False
        
        for i in range(self.counterTail):
            self.snake_position[i] = Vector2(self.snake[i].rect.x, self.snake[i].rect.y)
        
        #this is what allows for the blocky movement of snake
        if self.frames_counter%5 == 0: 
            self.snake[0].update()
            self.allow_move = True

            for i in range(1, self.counterTail):
                self.snake[i].update(self.snake_position[i-1])

        self.frames_counter += 1
        if self.frames_counter >= 255: #stop from overflow
            self.frames_counter = 0

    def draw(self):
        for i in range(self.counterTail):
            self.snake[i].draw()

    def self_collision(self):
        for i in range(1, self.counterTail):
            if self.snake[0].rect.x == self.snake[i].rect.x and self.snake[0].rect.y == self.snake[i].rect.y:
                return True

class SnakeBlock():
    def __init__(self, col):
        self.rounded = 50
        self.segments = 5
        self.speed = Vector2(SNAKE_SPEED, 0)
        self.color = col
        self.rect = Rectangle(OFFSET.x/2, OFFSET.y/2 + OFFSET_TOP, SQUARE_SIZE, SQUARE_SIZE)

    def update(self, new_pos=None):
        #get_frame_time makes movements not in the boxes, so not included
        if new_pos is not None:
            self.rect.x = new_pos.x
            self.rect.y = new_pos.y
        else:
            self.rect.x += self.speed.x * SQUARE_SIZE
            self.rect.y += self.speed.y * SQUARE_SIZE

    def draw(self):
        draw_rectangle_rounded(self.rect, self.rounded, self.segments, self.color)
