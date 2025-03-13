import pygame
import random

max_x = 500
max_y = 500

def test(o):
    t = 10
    o  = 10

o = 5
test(o)
print(o)

def demo_2(x, y, *, test_one, test_two):
    pass

demo_2(3, 5, test_two=4, test_one=10)

class Shape:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

    def bounce_if_needed(self, xl, yt, xr, yb):
        if self.x > xr or self.x <= xl:
            self.dx = -self.dx

        if self.y > yb or self.y <= yt:
            self.dy = -self.dy

    def move(self):
        self.x += self.dx
        self.y += self.dy


class Circle(Shape):
    def __init__(self, x, y, dx, dy, color, radius):
        Shape.__init__(self, x, y, dx, dy, color)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Square(Shape):
    def __init__(self, x, y, dx, dy, color, edge_length):
        Shape.__init__(self, x, y, dx, dy, color)
        self.edge_length = edge_length

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.edge_length, self.edge_length))


N = 10
avail_colors = ["red", "green", "blue"]
shapes = []
for i in range(int(N/2)):
    col = random.randint(0, len(avail_colors) - 1)
    rad = random.randint(10, 30)
    speed_x = random.randint(-2, 2)
    speed_y = random.randint(-2, 2)
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    shapes.append(Circle(x, y, speed_x, speed_y, avail_colors[col], rad))

for i in range(N - int(N/2)):
    col = random.randint(0, len(avail_colors) - 1)
    edge_len = random.randint(10, 30)
    speed_x = random.randint(-2, 2)
    speed_y = random.randint(-2, 2)
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)

    shapes.append(Square(x, y, speed_x, speed_y, avail_colors[col], edge_len))

# pygame setup
pygame.init()
screen = pygame.display.set_mode((max_x, max_y))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    for shape in shapes:
        shape.draw(screen)
        # pygame.draw.circle(screen, shape.color, (shape.x, shape.y), shape.radius)
        shape.move()
        shape.bounce_if_needed(0, 0, max_x, max_y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
