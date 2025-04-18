import pygame
import math

class arrow(pygame.sprite.Sprite):
    def __init__(self, a, b):
        x, y = b
        dx, dy = x - a[0], y - a[1]
        super().__init__()
        if math.sqrt((dx * dx) + (dy * dy)) != 0:
            self.cos1 = dx / math.sqrt((dx * dx) + (dy * dy))
            self.sin1 = dy / math.sqrt((dx * dx) + (dy * dy))
            if dy != 0:
                self.sin2 = math.sin(math.atan(-dx / dy))
                self.cos2 = math.cos(math.atan(-dx / dy))
            else:
                self.sin2 = math.sin(math.pi / 2)
                self.cos2 = math.cos(math.pi / 2)
            self.p = ((x, y), (x + 6 * self.cos2 - 6 * 1.732 * self.cos1, y + 6 * self.sin2 - 6 * 1.732 * self.sin1),
                      (x - 6 * self.cos2 - 6 * 1.732 * self.cos1, y - 6 * self.sin2 - 6 * 1.732 * self.sin1))
        else:
            self.p = ((x,y), (x, y), (x, y))

