import time
import sys
import math
import random
import pygame
import operator
from pygame import gfxdraw

window_width = 800
window_hight = 600


G = 6.674e-7
critical_mass = 12e12


class Circle:
    """
    A circle is an element that can travel around.
    """

    def __init__(self, x, y, mass, velocity_x=0, velocity_y=0, RGB=(255, 0, 0)):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.RGB = RGB
        self.deletable = True
    
    
    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def get_radius(self):
        return (((self.mass * (3 / 4)) / math.pi) ** (1 / 3)) * 10 ** -3

    def vel(self):
        return math.sqrt((self.velocity_x ** 2) + (self.velocity_y ** 2))

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __repr__(self):
        return "Circle(x = {}, y = {}, mass = {}e10, vel = {}, color = {})".format(
            round(self.x, 2),
            round(self.y, 2),
            int(self.mass) / 10e10,
            round(self.vel(), 2),
            self.RGB,
        )

    def draw(self):
        pygame.gfxdraw.filled_circle(
                            gamedisplay,
                            round(self.x),
                            round(self.y),
                            round(self.get_radius()),
                            self.RGB,
                        )


def get_color():
    col = tuple(random.randint(0, 255) for i in range(3))
    if col == (30, 30, 30):
        return get_color()
    else:
        return col


circle = []
circle2 = [
    Circle(x=200, y=500, mass=10e10, velocity_x=0, velocity_y=0, RGB=get_color()),
    Circle(window_width / 2 + 1, window_hight / 2 + 1, 20e10, RGB=get_color()),
    Circle(751, 50, 40e10, RGB=get_color()),
    Circle(205, 100, 40e10, 0, RGB=get_color()),
]

divider = 50
fun_mass = (critical_mass) / ((window_width / divider) * (window_hight / divider))

def new_balls():
    for x in range(window_width // divider):
        for y in range(window_hight // divider):
            circle.append(
                Circle(
                    (x * divider) + (divider / 2),
                    (y * divider) + (divider / 2),
                    fun_mass,
                    RGB=get_color(),
                )
            )

try:
    if sys.argv[1] == "s":
        new_balls()
except:
    pass


def color_picker(a, b):
    color1 = tuple([a.mass * x for x in a.RGB])
    color2 = tuple([b.mass * x for x in b.RGB])
    ab = tuple(map(operator.add, color1, color2))
    abb = tuple([round(x / (a.mass + b.mass)) for x in ab])
    return abb

def ball_in_circle(biggest):
    #print(biggest.x)
    this_mass = 10e10
    distance = 100
    force2 = G * ((biggest.mass * this_mass) / distance**2)
    speed = (math.sqrt((force2 * distance) / (biggest.mass + this_mass)))
    biggest.velocity_x -= speed / biggest.mass
    fartlist = [speed, -speed]
    circle.append(
                Circle(
                    biggest.x,
                    biggest.y - distance,
                    10e10,
                    velocity_x= random.choice(fartlist) * 0.03,
                    RGB=get_color(),
                )
            )

pygame.init()
gamedisplay = pygame.display.set_mode((window_width, window_hight))
pygame.display.set_caption("Vindu!")

print(len(circle))
max_mass = 0
crashed = False
max_vel = 0
rounds = 0
while not crashed:
    rounds += 1
    k1 = len(circle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            circle.append(
                Circle(
                    random.randint(0, window_width),
                    random.randint(0, window_hight),
                    10e10,
                    RGB=get_color(),
                )
            )
        if keys[pygame.K_LEFT]:
            circle.append(
                Circle(
                    random.randint(0, window_width),
                    random.randint(0, window_hight),
                    10e10,
                    velocity_x=-0.15,
                    RGB=get_color(),
                )
            )
        if keys[pygame.K_RIGHT]:
            circle.append(
                Circle(
                    random.randint(0, window_width),
                    random.randint(0, window_hight),
                    10e10,
                    velocity_x=0.15,
                    RGB=get_color(),
                )
            )
        if keys[pygame.K_t]:
            print("New!")
            for x in circle:
                print(x)

        if keys[pygame.K_j]:
            circle = []

        pos_x, pos_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            times = time.time()

        if keys[pygame.K_r]:
            max_mass2 = 0
            for c in circle:
                if c.mass > max_mass2:
                    max_mass2 = c.mass
            for c in circle:
                if c.mass == max_mass2:
                    ball_in_circle(c)
                   

        if keys[pygame.K_s]:
            new_balls()

        if event.type == pygame.MOUSEBUTTONUP:
            size = time.time() - times
            circle.append(
                Circle(pos_x, pos_y, max(size * 15 ** 10, 10e2), RGB=get_color())
            )
            print(size)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        circle.append(
            Circle(
                random.randint(0, window_width),
                random.randint(0, window_hight),
                10e10,
                velocity_x=random.uniform(-0.25, 0.25),
                RGB=get_color(),
            )
        )
    if keys[pygame.K_UP]:
        circle.append(
            Circle(
                random.randint(0, window_width),
                random.randint(0, window_hight),
                10e10,
                RGB=get_color(),
            )
        )

    pygame.display.update()
    gamedisplay.fill((30, 30, 30))

    listen = circle[:]

    for c in circle:
        c.x += c.velocity_x
        c.y += c.velocity_y

    for c in circle:
        c.draw()
        if c.x < -10000 or c.x > 10000:
            circle.remove(c)
        elif c.y < -10000 or c.y > 10000:
            circle.remove(c)
        listen.remove(c)

        for d in listen:
            dist = max(c.distance(d), 0.0000001)
            force = G * (c.mass * d.mass / dist ** 2)
            acceleration_c = 0.03 * (force / c.mass)
            acceleration_d = 0.03 * (force / d.mass)
            diff_x, diff_y = c - d
            c.velocity_x -= acceleration_c * diff_x / dist * 0.003
            c.velocity_y -= acceleration_c * diff_y / dist * 0.003
            d.velocity_x += acceleration_d * diff_x / dist * 0.003
            d.velocity_y += acceleration_d * diff_y / dist * 0.003

            if dist < c.get_radius() + d.get_radius():
                new_mass = c.mass + d.mass
                c.x = (c.mass * c.x + d.mass * d.x) / (c.mass + d.mass)
                c.y = (c.mass * c.y + d.mass * d.y) / (c.mass + d.mass)
                c.velocity_x = (c.velocity_x * c.mass + d.velocity_x * d.mass) / (
                    c.mass + d.mass
                )
                c.velocity_y = (c.velocity_y * c.mass + d.velocity_y * d.mass) / (
                    c.mass + d.mass
                )
                c.RGB = color_picker(c, d)
                c.mass = new_mass
                circle.remove(d)
                listen.remove(d)
                if new_mass > critical_mass:
                    if c in circle:
                        f = open("demofile2.txt", "a")
                        f.write("{}\n".format(c.RGB))
                        f.close()
                        circle.remove(c)
                    assert c not in listen
                max_vel = 0

        vel = c.vel()

        if vel > max_vel:
            max_vel = vel

    k2 = len(circle)
    if k1 != k2:
        print(len(circle), max_vel)
    max_vel = 0
