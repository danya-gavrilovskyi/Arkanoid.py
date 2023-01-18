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
    def __init__(self, x, y):
        self.radius = 15
        self.x = x
        self.y = y
        self.velocity_x = 400
        self.velocity_y = 400

    def move(self, dt):
        self.x += round(self.velocity_x * dt)
        self.y += round(self.velocity_y * dt)

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, 'red')

    def update(self, dt, paddle_x, paddle_y):
        self.move(dt)
        global previous_heart_x

        if (self.x >= WIDTH) or (self.x <=0):
            self.velocity_x *= -1
        if (self.y >= HEIGHT) or (self.y <=0):
            self.velocity_y *= -1

        if ((paddle_x + 200) >= self.x >= paddle_x) and (paddle_y <= (self.y+self.radius) <= (paddle_y + 35)):
            self.velocity_y *= -1

        if self.y >= HEIGHT:
            self.x = WIDTH // 2
            self.y = HEIGHT // 2
            if hearts:
                hearts.pop()
                previous_heart_x -= 35
            self.velocity_y *= -1

class Obstacle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def draw(self):
        rect = Rect(self.x, self.y, self.width, self.height)
        screen.draw.filled_rect(rect, 'lightblue')

    def hit(self, ball:Ball):
        if (self.x <= ball.x <= (self.x + self.width)) and (self.y <= (ball.y-ball.radius) <= (self.y + self.height)):
            return True

class HardObstacle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.hits = 0
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.color = 'darkblue'

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)

    def hit(self, ball:Ball):
        if (self.x <= ball.x <= (self.x + self.width)) and (self.y <= (ball.y-ball.radius) <= (self.y + self.height)):
            return True

class ExtraHeart():
    def __init__(self, actor:Actor):
        self.actor = actor
        self.velocity_y = 100

    def draw(self):
        self.actor.draw()

    def move(self, dt):
        self.actor.y += round(self.velocity_y * dt)

    def hit(self, paddle:Paddle):
        global previous_heart_x
        if (paddle.x <= self.actor.x <= paddle.x + paddle.width) and (paddle.y <= self.actor.y <= paddle.y + paddle.height):
            previous_heart_x += 35
            hearts.append(Actor('heart', (previous_heart_x, 20)))
            return True

    def update(self, dt):
        self.move(dt)

def draw():
    pass

WIDTH = 600
HEIGHT = 600

paddle_h = 35
paddle_w = 200
paddle = Paddle(WIDTH//2 - (paddle_w//2), HEIGHT - paddle_h, paddle_h, paddle_w)
ball = Ball(WIDTH // 2, HEIGHT//2)
previous_heart_x = 90

hearts = [Actor('heart', (20,20)), Actor('heart', (55,20)), Actor('heart', (90,20))]
obstacles = []
hard_obstacles = []
extrahearts = []

add_obstacles(hard_obstacles, 7, 'hard', [30, 50])
add_obstacles(obstacles, 6, 'default', [70, 80])
add_obstacles(obstacles, 7, 'default', [30, 110])

pgzrun.go()
