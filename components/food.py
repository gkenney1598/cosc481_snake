from pyray import *
from settings import *
import random

class Food():
    def __init__(self, ):
        self.rect = Rectangle(0, 0, SQUARE_SIZE * SPRITE_SCALE, SQUARE_SIZE * SPRITE_SCALE)
        self.color = RED
        self.active = False
        self.sprite = None
        self.sprites = []
        self.frame_rec = None
        self.texture_timer = 0
        self.texture_switch = 1 / (SQUARE_SIZE / 6)
        self.fruit_move_feature = False
        self.move = False
        self.move_timer = 0
        self.speed = 1 / (SQUARE_SIZE / 20)

    def startup(self):
        for sprite in SPRITES:
            self.sprites.append(load_texture(str(THIS_DIR) + "/resources/cute_" + sprite + "_run.png"))

        self.frame_rec = Rectangle(0.0, 0.0, float(self.sprites[0].width)/SPRITE_FRAMES, float(self.sprites[0].height))

    def update(self, snake, counterTail):
        self.texture_timer += get_frame_time()

        if is_key_pressed(KeyboardKey.KEY_M):
            self.fruit_move_feature = not self.fruit_move_feature

        if self.texture_timer >= self.texture_switch:
            self.frame_rec.x = float(self.sprite.width)/SPRITE_FRAMES
        if self.texture_timer >= self.texture_switch * 2:
            self.frame_rec.x = 0
            self.texture_timer = 0
        if not self.active:
            self.active = True
            self.rect.x = get_random_value(0, int(SCREENWIDTH/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.x/2
            self.rect.y = get_random_value(0, int((SCREENHEIGHT-OFFSET_TOP)/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP
            
            while self.in_tail(self.rect.x, self.rect.y, snake, counterTail):
                self.rect.x = get_random_value(0, int(SCREENWIDTH/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.x/2
                self.rect.y = get_random_value(0, int(SCREENHEIGHT/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP
            
            self.rand_sprite()

            if self.fruit_move_feature: self.move = True

        if self.fruit_move_feature and self.move:
            self.move_timer += get_frame_time()
            if self.move_timer >= self.speed:
                self.move_timer = 0
                directions = self.get_valid_directions()
                rand_direction = random.choice(directions)
                if self.in_tail(self.rect.x + rand_direction.x * SQUARE_SIZE, self.rect.y + rand_direction.y * SQUARE_SIZE, snake, counterTail):
                    rand_direction = random.choice(directions)
                self.rect.x += rand_direction.x * SQUARE_SIZE
                self.rect.y += rand_direction.y * SQUARE_SIZE

    def in_tail(self, x, y, snake, counterTail):
        for i in range(counterTail):
            if x == snake[i].x and y == snake[i].y:
                return True
        return False

    #used for fruit move
    def get_valid_directions(self):
        directions = []
        if self.rect.x + SQUARE_SIZE * 2 < SCREENWIDTH - OFFSET.x: #can move right
            directions.append(Vector2(1, 0))
        if self.rect.x - SQUARE_SIZE * 2 > 0: #can move left
            directions.append(Vector2(-1, 0))
        if self.rect.y + SQUARE_SIZE * 2 < SCREENHEIGHT - OFFSET.y: #can move down
            directions.append(Vector2(0, 1))
        if self.rect.y - SQUARE_SIZE * 2 > OFFSET_TOP: #can move up
            directions.append(Vector2(0, -1))
        return directions

    def rand_sprite(self):
        rand_sprite = get_random_value(0, len(self.sprites) - 1)
        self.sprite = self.sprites[rand_sprite]

    def draw(self):
        if self.sprite is None: #when restarting game, bug with reloading sprites
            self.rand_sprite()
        draw_texture_pro(self.sprite, self.frame_rec, self.rect, Vector2(0.0, 0.0), 0.0, RAYWHITE)

    def shutdown(self):
        for sprite in self.sprites:
            unload_texture(sprite)