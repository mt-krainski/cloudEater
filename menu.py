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

        MENU_BG_PATH = "./img/menu_bg.png"

        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))

        screen.fill((238,238,238))
        bg_image = pygame.image.load(MENU_BG_PATH)
        bg_image = pygame.transform.scale(bg_image, [int(x*0.9) for x in game.SCREEN_SIZE])
        screen.blit(bg_image, [int(x*0.1) for x in game.SCREEN_SIZE])
        pygame.display.set_caption("menu")

        start_button = button.Button(screen, "Start", -200, 280)
        quit_button = button.Button(screen, "Quit", -120, 280)

        start_button.draw_button()
        quit_button.draw_button()

        pygame.font.init()
        title_font = pygame.font.SysFont('Papyrus', 40, True)
        textsurface = title_font.render("CLOUD", False, (16,66,87))
        screen.blit(textsurface, (600, 375))
        textsurface = title_font.render("EATER", False, (16,66,87))
        screen.blit(textsurface, (725, 425))

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



