import pygame
import random
import math


pygame.init()
white, red, yellow, blue = (255, 255, 255), (240, 0, 0), (255, 242, 0), (0, 162, 232)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
run = 1
fps = pygame.time.Clock()
start, limit = 0, 40
stars, speed = [], 1


class STARS(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.r = 1
        self.col = white
        self.x = x
        self.y = y
        self.speed = speed
        if self.x > 0 and self.x <= width / 2 and self.y > 0 and self.y <= height / 2:
            self.dx, self.dy = width / 2 - self.x, height / 2 - self.y
        if self.x > width / 2 and self.y > 0 and self.y <= height / 2:
            self.dx, self.dy = self.x - width / 2, height / 2 - self.y
        if self.x > 0 and self.x <= width / 2 and self.y > height / 2:
            self.dx, self.dy = width / 2 - self.x, self.y - height / 2
        if self.x > width / 2 and self.y > height / 2:
            self.dx, self.dy = self.x - width / 2, self.y - height / 2
        self.sx = self.dx / math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        self.sy = self.dy / math.sqrt((self.dx * self.dx) + (self.dy * self.dy))


def move():
    global stars
    for i in stars:
        try:
            if i.x > 0 and i.x <= width / 2 and i.y > 0 and i.y <= height / 2:
                i.x += -i.sx * i.speed
                i.y += -i.sy * i.speed
            if i.x > width / 2 and i.y > 0 and i.y <= height / 2:
                i.x += i.sx * i.speed
                i.y += -i.sy * i.speed
            if i.x > 0 and i.x <= width / 2 and i.y > height / 2:
                i.x += -i.sx * i.speed
                i.y += i.sy * i.speed
            if i.x > width / 2 and i.y > height / 2:
                i.x += i.sx * i.speed
                i.y += i.sy * i.speed
            i.speed += 0.2
            i.r += 0.05
        except:
            pass


while run:
    screen.fill((0, 0, 0))
    fps.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if start == 0:
                    start = 1
                else:
                    start = 0
            if event.key == pygame.K_ESCAPE:
                run = 0
            if event.key == pygame.K_UP:
                speed += 0.1
            if event.key == pygame.K_DOWN and speed > 1:
                speed -= 0.1
            if event.key == pygame.K_w:
                limit += 1
            if event.key == pygame.K_s and limit > 10:
                limit -= 1
    if len(stars) <= limit and start == 1:
        stars.append(STARS(random.randint(10, width - 10), random.randint(10, height - 10)))
    if len(stars) > 0:
        for i in range(len(stars)):
            try:
                pygame.draw.circle(screen, stars[i].col, (stars[i].x, stars[i].y), stars[i].r)
                if stars[i].x - stars[i].r < 0 or stars[i].y - stars[i].r < 0 or stars[i].x + stars[i].r > width or \
                        stars[
                            i].y + stars[i].r > height:
                    stars.remove(stars[i])
                    if len(stars) < limit:
                        stars.append(STARS(random.randint(10, width - 10), random.randint(10, height - 10)))
                if stars[i].x == width / 2 or stars[i].y == height / 2:
                    stars.remove(stars[i])
            except:
                pass
    if start == 1:
        move()
    pygame.display.update()
pygame.quit()
