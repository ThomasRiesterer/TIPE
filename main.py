####################################################
# Imports

import pygame
import time
from math import *
from random import *


####################################################
# Classes and functions

class Circle:
    def __init__(self, default_x, default_y, radius):
        self.x = default_x
        self.y = default_y
        self.vx = 0
        self.vy = 0
        self.radius = radius

    def render_tick(self):
        pygame.draw.circle(screen, white, (self.x, self.y), self.radius/2, self.radius) 
        self.movement()
        self.x += self.vx
        self.y += self.vy

    def movement(self):
        self.vx = 0
        self.vy = 0
        collisions, n = calc_collisions(self)

        collide(self)

        if self.vx == 0 and self.vy == 0:
            dx = goal[0] - self.x
            dy = goal[1] - self.y
            self.vx = (dx / (abs(dx) + abs(dy))) *speed
            self.vy = (dy / (abs(dx) + abs(dy))) *speed
            for c in collisions:
                self.vx += c.vx
                self.vy += c.vy
            self.vx /= n
            self.vy /= n
            for c in collisions:
                if not(self.x == c.x):
                    self.vx += 1/(self.x - c.x) *coeff
                if not(self.y == c.y):
                    self.vy += 1/(self.y - c.y) *coeff

        self.vx /= n
        self.vy /= n


class Wall:
    def __init__(self, start_x, start_y, end_x, end_y, group):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        if self.start[0] == self.end[0] :
            self.orientation = 'V' # Vertical
        elif self.start[1] == self.end[1] :
            self.orientation = 'H' # Horizontal
        else :
            self.orientation = 'D' # Diagonal
        self.group = group
    
    def render_tick(self):
        pygame.draw.line(screen, white, self.start, self.end)


def on_goal(circle):
    return abs(circle.x - goal[0]) <= 40 and abs(circle.y - goal[1]) <= 20

def calc_collisions(circle):
    collisions = []
    for c in circles:
        if c == circle:
            continue
        diff = sqrt((c.x - circle.x)**2 + (c.y - circle.y)**2)
        dist = diff - (c.radius + circle.radius)
        if dist < 0:
            collisions.append(c)
    n = 1+len(collisions)/3
    return collisions, n

def wall_colliding_V(circle):
    colliding = False
    for w in walls:
        if w.orientation == 'H':
            continue
        if (w.start[0] - circle.radius < circle.x and circle.x < w.end[0] + circle.radius):
            if (w.start[1] < circle.y and circle.y < w.end[1]):
                colliding = True
                break
    return colliding

def wall_colliding_H(circle):
    colliding = False
    wall_group = 0
    for w in walls:
        if w.orientation == 'V':
            continue
        if (w.start[1] - circle.radius < circle.y and circle.y < w.end[1] + circle.radius):
            if (w.start[0] < circle.x and circle.x < w.end[0]):
                colliding = True
                wall_group = w.group
                break
    return colliding, wall_group

def wall_colliding_D(circle):
    colliding = False
    for w in walls:
        if (w.start[0] < circle.x - circle.radius and circle.x + circle.radius < w.end[0]) or (w.end[0] < circle.x - circle.radius and circle.x + circle.radius < w.start[0]):
            if (w.start[1] < circle.y - circle.radius and circle.y + circle.radius < w.end[1]) or (w.end[1] < circle.y - circle.radius and circle.y + circle.radius < w.start[1]):
                colliding = True
                break
    return colliding

def collide(circle):
    colliding_H, colliding_group_H = wall_colliding_H(circle)
    colliding_V = wall_colliding_V(circle)
    colliding_D = wall_colliding_D(circle)
    if colliding_H and colliding_group_H == 0:
        if circle.x < goal[0]:
            circle.vx = speed
            circle.vy = 0
        else:
            circle.vx = -speed
            circle.vy = 0
    elif colliding_V:
        circle.vx = 0
        circle.vy = -speed
    elif colliding_D:
        normalized_speed = sqrt(circle.vx ** 2 + circle.vy ** 2)
        if circle.x < goal[0]:
            circle.vx = -normalized_speed
            circle.vy = -normalized_speed
        else:
            circle.vx = normalized_speed
            circle.vy = -normalized_speed


####################################################
# Initialisation

screen_res = (1280,720)
goal = (640,50)

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

radius = 18
speed = 1
coeff = 1.7

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("TIPE : bousculades")
screen.fill(black)

finished = 0
initial_time = time.time()


####################################################
# Main run body

nb = 50
circles = []
for i in range(nb):
#    circles.append(Circle(randint(120,1160), randint(80,640), radius))
#    circles.append(Circle(randint(400,880), randint(250,500), radius))
    circles.append(Circle(randint(520,760), randint(250,500), radius))    

walls = []
                                         # Object0
walls.append(Wall(100,60,100,660,0))     # Left_Vertical
walls.append(Wall(1180,60,1180,660,0))   # Right_Vertical
walls.append(Wall(100,60,610,60,0))      # TopRight_Horizontal
walls.append(Wall(670,60,1180,60,0))     # TopLeft_Horizontal
walls.append(Wall(100,660,1180,660,0))   # Bottom_Horizontal

o1_size = 40                             # Object1
o1_cH = 640
o1_cV = 150
#walls.append(Wall(o1_cH-o1_size,o1_cV,o1_cH,o1_cV-o1_size,1))
#walls.append(Wall(o1_cH,o1_cV-o1_size,o1_cH+o1_size,o1_cV,1))
#walls.append(Wall(o1_cH+o1_size,o1_cV,o1_cH,o1_cV+o1_size,1))
#walls.append(Wall(o1_cH,o1_cV+o1_size,o1_cH-o1_size,o1_cV,1))


run = True
while run:
    screen.fill(black)

    for c in circles:
        c.render_tick()

    for w in walls:
        w.render_tick()

    circles_new = []
    for c in circles:
        if not(on_goal(c)):
            circles_new.append(c)
    circles = circles_new
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False

    if circles == [] and finished == 0:
        print("temps d'évacuation : ", time.time() - initial_time, "secondes")
        finished = 1

    pygame.display.update()
    clock.tick(80)

pygame.quit()
