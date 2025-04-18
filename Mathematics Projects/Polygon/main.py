import pygame
import random
import numpy as np
import math

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()

shena = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
points = []
points_ = []
samples = []
show = False


def transform(x, y):
    return (x + (width / 2), (height / 2) - y)


def sample_type(p, points):
    v1, v2 = [0, 0], [0, 0]
    a = 0
    for i in range(0, len(points)):
        if i + 1 < len(points):
            v1[0], v1[1] = points[i][0] - p[0], points[i][1] - p[1]
            v2[0], v2[1] = points[i + 1][0] - p[0], points[i + 1][1] - p[1]
        else:
            v1[0], v1[1] = points[i][0] - p[0], points[i][1] - p[1]
            v2[0], v2[1] = points[0][0] - p[0], points[0][1] - p[1]
        c = ((v1[0] * v2[0]) + (v1[1] * v2[1])) / (
                (((v1[0] ** 2) + (v1[1] ** 2)) ** 0.5) * (((v2[0] ** 2) + (v2[1] ** 2)) ** 0.5))
        a += math.acos(c)
    a = round(a * 180 / math.pi, 10)
    if a == 360:
        return (255, 0, 0)
    else:
        return (0, 255, 0)


while shena:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sena = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                sena = False
            if event.key == pygame.K_SPACE:
                if show == False:
                    show = True
                    for i in points:
                        points_.append([i[0] + (width / 2), (height / 2) - i[1]])
                    for i in range(10000):
                        samples.append([random.randint(-width / 2, width / 2), random.randint(-height / 2, height / 2)])
                else:
                    show = False
                    points.clear()
                    points_.clear()
                    samples.clear()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not show:
            x, y = pygame.mouse.get_pos()
            points.append([x - (width / 2), (height / 2) - y])
    for i in points:
        pygame.draw.circle(screen, colors['white'], (i[0] + (width / 2), (height / 2) - i[1]), 1)
    if show:
        pygame.draw.polygon(screen, colors['white'], points_, 1)
    if len(samples) > 0:
        for i in samples:
            pygame.draw.circle(screen, sample_type(i, points), (i[0] + (width / 2), (height / 2) - i[1]), 1)
    pygame.display.update()
pygame.quit()
