import pygame

class Button:

    def __init__(self, screen, label, offset=0):
        self.screen = screen
        self.buttonColour = (153, 153, 255)
        self.buttonHeight = 50
        self.buttonWidth = 150
        self.offset = offset
        self.label = label

    def get_left_x(self):
        return self.screen.get_width() / 2 - self.buttonWidth / 2

    def get_top_y(self):
        return self.screen.get_height() / 2 - self.buttonHeight / 2 + self.offset

    def get_right_x(self):
        return self.get_left_x() + self.buttonWidth

    def get_bottom_y(self):
        return self.get_top_y() + self.buttonHeight

    def write_label(self):
        pygame.font.init()
        myfont = pygame.font.SysFont('Arial', 30)
        textsurface = myfont.render(self.label, False, (0, 0, 0))

        text_width, text_height = myfont.size(self.label)

        self.screen.blit(textsurface, (self.get_right_x() + (self.get_left_x()-self.get_right_x())/2 - text_width/2, self.get_top_y() + (self.get_bottom_y()-self.get_top_y())/2 - text_height/2))

    def draw_button(self):
        pygame.draw.rect(self.screen, self.buttonColour, (self.get_left_x(), self.get_top_y(), self.buttonWidth, self.buttonHeight))
        self.write_label()

