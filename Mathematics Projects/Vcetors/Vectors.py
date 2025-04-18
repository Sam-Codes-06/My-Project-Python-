import Vect2d
import pygame
import math

pygame.init()
run = 1
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
scalex, scaley = 1, 1
menu = pygame.image.load("data/menu.jpg")
sm = 1
a = Vect2d.Vect2d(scalex, scaley, 1)
change = 1
vects = []
show_result = 0
move = 0
sp, ep = 0, 0
dx, dy = 0, 0
font = pygame.font.SysFont('calibri', 25, 1)
while run:
    if sm == 0:
        Vect2d.Vect2d(scalex, scaley, 1)
    if sm == 1:
        screen.fill((255, 255, 255))
        screen.blit(menu, ((width - menu.get_height()) / 2, 0))

    if sm == 0:
        for i in vects:
            pygame.draw.line(screen, (255, 200, 0), i[0][0], i[0][1], 4)
            pygame.draw.circle(screen, (0, 0, 0), (i[0][0][0] + 1, i[0][0][1]), 5)
            pygame.draw.circle(screen, (255, 255, 255), (i[0][0][0] + 1, i[0][0][1]), 3)
            pygame.draw.circle(screen, (0, 0, 0), (i[0][1][0] + 1, i[0][1][1]), 5)
    if show_result == 1 and len(vects) > 0 and type(result) == list:
        text1 = font.render("Magitude = %.3f" % result[1], True, (0, 0, 0),
                            (255, 255, 255))
        angle = result[2] * 180 / math.pi
        text2 = font.render(", \u03B8 = %.3f\N{DEGREE SIGN}" % angle, True, (0, 0, 0), (255, 255, 255))
        screen.blit(text1, (0, height - text1.get_height()))
        screen.blit(text2, (text1.get_width(), height - text2.get_height()))
        pygame.draw.line(screen, (255, 0, 0), result[0][0], result[0][1], 4)
        pygame.draw.circle(screen, (0, 0, 0), (result[0][0][0] + 1, result[0][0][1]), 5)
        pygame.draw.circle(screen, (255, 255, 255), (result[0][0][0] + 1, result[0][0][0]), 3)
        pygame.draw.circle(screen, (0, 0, 0), (result[0][1][0] + 1, result[0][1][1]), 5)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = 0
            if sm == 0:
                if event.key == pygame.K_RETURN:
                    show_result = 1
                    result = a.get_resultant(vects)
                if event.key == pygame.K_SPACE:
                    show_result = 0
                if event.key == pygame.K_r:
                    vects.clear()
                    show_result = 0
                    move = 0
                    sp, ep = 0, 0
                    dx, dy = 0, 0
                if event.key == pygame.K_w and move == 0 and show_result == 0:
                    scaley += 1
                if event.key == pygame.K_s and move == 0 and scaley > 1 and show_result == 0:
                    scaley -= 1
                if event.key == pygame.K_a and move == 0 and scalex > 1 and show_result == 0:
                    scalex -= 1
                if event.key == pygame.K_d and move == 0 and show_result == 0:
                    scalex += 1
                if event.key == pygame.K_UP:
                    x, y = pygame.mouse.get_pos()
                    if y > 0:
                        y -= change
                    pygame.mouse.set_pos(x, y)
                if event.key == pygame.K_DOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < height:
                        y += change
                    pygame.mouse.set_pos(x, y)
                if event.key == pygame.K_RIGHT:
                    x, y = pygame.mouse.get_pos()
                    if x < width:
                        x += change
                    pygame.mouse.set_pos(x, y)
                if event.key == pygame.K_LEFT:
                    x, y = pygame.mouse.get_pos()
                    if x > 0:
                        x -= change
                    pygame.mouse.set_pos(x, y)
                if event.key == pygame.K_RCTRL:
                    change += 1
                if event.key == pygame.K_LCTRL and change > 1:
                    change -= 1
            if event.key == pygame.K_F2:
                if sm == 0:
                    sm = 1
                else:
                    sm = 0
        if event.type == pygame.MOUSEBUTTONDOWN and sm == 0:
            move = 1
            sp = [pygame.mouse.get_pos()]
        if event.type == pygame.MOUSEBUTTONUP and sm == 0:
            move = 0
    if move == 1 and sp != 0 and sm == 0:
        show_result = 0
        x, y = pygame.mouse.get_pos()
        sx, sy = (sp[0][0] - width / 2) * scalex / 100, (height / 2 - sp[0][1]) * scaley / 100
        ex, ey = (x - width / 2) * scalex / 100, (height / 2 - y) * scaley / 100
        l = a.get_vect((sx, sy), (ex, ey))[1]
        angle = a.get_vect((sx, sy), (ex, ey))[2] * 180 / math.pi
        text1 = font.render("Magitude = %.3f" % l, True, (0, 0, 0),
                            (255, 255, 255))
        text2 = font.render(", \u03B8 = %.3f\N{DEGREE SIGN}" % angle, True, (0, 0, 0), (255, 255, 255))
        screen.blit(text1, (0, height - text1.get_height()))
        screen.blit(text2, (text1.get_width(), height - text2.get_height()))
        pygame.draw.line(screen, (255, 200, 0), (sp[0][0] - 1, sp[0][1]), (x - 1, y), 4)
        pygame.draw.circle(screen, (0, 0, 0), (sp[0][0], sp[0][1]), 5)
        pygame.draw.circle(screen, (255, 255, 255), (sp[0][0], sp[0][1]), 3)
    if move == 0 and sp != 0 and sm == 0:
        ep = [pygame.mouse.get_pos()]
        vects.append(a.get_vect(((sp[0][0] - width / 2 - 1) * scalex / 100, (height / 2 - sp[0][1]) * scaley / 100),
                                ((ep[0][0] - width / 2 - 1) * scalex / 100, (height / 2 - ep[0][1]) * scaley / 100)))
        sp = 0
        result = a.get_resultant(vects)
    pygame.display.update()
pygame.quit()
