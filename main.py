import random

import pygame
import sys
import math
import numpy as np

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

white = (255, 255, 255)
red = (255, 0, 0)
screen.fill(white)

BASIC_TRIANGLE_POINTLIST = [(-10, -20), (10, -20), (0, 20)]

for x, y in BASIC_TRIANGLE_POINTLIST:
    print(f"x: {x}")
    print(f"y: {y}")


def update_mouse():
    return pygame.mouse.get_pos()


def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def draw_plane(x, y, phi, screen):
    PLANE_COLOR = (0, 0, 255) #blue
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)
    t_matrix = np.matrix(
        [[cos_phi, -sin_phi, x],
         [sin_phi,  cos_phi, y],
         [      0,        0, 1]])

    new_pointlist = \
        [(t_matrix*np.matrix([X, Y, 1]).transpose())[0:2].tolist()
         for X, Y in BASIC_TRIANGLE_POINTLIST]

    points = [[item[0][0], item[1][0]] for item in new_pointlist]

    pygame.draw.polygon(screen, PLANE_COLOR, points)


angle = 0
plane_pos = [100, 100]
velocity = 10
refresh_freqency = 100
dt = 1/refresh_freqency

marked_points = []

while True:
    screen.fill(white)
    pos = update_mouse()
    angle = -math.pi/2 + math.atan2((pos[1]-plane_pos[1]), (pos[0]-plane_pos[0]))

    for x, y in marked_points:
        # screen.set_at((int(x), int(y)), red)
        pygame.draw.circle(screen, red, (int(x), int(y)), 2, 0)

    help(screen.fill)
    draw_plane(plane_pos[0],
               plane_pos[1],
               angle, screen)

    velocity = 0.5*get_distance(pos, plane_pos)

    plane_pos[0] -= velocity * math.sin(angle) * dt
    plane_pos[1] += velocity * math.cos(angle) * dt

    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        for i in range(10):
            marked_points.append(
                [plane_pos[0] + random.gauss(0, 20),
                 plane_pos[1] + random.gauss(0, 20)])

    if pygame.mouse.get_pressed()[2]:
        marked_points.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    msElapsed = clock.tick(refresh_freqency)
