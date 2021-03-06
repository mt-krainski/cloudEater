import random

import pygame
import sys
import math
import numpy as np

SCREEN_SIZE = (800, 600)

from backend.SceneProvider import SceneProvider

scene_provider = SceneProvider()
scene_provider.get_random_scene()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
light_grey = (189,189,189)
transparent_purple = (153, 50, 204)
screen.fill(white)

def setup_transparent_surface(surface, transparent_colour, alpha):
    surface.fill(transparent_colour)
    surface.set_colorkey(transparent_colour)
    surface.set_alpha(alpha)

paint_surface = pygame.Surface(SCREEN_SIZE)
setup_transparent_surface(paint_surface, transparent_purple, 140)

paint_preview_surface = pygame.Surface(SCREEN_SIZE)
setup_transparent_surface(paint_preview_surface, transparent_purple, 128)

side_menu_surface = pygame.Surface((200, SCREEN_SIZE[1]))
side_menu_surface.fill((238,238,238))

MENU_BG_PATH = "./img/menu_bg.png"
bg_image = pygame.image.load(MENU_BG_PATH)
bg_image = pygame.transform.scale(bg_image, [200, int(600/4)])
side_menu_surface.blit(bg_image, [0, SCREEN_SIZE[1]-int(600/4)])

pygame.font.init()
SIDE_MENU_TEXTS = [
    "CLOUD EATER",
    "",
    "left click - spray",
    "right click - unspray",
    "E - switch image type",
    "up - increase spread",
    "down - decrease spread",
    "m wheel - change spread",
    "w - exit"]

SIDE_MENU_TEXT_SIZE = 20
side_menu_font = pygame.font.SysFont('Arial', SIDE_MENU_TEXT_SIZE, True)
for i, text in enumerate(SIDE_MENU_TEXTS):
    side_menu_text_surface = side_menu_font.render(text, False, (0, 0, 0))
    text_width, text_height = side_menu_font.size(text)
    text_height *= 1.2
    side_menu_surface.blit(
        side_menu_text_surface,
        (10, 20 + i*text_height))

BASIC_TRIANGLE_POINTLIST = [(-10, -20), (10, -20), (0, 20)]

GAMEMODE_SOLO = 0
GAMEMODE_ADVERSARY = 1
GAMEMODE_TRAINING = 2

def update_mouse():
    return pygame.mouse.get_pos()


def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def get_angle(a, b):
    angle = -math.pi / 2 + math.atan2((a[1] - b[1]), (a[0] - b[0]))
    return angle

old_angle = 0
delta_angle_old = 0
delta_distance = 0
plane_pos = [400, 300]
velocity = 10
refresh_frequency = 100
dt = 1 / refresh_frequency
linear_acceleration = 0
angular_acceleration = 0

marked_points = []

pos = plane_pos
vel = velocity
bear = 0
delta_bear = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite
        if image_file is not None:
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()

    def set_image(self, image: np.ndarray):
        surf = pygame.surfarray.make_surface(np.swapaxes(image,0,1))
        self.image = surf
        self.rect = self.image.get_rect()


