import pygame, math, time

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()


def transform(x, y):
    return (x * 10, (height - 100) - (y * 10))


run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
x, y, u, g, t, a = 0, 0, 20, -9.8, 0, math.pi / 3
start = False
while run:
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (0, 154, 23), (0, height - 100, width, 100))
    pygame.draw.circle(screen, colors['red'], transform(x, y), 5)
    if start and y >= 0:
        p = time.time() - t
        x = u * math.cos(a) * p
        y = u * math.sin(a) * p + g * p * p / 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                x, y, u, g, t, a = 0, 0, 20, -9.8, 0, math.pi / 3

                start = False
                t = time.time()
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                start = True
                t = time.time()
    pygame.display.update()
pygame.quit()
