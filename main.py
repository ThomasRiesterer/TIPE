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
#        pygame.draw.circle(screen, red, goal, 5, 5)
        self.movement()
        self.x += self.vx
        self.y += self.vy

    def movement(self):
        collisions = []
        for c in circles:
            if c == self:
                continue
            diff = sqrt((c.x - self.x)**2 + (c.y - self.y)**2)
            dist = diff - (c.radius + self.radius)
            if dist < 0:
                collisions.append(c)
        n = 1+len(collisions)/3

        if wall_collide_H(self):
            if self.x < goal[0]:
                self.vx = speed
                self.vy = 0
            else:
                self.vx = -speed
                self.vy = 0
        elif wall_collide_V(self):
            self.vx = 0
            self.vy = -speed
        else:
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
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        if self.start[0] == self.end[0] :
            self.orientation = 'V' # Vertical
        if self.start[1] == self.end[1] :
            self.orientation = 'H' # Horizontal
    
    def render_tick(self):
        pygame.draw.line(screen, white, self.start, self.end)


def on_goal(circle):
    return abs(circle.x - goal[0]) <= 40 and abs(circle.y - goal[1]) <= 20

def wall_collide_V(circle):
    colliding = False
    for w in walls:
        if w.orientation == 'H':
            continue
        if (w.start[0] - circle.radius < circle.x and circle.x < w.end[0] + circle.radius):
            if (w.start[1] < circle.y and circle.y < w.end[1]):
                colliding = True
    return colliding

def wall_collide_H(circle):
    colliding = False
    for w in walls:
        if w.orientation == 'V':
            continue
        if (w.start[1] - circle.radius < circle.y and circle.y < w.end[1] + circle.radius):
            if (w.start[0] < circle.x and circle.x < w.end[0]):
                colliding = True
    return colliding


####################################################
# Initialisation

screen_res = (1280,720)
goal = (640,50)

white = (255,255,255)
red = (255,0,0)
gray = (50,50,50)

radius = 18
speed = 1
coeff = 2

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screen_res)
pygame.display.set_caption("TIPE : bousculades")
screen.fill(gray)


####################################################
# Main run body

nb = 50
circles = []
for i in range(nb):
#    circles.append(Circle(randint(120,1160), randint(80,640), radius))
    circles.append(Circle(randint(400,880), randint(250,500), radius))    

walls = []

walls.append(Wall(100,60,100,660))     # Left_Vertical
walls.append(Wall(1180,60,1180,660))   # Right_Vertical
walls.append(Wall(100,60,610,60))      # TopRight_Horizontal
walls.append(Wall(670,60,1180,60))     # TopLeft_Horizontal
walls.append(Wall(100,660,1180,660))   # Bottom_Horizontal

#walls.append(Wall(620,150,620,190))    # Object1
#walls.append(Wall(660,150,660,190))
#walls.append(Wall(620,150,660,150))
#walls.append(Wall(620,190,660,190))


run = True
while run:
    screen.fill(gray)

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

    pygame.display.update()
    clock.tick(60)

pygame.quit()
