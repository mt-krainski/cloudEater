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
light_grey = (189,189,189)
transparent_purple = (153, 50, 204)
screen.fill(white)

paint_surface = pygame.Surface((800, 600))
paint_surface.fill(transparent_purple)
paint_surface.set_colorkey(transparent_purple)

paint_preview_surface = pygame.Surface((800, 600))
paint_preview_surface.fill(transparent_purple)
paint_preview_surface.set_colorkey(transparent_purple)
paint_preview_surface.set_alpha(128)

BASIC_TRIANGLE_POINTLIST = [(-10, -20), (10, -20), (0, 20)]


def update_mouse():
    return pygame.mouse.get_pos()


def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

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

paint_standard_deviation = 20


pos = plane_pos
vel = velocity
bear = angle
delta_bear = delta_angle

class Game:
    def __init__(self):
        self.dt = 1 / refresh_frequency

    def play(self):
        while True:

            screen.fill(white)

            pos = update_mouse()
            plane.update(pos)
            # plane.update_bearing(pos)

            screen.blit(paint_surface, (0, 0))
            screen.blit(paint_preview_surface, (0, 0))

            plane.draw(screen)

            if pygame.mouse.get_pressed()[0]:
                plane.draw_shooting(paint_standard_deviation)
            plane.draw_paint_preview(paint_preview_surface, paint_standard_deviation * 2)

            pygame.display.update()
            if pygame.mouse.get_pressed()[2]:
                marked_points.clear()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            msElapsed = clock.tick(refresh_frequency)


class Scene:
    def __init__(self):
        return

class Fighter:
    def __init__(self, pos, vel, bear, delta_bear):
        self.position = pos
        self.velocity = vel
        self.bearing = bear
        self.delta_bearing = delta_bear


    def update(self, mouse_position):
        self.update_position(mouse_position)
        self.update_velocity(mouse_position)
        self.update_bearing(mouse_position)

    def update_position(self, mouse_position):
        self.position[0] -= self.velocity * math.sin(self.bearing) * dt
        self.position[1] += self.velocity * math.cos(self.bearing) * dt

    def update_velocity(self, mouse_position):
        self.velocity = 0.5*get_distance(self.position, mouse_position)

    def update_bearing(self, mouse_position):
        delta_bearing = self.bearing - get_angle(mouse_position, self.position)

        if delta_bearing - self.delta_bearing > math.pi:
            delta_bearing -= 2*math.pi
        elif delta_bearing - self.delta_bearing < -math.pi:
            delta_bearing += 2*math.pi

        angular_acceleration = -2*delta_bearing
        self.bearing += angular_acceleration*dt

    def draw(self, screen):

        PLANE_COLOR = (0, 0, 255)  # blue
        cos_phi = math.cos(self.bearing)
        sin_phi = math.sin(self.bearing)
        t_matrix = np.matrix(
            [[cos_phi, -sin_phi, self.position[0]],
             [sin_phi, cos_phi, self.position[1]],
             [0, 0, 1]])

        new_pointlist = \
            [(t_matrix * np.matrix([X, Y, 1]).transpose())[0:2].tolist()
             for X, Y in BASIC_TRIANGLE_POINTLIST]

        points = [[item[0][0], item[1][0]] for item in new_pointlist]

        pygame.draw.polygon(screen, PLANE_COLOR, points)

    def draw_paint_preview(self, surface, paint_radius):
        surface.fill(transparent_purple)
        pygame.draw.circle(surface, light_grey,
                           (int(self.position[0]), int(self.position[1])), paint_radius, 0)

    def draw_shooting(self, paint_dstd):
        for i in range(100):
            pygame.draw.circle(
                paint_surface, red,
                (int(self.position[0] + random.gauss(0, paint_dstd)),
                    int(self.position[1] + random.gauss(0, paint_dstd))),
                2, 0)


plane = Fighter(plane_pos, velocity, angle, delta_angle)



game = Game()
game.play()
