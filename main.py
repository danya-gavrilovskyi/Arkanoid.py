import pgzrun
import random
from pgzero.actor import Actor

class Paddle():
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def draw(self):
        rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(rect, 'black')

class Ball():
    pass

class Obstacle():
    pass

def draw():
    pass

WIDTH = 600
HEIGHT = 600

paddle_h = 35
paddle_w = 200
paddle = Paddle(WIDTH//2 - (paddle_w//2), HEIGHT - paddle_h, paddle_h, paddle_w)

pgzrun.go()
