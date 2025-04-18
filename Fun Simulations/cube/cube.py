import pygame, math, numpy as np

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()

cam = 10


def transform(x, y, z):
    global alpha, beta, gama
    v = [[x, y, z]]
    rx = [[1, 0, 0], [0, math.cos(alpha), -math.sin(alpha)], [0, math.sin(alpha), math.cos(alpha)]]
    ry = [[math.cos(beta), 0, math.sin(beta)], [0, 1, 0], [-math.sin(beta), 0, math.cos(beta)]]
    rz = [[math.cos(gama), -math.sin(gama), 0], [math.sin(gama), math.cos(gama), 0], [0, 0, 1]]
    v = np.dot(v, rx)
    v = np.dot(v, ry)
    v = np.dot(v, rz)
    """
    p = np.array([[1., 0., 1.], [0., 1., 1.]])
    v = np.dot(p, np.transpose(v))
    x, y = v[0][0], v[1][0]
    """
    x, y, z = v[0][0], v[0][1], v[0][2]
    x, y = y * (cam / (cam - x)), z * (cam / (cam - x))
    x, y = (x * 100) + (width / 2), (height / 2) - (100 * y)
    return (x, y)


run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
ym, zm, xm = 0, 0, 0
rotate_x, rotate_y, rotate_z = False, False, False
alpha, beta, gama = 0, 0, 0
while run:
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, 1 + ym, -1 + zm), transform(1 + xm, -1 + ym, -1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, 1 + ym, -1 + zm), transform(-1 + xm, 1 + ym, -1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, 1 + ym, -1 + zm), transform(1 + xm, 1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, -1 + ym, -1 + zm), transform(-1 + xm, -1 + ym, -1 + zm),
                     1)
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, -1 + ym, -1 + zm), transform(1 + xm, -1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, -1 + ym, -1 + zm), transform(-1 + xm, -1 + ym, 1 + zm),
                     1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, -1 + ym, -1 + zm), transform(-1 + xm, 1 + ym, -1 + zm),
                     1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, 1 + ym, 1 + zm), transform(1 + xm, 1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(1 + xm, 1 + ym, 1 + zm), transform(1 + xm, -1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, -1 + ym, 1 + zm), transform(1 + xm, -1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, -1 + ym, 1 + zm), transform(-1 + xm, 1 + ym, 1 + zm), 1)
    pygame.draw.line(screen, colors['blue'], transform(-1 + xm, 1 + ym, -1 + zm), transform(-1 + xm, 1 + ym, 1 + zm), 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
            if event.key == pygame.K_w:
                zm += .1
            if event.key == pygame.K_s:
                zm -= .1
            if event.key == pygame.K_d:
                ym += .1
            if event.key == pygame.K_a:
                ym -= .1
            if event.key == pygame.K_UP:
                if xm < 8.9:
                    xm += .1
            if event.key == pygame.K_DOWN:
                if xm > -8.9:
                    xm -= .1
            if event.key == pygame.K_LEFT:
                if rotate_x:
                    alpha -= math.pi / 180
                if rotate_y:
                    beta -= math.pi / 180
                if rotate_z:
                    gama -= math.pi / 180
            if event.key == pygame.K_RIGHT:
                if rotate_x:
                    alpha += math.pi / 180
                if rotate_y:
                    beta += math.pi / 180
                if rotate_z:
                    gama += math.pi / 180
            if event.key == pygame.K_SPACE:
                pass
            if event.key == pygame.K_x:
                rotate_x = True
            if event.key == pygame.K_y:
                rotate_y = True
            if event.key == pygame.K_z:
                rotate_z = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                rotate_x = False
            if event.key == pygame.K_y:
                rotate_y = False
            if event.key == pygame.K_z:
                rotate_z = False
    pygame.display.update()
pygame.quit()
