from pyray import Vector2
from pathlib import Path

SCREENWIDTH, SCREENHEIGHT = 850, 850
SNAKE_LENGTH, SQUARE_SIZE = 256, 40
OFFSET_TOP = 100
OFFSET = Vector2(SCREENWIDTH % SQUARE_SIZE, (SCREENHEIGHT-OFFSET_TOP) % SQUARE_SIZE)
SNAKE_SPEED = 1
SNAKE_MOVE_TIME = 1 / (SQUARE_SIZE / 4)
THIS_DIR = Path(__file__).resolve().parent
SPRITES = ['apple', 'lemon', 'orange', 'pear', 'strawberry', 'watermelon']
SPRITE_FRAMES = 2
SPRITE_POWERS = ["Reset Powerups", "Fruit moves", "Speed up snake", "2x Score", "0.5x Score", "Fruit Bigger"]