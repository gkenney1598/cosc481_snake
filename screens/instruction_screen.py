from pyray import *
from settings import *
from components.button import Button
from enums import Screens
from components.food import Food

class InstructionScreen():
    def __init__(self):
        self.start_button = Button("Start", BUTTON_X, int(SCREENHEIGHT - 60), BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, WHITE)
        self.fruit_instruction_dest = Rectangle(100, 0, SQUARE_SIZE * 2, SQUARE_SIZE * 2)
        self.key_image = None
        self.key_rect = None
        self.key_dest = Rectangle(90, 575, 50, 50)
        self.fruit = Food()

    def startup(self):
        self.key_image = load_texture(str(THIS_DIR) + "/resources/key.jpg")
        self.key_rect = Rectangle(0.0, 0.0, float(self.key_image.width), float(self.key_image.height))
        self.key_dest.width = int(self.key_rect.width * KEY_PNG_SCALE)
        self.key_dest.height = int(self.key_rect.height * KEY_PNG_SCALE)
        self.fruit.startup()
    
    def update(self):
        if self.start_button.is_clicked():
            return Screens.GAME
        return Screens.INSTRUCTIONS

    def draw(self):
        for i, food in enumerate(self.fruit.sprites):
            self.fruit_instruction_dest.y = 100+i*75
            draw_texture_pro(food, self.fruit.frame_rec, self.fruit_instruction_dest, Vector2(0.0, 0.0), 0.0, BACKGROUND_COLOR)
            draw_text(SPRITE_POWERS[i], 175, 125+i*75, SMALL_FONT_SIZE, DARKGRAY)
        draw_texture_pro(self.key_image, self.key_rect, self.key_dest, Vector2(0.0, 0.0), 0.0, BACKGROUND_COLOR)
        draw_text("Move", 200, 600, SMALL_FONT_SIZE, DARKGRAY)
        self.start_button.draw()

    def shutdown(self):
        unload_texture(self.key_image)
        for i in range(len(self.fruit.sprites)):
            unload_texture(self.fruit.sprites[i])