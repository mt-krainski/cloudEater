import pygame
import sys
import button
import game

class Menu:

    def __init__(self, width, height):
        self.width = width
        self.height = height


    def click_start(self, game_mode):
        newgame = game.Game(game_mode)
        newgame.play()


    def click_quit(self, event):
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()


    def show_menu(self):

        MENU_BG_PATH = "./img/menu_bg.png"

        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))

        bg_image = pygame.image.load(MENU_BG_PATH)
        bg_image = pygame.transform.scale(bg_image, [int(x*0.9) for x in game.SCREEN_SIZE])
        pygame.display.set_caption("menu")

        start_button = button.Button(screen, "PLAY SOLO", -200, 280)
        start_adv_button = button.Button(screen, "ADVERSARY MODE", -120, 280)
        quit_button = button.Button(screen, "QUIT", -40, 280)

        pygame.font.init()
        title_font = pygame.font.SysFont('Papyrus', 40, True)
        textsurface_cloud = title_font.render("CLOUD", False, (16,66,87))
        textsurface_eater = title_font.render("EATER", False, (16,66,87))

        while True:
            screen.fill((238, 238, 238))
            screen.blit(bg_image, [int(x * 0.1) for x in game.SCREEN_SIZE])

            start_button.draw_button()
            start_adv_button.draw_button()
            quit_button.draw_button()

            screen.blit(textsurface_cloud, (600, 375))
            screen.blit(textsurface_eater, (725, 425))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] >= start_button.get_left_x() and pygame.mouse.get_pos()[1] >= start_button.get_top_y():
                        if pygame.mouse.get_pos()[0] <= start_button.get_right_x() and pygame.mouse.get_pos()[1] <= start_button.get_bottom_y():
                            self.click_start(game.GAMEMODE_SOLO)
                    if pygame.mouse.get_pos()[0] >= start_adv_button.get_left_x() and pygame.mouse.get_pos()[1] >= start_adv_button.get_top_y():
                        if pygame.mouse.get_pos()[0] <= start_adv_button.get_right_x() and pygame.mouse.get_pos()[1] <= start_adv_button.get_bottom_y():
                            self.click_start(game.GAMEMODE_ADVERSARY)
                    if pygame.mouse.get_pos()[0] >= quit_button.get_left_x() and pygame.mouse.get_pos()[1] >= quit_button.get_top_y():
                        if pygame.mouse.get_pos()[0] <= quit_button.get_right_x() and pygame.mouse.get_pos()[1] <= quit_button.get_bottom_y():
                            self.click_quit(pygame.QUIT)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



