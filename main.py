import pgzrun
import random
import time
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

    def update(self, dt, paddle_x, paddle_y, paddle_width):
        self.move(dt)
        global previous_heart_x

        if (self.x >= WIDTH) or (self.x <=0):
            self.velocity_x *= -1
        if (self.y >= HEIGHT) or (self.y <=0):
            self.velocity_y *= -1

        if ((paddle_x + paddle_width) >= self.x >= paddle_x) and (paddle_y <= (self.y+self.radius) <= (paddle_y + 35)):
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

class BonusPaddleWidth():
    def __init__(self, actor:Actor):
        self.actor = actor
        self.velocity_y = 100

    def draw(self):
        self.actor.draw()

    def move(self, dt):
        self.actor.y += round(self.velocity_y * dt)

    def hit(self, paddle:Paddle):
        if (paddle.x <= self.actor.x <= paddle.x + paddle.width) and (paddle.y <= self.actor.y <= paddle.y + paddle.height):
            return True

    def update(self, dt):
        self.move(dt)

def draw():
    screen.clear()
    screen.fill(('#B39F61'))
    if hearts and (obstacles or hard_obstacles):
        paddle.draw()
        ball.draw()
        for obstacle in obstacles:
            if obstacle.hit(ball):
                ball.velocity_y *= -1
                obstacles.remove(obstacle)
            obstacle.draw()

        for obstacle in hard_obstacles:
            if obstacle.hit(ball):
                obstacle.hits += 1
                obstacle.color = 'lightblue'
                if obstacle.hits == 2:
                    hard_obstacles.remove(obstacle)
                ball.velocity_y *= -1
            obstacle.draw()

        for heart in hearts:
            heart.draw()

        for extraheart in extrahearts:
            extraheart.draw()

        for item in extra_paddle_width_items:
            item.draw()

    elif not hearts:
        screen.draw.text('You lose !!!', (210, 250), color='black', fontsize=50)
    elif not obstacles and not hard_obstacles:
        screen.draw.text('You win !!!', (210, 250), color='black', fontsize=50)

def update(dt):
    global previous_heart_x, start_time
    ball.update(dt, paddle.x, paddle.y, paddle.width) 
    if 0.051 > random.random() > 0.05:
        extrahearts.append(ExtraHeart(Actor('bonusheart', (random.randint(0, WIDTH), 15))))

    if 0.061 > random.random() > 0.06:
        extra_paddle_width_items.append(BonusPaddleWidth(Actor('bonus_item', (random.randint(0, WIDTH), 15))))

    for extraheart in extrahearts:
        extraheart.update(dt)
        extraheart.draw()
        if extraheart.hit(paddle):
            extrahearts.remove(extraheart)

    for item in extra_paddle_width_items:
        item.update(dt)
        item.draw()
        if item.hit(paddle):
            start_time = time.time()
            extra_paddle_width_items.remove(item)
            paddle.width = 300

    if time.time() >= start_time+10:
        paddle.width = 200

def on_mouse_move(pos):
    x = pos[0] - (paddle_w // 2)
    paddle.x = x

def add_obstacles(obstacles: list, number_of_obstacles: int, type_of_obstacles: str, start_coords: list):
    obst_count = 0
    x = start_coords[0]
    y = start_coords[1]
    if type_of_obstacles == 'hard':
        while obst_count < number_of_obstacles:
            obstacles.append(HardObstacle(x, y, 50, 20))
            obst_count+=1
            x+= 80
    else:
        while obst_count < number_of_obstacles:
            obstacles.append(Obstacle(x, y, 50, 20))
            obst_count+=1
            x+= 80

WIDTH = 600
HEIGHT = 600

paddle_h = 35
paddle_w = 200
paddle = Paddle(WIDTH//2 - (paddle_w//2), HEIGHT - paddle_h, paddle_h, paddle_w)
ball = Ball(WIDTH // 2, HEIGHT//2)
previous_heart_x = 90
start_time = 0

hearts = [Actor('heart', (20,20)), Actor('heart', (55,20)), Actor('heart', (90,20))]
obstacles = []
hard_obstacles = []
extrahearts = []
extra_paddle_width_items = []

add_obstacles(hard_obstacles, 7, 'hard', [30, 50])
add_obstacles(obstacles, 6, 'default', [70, 80])
add_obstacles(obstacles, 7, 'default', [30, 110])

pgzrun.go()