class Game:
    def __init__(self, game_mode):
        self.dt = 1 / refresh_frequency
        self.plane = Fighter(plane_pos, velocity, bear, delta_bear, 20)
        self.aux_sprite_right = AuxFighterSprite(
                                [int(SCREEN_SIZE[0]), 0],
                                self.plane)
        self.aux_sprite_left = AuxFighterSprite(
                                [-int(SCREEN_SIZE[0]), 0],
                                self.plane)
        self.aux_sprite_bottom = AuxFighterSprite(
                                [0, int(SCREEN_SIZE[1])],
                                self.plane)
        self.aux_sprite_top = AuxFighterSprite(
                                [0, -int(SCREEN_SIZE[1])],
                                self.plane)
        self.game_mode = game_mode

    def play(self):
        playing = True
        level_finished = False
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        pygame.mouse.set_pos(400,300)

        BackGround = Background(None, [0, 0])
        BackGround.set_image(scene_provider.get_next_satellite_image())

        if self.game_mode == GAMEMODE_ADVERSARY:

            adversary_surface = pygame.Surface(SCREEN_SIZE)
            setup_transparent_surface(adversary_surface, black, 50)

            adversary_bg_image = pygame.surfarray.make_surface(np.swapaxes(scene_provider.get_submit(np.random.randint(0,100)),0,1))
            adversary_surface.blit(adversary_bg_image, [0, 0])

            paint_surface.blit(adversary_surface, (0,0))

        #BackGround.set_image(scene_provider.get_next_satellite_image())

        while playing:

            screen.fill(white)

            pos = update_mouse()
            self.plane.update(pos)

            # Check to see if needs to be swapped with current
            if self.plane.position[0] <  0 :
                # off screen left, SWAP WITH RIGHT
                self.plane.position[0] = self.plane.position[0] + SCREEN_SIZE[0]
            elif self.plane.position[0]  > SCREEN_SIZE[0]:
                # off screen right, SWAP WITH LEFT
                self.plane.position[0] = self.plane.position[0] - SCREEN_SIZE[0]
            elif self.plane.position[1]  < 0:
                # off screen top, SWAP WITH BOTTOM
                self.plane.position[1] = self.plane.position[1] + SCREEN_SIZE[1]
            elif self.plane.position[1] > SCREEN_SIZE[1]:
                # off screen bottom, SWAP WITH TOP
                self.plane.position[1] = self.plane.position[1] - SCREEN_SIZE[1]

            # Update shadow positions
            self.aux_sprite_right.copy_position(self.plane)
            self.aux_sprite_left.copy_position(self.plane)
            self.aux_sprite_bottom.copy_position(self.plane)
            self.aux_sprite_top.copy_position(self.plane)


            screen.blit(BackGround.image, BackGround.rect)
            screen.blit(paint_surface, (0, 0))
            screen.blit(paint_preview_surface, (0, 0))

            if self.game_mode != GAMEMODE_TRAINING:
                self.plane.draw(screen)
                self.aux_sprite_right.draw(screen)
                self.aux_sprite_left.draw(screen)
                self.aux_sprite_bottom.draw(screen)
                self.aux_sprite_top.draw(screen)

            if pygame.mouse.get_pressed()[0]:
                if self.game_mode == GAMEMODE_TRAINING:
                    self.plane.draw_with_mouse(red)
                else:
                    self.plane.draw_shooting(red)


            if pygame.mouse.get_pressed()[2]:
                if self.game_mode == GAMEMODE_TRAINING:
                    self.plane.draw_with_mouse(transparent_purple)
                else:
                    self.plane.draw_shooting(transparent_purple)

            if self.game_mode == GAMEMODE_TRAINING:
                self.plane.draw_paint_preview_mouse(paint_preview_surface)
            else:
                self.plane.draw_paint_preview(paint_preview_surface)
                self.aux_sprite_right.draw_paint_preview(paint_preview_surface)
                self.aux_sprite_left.draw_paint_preview(paint_preview_surface)
                self.aux_sprite_bottom.draw_paint_preview(paint_preview_surface)
                self.aux_sprite_top.draw_paint_preview(paint_preview_surface)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if self.plane.paint_stdev < 20:
                            self.plane.incr_paint_stdev()
                    if event.button == 5:
                        if self.plane.paint_stdev > 1:
                            self.plane.decr_paint_stdev()

                    # same as above but for key - find a way to avoid repetition
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if self.plane.paint_stdev < 20:
                        self.plane.incr_paint_stdev()
                if keys[pygame.K_DOWN]:
                    if self.plane.paint_stdev > 1:
                        self.plane.decr_paint_stdev()
                if keys[pygame.K_e]:
                    BackGround.set_image(scene_provider.get_next_satellite_image())
                if keys[pygame.K_w]:
                    scene_provider.end_round(pygame.surfarray.array2d(paint_surface))              
                    self.game_end()
                    playing = False
                if keys[pygame.K_ESCAPE]:
                    self.game_end()
                    playing = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(side_menu_surface, (SCREEN_SIZE[0], 0))
            pygame.display.update()
            msElapsed = clock.tick(refresh_frequency)

    def game_end(self):
        paint_surface.fill(transparent_purple)
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        self.plane.position = plane_pos


class Fighter:
    def __init__(self, pos, vel, bear, delta_bear, paint_stdev):
        self.position = pos
        self.velocity = vel
        self.bearing = bear
        self.delta_bearing = delta_bear
        self.paint_stdev = paint_stdev
        self.origin = [400, 300]


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

        PLANE_COLOR = (16,66,87)
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

    def draw_paint_preview(self, surface):
        surface.fill(transparent_purple)
        pygame.draw.circle(surface, light_grey,
                           (int(self.position[0]), int(self.position[1])), self.paint_stdev*2, 0)

    def draw_paint_preview_mouse(self, surface):
        surface.fill(transparent_purple)
        pygame.draw.circle(surface, light_grey,
                           (int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])), self.paint_stdev * 2, 0)

    def draw_shooting(self, colour):
        for i in range(100):
            pygame.draw.circle(
                paint_surface, colour,
                (int(self.position[0] + random.gauss(0, self.paint_stdev)),
                    int(self.position[1] + random.gauss(0, self.paint_stdev))),
                2, 0)

    def draw_with_mouse(self, colour):
        for i in range(100):
            pygame.draw.circle(
                paint_surface, colour,
                (int(pygame.mouse.get_pos()[0] + random.gauss(0, self.paint_stdev)),
                 int(pygame.mouse.get_pos()[1] + random.gauss(0, self.paint_stdev))),
                2, 0)

    def incr_paint_stdev(self) -> object:
        self.paint_stdev += 1

    def decr_paint_stdev(self):
        self.paint_stdev -= 1


class AuxFighterSprite():
    """
    Implements shadow sprites for wraparound.
    """
    def __init__(self, OFFSET, PlayerFigherObject):
        self.position = [0, 0]
        self.velocity = 0
        self.bearing = 0
        self.paint_stdev = 0
        self.origin = PlayerFigherObject.origin
        self.OFFSET = OFFSET
        self.copy_position(PlayerFigherObject)

    def copy_position(self, FigtherObject):
        self.position[0] = FigtherObject.position[0] + self.OFFSET[0]
        self.position[1] = FigtherObject.position[1] + self.OFFSET[1]
        self.velocity = FigtherObject.velocity
        self.bearing  = FigtherObject.bearing
        self.paint_stdev = FigtherObject.paint_stdev

    def draw(self, screen):
        PLANE_COLOR = (16,66,87)
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

    def draw_paint_preview(self, surface):
        #surface.fill(transparent_purple)
        pygame.draw.circle(surface, light_grey,
                           (int(self.position[0]), int(self.position[1])), self.paint_stdev*2, 0)

