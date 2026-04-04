from pyray import *
from settings import *
import random
from enums import FruitType

class Food():
    def __init__(self, ):
        self.rect = Rectangle(0, 0, SQUARE_SIZE, SQUARE_SIZE)
        self.color = RED
        self.active = False
        self.sprite_texture = None
        self.sprites = []
        self.frame_rec = None
        self.texture_timer = 0
        self.texture_switch = 1 / (SQUARE_SIZE / 6)
        self.move = False
        self.move_timer = 0
        self.speed = 1 / (SQUARE_SIZE / 20)
        self.cur_sprite = None
        self.hit_box = Rectangle(0, 0, SQUARE_SIZE, SQUARE_SIZE)

    def startup(self):
        for sprite in SPRITES:
            self.sprites.append(load_texture(str(THIS_DIR) + "/resources/cute_" + sprite + "_run.png"))

        self.frame_rec = Rectangle(0.0, 0.0, float(self.sprites[0].width)/SPRITE_FRAMES, float(self.sprites[0].height))

    def update(self, snake, counterTail, dev_mode):
        self.texture_timer += get_frame_time()

        if self.texture_timer >= self.texture_switch:
            self.frame_rec.x = float(self.sprite_texture.width)/SPRITE_FRAMES
        if self.texture_timer >= self.texture_switch * 2:
            self.frame_rec.x = 0
            self.texture_timer = 0
        if not self.active:
            self.active = True
            if self.cur_sprite is FruitType.WATERMELON: #make sure watermelon doesn't spawn half off the map
                max_x = int(SCREENWIDTH/SQUARE_SIZE - 3)
                max_y = int((SCREENHEIGHT-OFFSET_TOP)/SQUARE_SIZE - 3)
            else:
                max_x = int(SCREENWIDTH/SQUARE_SIZE - 1)
                max_y = int((SCREENHEIGHT-OFFSET_TOP)/SQUARE_SIZE - 1)
            self.rect.x = get_random_value(0, max_x) * SQUARE_SIZE + OFFSET.x/2
            self.rect.y = get_random_value(0, max_y) * SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP
            
            for i in range(MAX_PLACEMENT_TRIES):
                if self.in_tail(self.rect.x, self.rect.y, snake, counterTail):
                    self.rect.x = get_random_value(0, max_x) * SQUARE_SIZE + OFFSET.x/2
                    self.rect.y = get_random_value(0, max_y) * SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP
                else:
                    break
            
            self.hit_box.x = self.rect.x
            self.hit_box.y = self.rect.y
            
            if not dev_mode:
                self.rand_sprite()
            
            self.power_up()
        
        if self.active and self.move:
            self.move_fruit(snake, counterTail)

        if dev_mode:
            self.set_sprite()

    def in_tail(self, x, y, snake, counterTail):
        for i in range(counterTail):
            if x == snake[i].x and y == snake[i].y:
                return True
        return False
    
    def power_up(self):
        match self.cur_sprite:
            case FruitType.LEMON:
                self.move = True
                self.rect.width = SQUARE_SIZE
                self.rect.height = SQUARE_SIZE
                self.hit_box.width = self.rect.width
                self.hit_box.height = self.rect.height
            case FruitType.WATERMELON:
                self.move = False
                self.rect.width = SQUARE_SIZE * 2
                self.rect.height = SQUARE_SIZE * 2
                self.hit_box.width = self.rect.width
                self.hit_box.height = self.rect.height
            case _:
                self.move = False
                self.rect.width = SQUARE_SIZE
                self.rect.height = SQUARE_SIZE
                self.hit_box.width = self.rect.width
                self.hit_box.height = self.rect.height
    
    def move_fruit(self, snake, counterTail):
        self.move_timer += get_frame_time()
        if self.move_timer >= self.speed:
            self.move_timer = 0
            directions = self.get_valid_directions()
            rand_direction = random.choice(directions)
            for i in range(MAX_PLACEMENT_TRIES):
                if self.in_tail(self.rect.x + rand_direction.x * SQUARE_SIZE, self.rect.y + rand_direction.y * SQUARE_SIZE, snake, counterTail):
                    rand_direction = random.choice(directions)
                else:
                    break
            self.rect.x += rand_direction.x * SQUARE_SIZE
            self.rect.y += rand_direction.y * SQUARE_SIZE

            self.hit_box.x = self.rect.x
            self.hit_box.y = self.rect.y

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
        self.cur_sprite = rand_sprite
        self.sprite_texture = self.sprites[rand_sprite]

    def set_sprite(self):
        if is_key_pressed(KeyboardKey.KEY_ONE):
            self.sprite_texture = self.sprites[FruitType.APPLE]
            self.cur_sprite = FruitType.APPLE
        if is_key_pressed(KeyboardKey.KEY_TWO):
            self.sprite_texture = self.sprites[FruitType.LEMON]
            self.cur_sprite = FruitType.LEMON
        if is_key_pressed(KeyboardKey.KEY_THREE):
            self.sprite_texture = self.sprites[FruitType.ORANGE]
            self.cur_sprite = FruitType.ORANGE
        if is_key_pressed(KeyboardKey.KEY_FOUR):
            self.sprite_texture = self.sprites[FruitType.PEAR]
            self.cur_sprite = FruitType.PEAR
        if is_key_pressed(KeyboardKey.KEY_FIVE):
            self.sprite_texture = self.sprites[FruitType.STRAWBERRY]
            self.cur_sprite = FruitType.STRAWBERRY
        if is_key_pressed(KeyboardKey.KEY_SIX):
            self.sprite_texture = self.sprites[FruitType.WATERMELON]
            self.cur_sprite = FruitType.WATERMELON
        if is_key_pressed(KeyboardKey.KEY_SEVEN):
            self.rand_sprite()

    def draw(self, dev_mode):
        if self.sprite_texture is None:
            self.rand_sprite()
        draw_texture_pro(self.sprite_texture, self.frame_rec, self.rect, Vector2(0.0, 0.0), 0.0, RAYWHITE)

    def draw_hit_box(self):
        draw_rectangle_lines_ex(self.hit_box, 2, RED)

    def shutdown(self):
        for sprite in self.sprites:
            unload_texture(sprite)