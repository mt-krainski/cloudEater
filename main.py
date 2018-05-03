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
ck_purple = (153, 50, 204)
screen.fill(white)

surface1 = pygame.Surface((800,600))
surface1.fill(ck_purple)
# surface1.set_alpha(255)
surface1.set_colorkey(ck_purple)

BASIC_TRIANGLE_POINTLIST = [(-10, -20), (10, -20), (0, 20)]


def update_mouse():
    return pygame.mouse.get_pos()


def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def draw_plane(x, y, phi, screen):
    PLANE_COLOR = (0, 0, 255)  # blue
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


def get_angle(a, b):
    angle = -math.pi / 2 + math.atan2((a[1] - b[1]), (a[0] - b[0]))
    print(f"angle: {angle}")
    return angle


angle = 0
old_angle = 0
delta_angle = 0
delta_angle_old = 0
delta_distance = 0
plane_pos = [100, 100]
velocity = 10
refresh_frequency = 100
dt = 1 / refresh_frequency
linear_acceleration = 0
angular_acceleration = 0

marked_points = []

while True:
    screen.fill(white)
    pos = update_mouse()

    delta_angle = old_angle - get_angle(pos, plane_pos)

    if delta_angle - delta_angle_old > math.pi:
        delta_angle -= math.pi*2
    elif delta_angle - delta_angle_old < -math.pi:
        delta_angle += math.pi*2

    delta_angle_old = delta_angle

    screen.blit(surface1, (0, 0))
    help(screen.fill)
    draw_plane(plane_pos[0],
               plane_pos[1],
               angle, screen)

    delta_distance = get_distance(pos, plane_pos)

    linear_acceleration = 0.5*get_distance(pos, plane_pos)
    angular_acceleration = -2*delta_angle

    angle += angular_acceleration*dt
    velocity = 0.5*get_distance(pos, plane_pos)

    old_angle = angle

    plane_pos[0] -= velocity * math.sin(angle) * dt
    plane_pos[1] += velocity * math.cos(angle) * dt

    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        for i in range(100):
            pygame.draw.circle(surface1, red, (int(plane_pos[0] + random.gauss(0, 20)), int(plane_pos[1] + random.gauss(0, 20))), 2, 0)

    if pygame.mouse.get_pressed()[2]:
        marked_points.clear()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    msElapsed = clock.tick(refresh_frequency)
