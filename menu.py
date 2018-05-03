import pygame
import sys
import button
import game

class Menu:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def click_start(self):
        newgame = game.Game()
        newgame.play()

    def click_quit(self, event):
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def show_menu(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("menu")

        screen.fill((175,175,175))

        start_button = button.Button(screen, "Start", 0)
        quit_button = button.Button(screen, "Quit", 100)

        start_button.draw_button()
        quit_button.draw_button()

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] >= start_button.get_left_x() and pygame.mouse.get_pos()[1] >= start_button.get_top_y():
                        if pygame.mouse.get_pos()[0] <= start_button.get_right_x() and pygame.mouse.get_pos()[1] <= start_button.get_bottom_y():
                            self.click_start()
                    if pygame.mouse.get_pos()[0] >= quit_button.get_left_x() and pygame.mouse.get_pos()[1] >= quit_button.get_top_y():
                        if pygame.mouse.get_pos()[0] <= quit_button.get_right_x() and pygame.mouse.get_pos()[1] <= quit_button.get_bottom_y():
                            self.click_quit(pygame.QUIT)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



