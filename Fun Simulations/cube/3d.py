import pygame, numpy as np, math

pygame.init()
screen = pygame.display.set_mode((600, 600))
width, height = pygame.display.get_surface().get_size()


def transform(x, y, z):
    global alpha, beta, gama, cam
    v = [[x, y, z]]
    rx = [[1, 0, 0], [0, math.cos(alpha), -math.sin(alpha)], [0, math.sin(alpha), math.cos(alpha)]]
    ry = [[math.cos(beta), 0, math.sin(beta)], [0, 1, 0], [-math.sin(beta), 0, math.cos(beta)]]
    rz = [[math.cos(gama), -math.sin(gama), 0], [math.sin(gama), math.cos(gama), 0], [0, 0, 1]]
    v = np.dot(v, rx)
    v = np.dot(v, ry)
    v = np.dot(v, rz)
    x, y, z = v[0][0], v[0][1], v[0][2]
    x, y = y * (cam / (cam - x)), z * (cam / (cam - x))
    x, y = (x * 100) + (width / 2), (height / 2) - (100 * y)
    return (x, y)


cam, alpha, beta, gama = 10, 0, 0, 0
run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "royalblue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 240), 'yellow': (150, 150, 0)}
rotate_x, rotate_y, rotate_z = False, False, False
vectors = [[[-1, -1, 0]], [[1, -1, 0]], [[1, 1, 0]], [[-1, 1, 0]]]
coord = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


lx, ly, lz = np.linspace(-100, 100, 100), np.linspace(-100, 100, 100), np.linspace(-100, 100, 100)
kk = 0
while run:
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, colors['red'], transform(0, 0, 0),
                     transform(coord[0][0], coord[0][1], coord[0][2]), 2)
    pygame.draw.line(screen, colors['green'], transform(0, 0, 0),
                     transform(coord[1][0], coord[1][1], coord[1][2]), 2)
    pygame.draw.line(screen, colors['blue'], transform(0, 0, 0),
                     transform(coord[2][0], coord[2][1], coord[2][2]), 2)
    for i in lx:
        for j in ly:
            for k in lz:
                print(kk)
                kk += 1
                pygame.draw.circle(screen, colors['white'], transform(i, j, k), 1)
    p = []
    for i in range(len(vectors)):
        p.append(transform(vectors[i][0][0], vectors[i][0][1], vectors[i][0][2]))
    # pygame.draw.polygon(screen, colors['royalblue'], p)
    p.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
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
                print(vectors)
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
