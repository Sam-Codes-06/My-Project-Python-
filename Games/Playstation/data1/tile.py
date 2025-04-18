import pygame

pygame.init()
colors = {2: '#F1948A', 4: '#BB8FCE', 8: '#95c9ec', 16: '#bdc3c7', 32: '#f8c471', 64: '#d35400', 128: '#82e0aa',
          256: '#73c6b6', 512: '#7f8c8d', 1024: '#34495e', 2048: '#7b241c', 4096: '#4a235a', 8192: '#1b4f72',
          16384: '#0e6251', 32768: '#7e5109', 65536: '#4D5656', 131072: '#1b2631'}


class Button:
    def __init__(self, text, width, height, pos):
        self.text = text
        self.select = 3
        self.top_rect = pygame.Rect(pos, (width, height))
        self.size = 0
        if text in ('2', '4', '8'):
            self.size = 100
        if text in ('16', '32', '64'):
            self.size = 80
        if text in ('128', '256', '512'):
            self.size = 60
        self.gui_font = pygame.font.Font('freesansbold.ttf', self.size)
        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.surf = screen
        if self.text != '0':
            pygame.draw.rect(screen, colors[int(self.text)], self.top_rect, 0, 3)
            screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y + 2))
        if self.text == '0':
            pygame.draw.rect(screen, '#FAE5D3', self.top_rect, 0, 3)
            screen.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))


