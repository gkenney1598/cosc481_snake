from pyray import *
from settings import *

class Food():
    def __init__(self, ):
        self.rect = Rectangle(0, 0, SQUARE_SIZE * SPRITE_SCALE, SQUARE_SIZE * SPRITE_SCALE)
        self.color = RED
        self.active = False
        self.sprite = None
        self.sprites = []
        self.frame_rec = None
        self.frames_counter = 0

    def startup(self):
        for sprite in SPRITES:
            self.sprites.append(load_texture(str(THIS_DIR) + "/resources/cute_" + sprite + "_run.png"))

        self.frame_rec = Rectangle(0.0, 0.0, float(self.sprites[0].width)/SPRITE_FRAMES, float(self.sprites[0].height))

    def update(self, snake, counterTail):
        self.frames_counter += 1

        if self.frames_counter == 15:
            self.frame_rec.x = float(self.sprite.width)/SPRITE_FRAMES
        if self.frames_counter == 30:
            self.frame_rec.x = 0
            self.frames_counter = 0
        if not self.active:
            self.active = True
            self.rect.x = get_random_value(0, int(SCREENWIDTH/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.x/2
            self.rect.y = get_random_value(0, int((SCREENHEIGHT-OFFSET_TOP)/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.y/2 + OFFSET_TOP
            
            #have to do comparison with x and y values, doing vectors doesnt work
            for i in range(counterTail):
                if self.rect.x == snake[i].x and self.rect.y == snake[i].y:
                    self.rect.x = get_random_value(0, int(SCREENWIDTH/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.x/2
                    self.rect.y = get_random_value(0, int(SCREENHEIGHT/SQUARE_SIZE - 1)) * SQUARE_SIZE + OFFSET.y/2
            
            self.rand_sprite()
            
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