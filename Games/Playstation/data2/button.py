import pygame, random

pygame.init()
colors = ['#cd6155', '#e74c3c', '#922b21', '#641e16', '#78281f', '#f1948a', '#9b59b6', '#bb8fce', '#6c3483', '#5b2c6f',
          '#5499c7', '#85c1e9', '#247a13', '#1a5276', '#1b4f72', '#76d7c4', '#45b39d', '#17a589', '#117864', '#0b5345',
          '#7dcea0', '#58d68d', '#229954', '#1d8348', '#f9e79f', '#f8c471', '#f4d03f', '#d68910', '#9a7d0a', '#f0b27a',
          '#d35400', '#935116', '#797d7f', '#424949', '#5d6d73', '#34495e', '#212f3d', '#979a9a', '#f7dc6f', '#aed6f1',
          '#000000']


class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.text = text
        self.pressed = False
        self.elevation = 3
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.under_stress = False
        self.select = 3
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = colors[random.randint(0, len(colors) - 1)]
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.surf = screen
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        if self.text == 'Cancel' or self.text == 'Exit to Desktop' or self.text == 'Exit to Main-Menu':
            pygame.draw.rect(screen, (0, 0, 0), self.top_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.top_rect, self.select)
            screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
        elif self.text in ('Single-Player', 'Multi-Player', 'Exit', 'Host', 'Join', 'Back', 'OK'):
            pygame.draw.rect(screen, self.top_color, self.top_rect)
            screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))
        else:
            screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if self.text == 'Cancel' or self.text == 'Exit to Desktop' or self.text == 'Exit to Main-Menu':
                self.select = 1
            if self.under_stress == False:
                self.top_color = colors[random.randint(0, len(colors) - 1)]
                self.under_stress = True


        else:
            self.dynamic_elecation = self.elevation
            if self.under_stress == True:
                self.top_color = colors[random.randint(0, len(colors) - 1)]
                self.under_stress = False
            self.elevation = 3
            self.select = 3


gui_font = pygame.font.Font(None, 48)