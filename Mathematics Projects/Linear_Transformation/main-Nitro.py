import pygame
import numpy as np
import arrow

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()

run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0), 'yellow': (150, 150, 0)}


def transform(x, y, r=''):
    if r == '':
        return ((x * 25) + width / 2, height / 2 - (y * 25))
    else:
        return ((x * 50) + width / 2, height / 2 - (y * 50))


current = np.array([[1, 5], [-3, -4]])
initial = np.array([[1, 0], [0, 1]])
show_i = np.array([[1, 0], [0, 1]])
grid_x = []
grid_y = []
show_x, show_y = [], []
l = 40
print(current)
vector = np.array([[1, 1]])
for i in range(-l, l + 1):
    grid_y.append([np.array([[i, -l]]), np.array([[i, l]])])
    grid_x.append([np.array([[-l, i]]), np.array([[l, i]])])
    show_x.append([np.array([[-l, i]]), np.array([[l, i]])])
    show_y.append([np.array([[i, -l]]), np.array([[i, l]])])
while run:
    screen.fill((0, 0, 0))
    for i in range(len(grid_x)):
        a1, a2 = np.matrix.dot(show_y[i][0], show_i), np.matrix.dot(show_y[i][1], show_i)
        if a1[0][0] == 0:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 3)
        elif a1[0][0] % 2 == 0:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 2)
        else:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 1)
        a1, a2 = np.matrix.dot(show_x[i][0], show_i), np.matrix.dot(show_x[i][1], show_i)
        if a1[0][1] == 0:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 3)
        elif a1[0][1] % 2 == 0:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 2)
        else:
            pygame.draw.line(screen, colors['grey'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 1)
    for i in range(len(grid_y)):
        a1, a2 = np.dot(grid_y[i][0], current), np.dot(grid_y[i][1], current)
        if grid_y[i][0][0][0] % 2 == 0 and grid_y[i][0][0][0] != 0:
            pygame.draw.line(screen, colors['blue'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 1)
        elif grid_y[i][0][0][0] == 0:
            pygame.draw.line(screen, colors['blue'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 3)
        a1, a2 = np.dot(grid_x[i][0], current), np.dot(grid_x[i][1], current)
        if grid_x[i][0][0][1] % 2 == 0 and grid_x[i][1][0][1] != 0:
            pygame.draw.line(screen, colors['blue'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 1)
        elif grid_x[i][1][0][1] == 0:
            pygame.draw.line(screen, colors['blue'], transform(a1[0][0], a1[0][1]), transform(a2[0][0], a2[0][1]), 3)
    pygame.draw.line(screen, colors['green'], transform(0, 0, 'u'), transform(current[0][0], current[0][1], 'u'), 3)
    pygame.draw.line(screen, colors['orange'], transform(0, 0, 'u'), transform(current[1][0], current[1][1], 'u'), 3)
    v = arrow.arrow((width / 2, height / 2), transform(current[1][0], current[1][1], 'u'))
    pygame.draw.polygon(screen, colors['orange'], v.p)
    v = arrow.arrow((width / 2, height / 2), transform(current[0][0], current[0][1], 'u'))
    pygame.draw.polygon(screen, colors['green'], v.p)
    pygame.draw.line(screen, colors['yellow'], transform(0, 0, 'unit'), transform(vector[0][0], vector[0][1], 'unit'), 3)
    pygame.draw.polygon(screen, colors['yellow'], arrow.arrow(transform(0, 0), transform(vector[0][0], vector[0][1], 'unit')).p)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
            if event.key == pygame.K_SPACE:
                vector = np.matrix.dot(vector, current)
    pygame.display.update()
pygame.quit()
