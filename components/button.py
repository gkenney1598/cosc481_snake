from pyray import *
from settings import *

class Button():
    def __init__(self, text, x, y, width, height, color=GRAY, text_color=BLACK):
        self.text = text
        self.rect = Rectangle(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.font_size = 20

    def draw(self):
        draw_rectangle_rec(self.rect, self.color)
        center_x = SCREENWIDTH/2 - (len(self.text) * self.font_size / 4)
        draw_text(self.text, int(center_x), int(self.rect.y + 10), self.font_size, self.text_color)

    def is_clicked(self):
        mouse_pos = get_mouse_position()
        if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
            return check_collision_point_rec(mouse_pos, self.rect)