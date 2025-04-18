import pygame, random

pygame.init()

class Button:
    def __init__(self, text, width, height, pos):
        self.text = text
        self.pressed = False
        self.original_y_pos = pos[1]
        self.under_stress = False
        self.select = 3
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (255, 255, 255)
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.surf = screen
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        pygame.draw.rect(screen, (0, 0, 0), self.top_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.top_rect, self.select)
        screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if self.text == 'Cancel' or self.text == 'Exit to Desktop' or self.text == 'Exit to Main-Menu':
                self.select = 1
            if pygame.mouse.get_pressed()[0] == True:
                self.pressed = True
            if self.under_stress == False:
                self.under_stress = True


        else:
            self.pressed = False
            if self.under_stress == True:
                self.under_stress = False
            self.select = 3


gui_font = pygame.font.Font(None, 48)