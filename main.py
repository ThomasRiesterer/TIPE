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

    def on_goal(self):
        return abs(self.x - goal[0]) <= 15 and abs(self.y - goal[1]) <= 15

    def render_tick(self):
        pygame.draw.circle(screen, white, (self.x, self.y), self.radius, self.radius) 
        self.movement()
        self.x += self.vx
        self.y += self.vy

    def movement(self):
        dx = goal[0] - self.x
        dy = goal[1] - self.y
        self.vx = (dx / (abs(dx) + abs(dy))) *speed
        self.vy = (dy / (abs(dx) + abs(dy))) *speed
        collide(self)
        

class Wall:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        if self.start[0] == self.end[0]:
            self.orientation = 'V' # Vertical
        elif self.start[1] == self.end[1]:
            self.orientation = 'H' # Horizontal
        else:
            self.orientation = 'D' # Diagonal
    
    def render_tick(self):
        pygame.draw.line(screen, white, self.start, self.end)


class Object:
    def __init__(self, center_h, center_v, size):
        self.center_h = center_h
        self.center_v = center_v
        self.size = size
        self.wall1 = Wall(self.center_h-self.size,self.center_v,self.center_h,self.center_v-self.size)
        self.wall2 = Wall(self.center_h,self.center_v-self.size,self.center_h+self.size,self.center_v)
        self.wall3 = Wall(self.center_h+self.size,self.center_v,self.center_h,self.center_v+self.size)
        self.wall4 = Wall(self.center_h,self.center_v+self.size,self.center_h-self.size,self.center_v)

    def render_tick(self):
        pygame.draw.line(screen, white, self.wall1.start, self.wall1.end)
        pygame.draw.line(screen, white, self.wall2.start, self.wall2.end)
        pygame.draw.line(screen, white, self.wall3.start, self.wall3.end)
        pygame.draw.line(screen, white, self.wall4.start, self.wall4.end)


def collide(circle):
    coeff_total = 1

    for c in circles:
        if circle == c:
            continue
        dist = sqrt((c.x - circle.x)**2 + (c.y - circle.y)**2)
        if dist - (c.radius + circle.radius) < 0:
            dx = c.x - circle.x
            dy = c.y - circle.y
            circle.vx -= (dx / (abs(dx) + abs(dy))) *speed
            circle.vy -= (dy / (abs(dx) + abs(dy))) *speed
            coeff_total *= coeff_ralentissement 

    for w in walls:
        if w.orientation == 'V' and (100 + circle.radius >= circle.x or circle.x >= 1180 - circle.radius):
            circle.vx = 0
        elif w.orientation == 'H' and (60 + circle.radius >= circle.y or circle.y >= 660 - circle.radius):
            if not (610 + circle.radius < circle.x and circle.x < 670 - circle.radius):
                circle.vy = 0

    for o in objects:
        normalized_speed = speed * sqrt(2)/2
        dist_x = o.center_h - circle.x
        dist_y = o.center_v - circle.y
        if abs(dist_x) + abs(dist_y) - circle.radius < o.size:
            if circle.x < o.center_h:
                circle.vx = -normalized_speed
                circle.vy = -normalized_speed
            else:
                circle.vx = normalized_speed
                circle.vy = -normalized_speed

    circle.vx *= coeff_total
    circle.vy *= coeff_total


####################################################
# Initialisation

screen_res = (1280,720)
goal = (640,50)

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)

radius = 10
speed = 1
coeff_ralentissement = 0.7

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("TIPE : bousculades")
screen.fill(black)

finished = 0
initial_time = time.time()


####################################################
# Main run body

nb = 80
#nb = 10
circles = []
for i in range(nb):
#    circles.append(Circle(randint(120,1160), randint(80,640), radius))
#    circles.append(Circle(randint(400,880), randint(250,500), radius))
    circles.append(Circle(randint(340,940), randint(300,600), radius))    

walls = []

walls.append(Wall(100,60,100,660))        # Left_Vertical
walls.append(Wall(1180,60,1180,660))      # Right_Vertical
walls.append(Wall(100,60,610,60))         # TopRight_Horizontal
walls.append(Wall(670,60,1180,60))        # TopLeft_Horizontal
walls.append(Wall(100,660,1180,660))      # Bottom_Horizontal

objects = []

#objects.append(Object(640,180,70))       # One object

objects.append(Object(570,180,40))        # Two objects
objects.append(Object(710,180,40))


run = True
while run:
    screen.fill(black)

    for c in circles:
        c.render_tick()

    for w in walls:
        w.render_tick()

    for o in objects:
        o.render_tick()

    circles_new = []
    for c in circles:
        if not(c.on_goal()):
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
