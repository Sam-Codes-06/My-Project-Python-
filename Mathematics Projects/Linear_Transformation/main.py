import pygame
from coord import pcoord
from arrow import arrow
import numpy
import webbrowser

pygame.init()
screen = pygame.display.set_mode((0, 0))
run = 1
width, height = screen.get_size()
show_menu = True
scalex, scaley = 50, 50
uv = numpy.array([[1., 0.], [0., 1.]])
nuv = numpy.array([[1., 0.], [0., 1.]])
rateix, rateiy, ratejx, ratejy, ratevx, ratevy = 0, 0, 0, 0, 0, 0
vector = numpy.array([1., 1.])
rvector = numpy.array([1., 1.])
nvector = numpy.array([1., 1.])
fvector = numpy.array([1., 1.])
move_r = 0
speed = 100
matrix_text = pygame.font.Font('freesansbold.ttf', 24)
menu_text1 = pygame.font.Font('freesansbold.ttf', 64)
menu_text2 = pygame.font.Font('freesansbold.ttf', 50)
menu_text3 = pygame.font.Font('freesansbold.ttf', 32)
x1, y1, x2, y2 = (width / 2) + scalex, height / 2, width / 2, (height / 2) - scaley
show_l = 1
move = 0
colors = {"white": (255, 255, 255), "red": (255, 0, 0), "green": (150, 253, 55), "blue": (0, 227, 227),
          "orange": (255, 127, 39),
          "grey": (64, 64, 64), "yellow": (255, 240, 0)}
lh, lv, nlh, nlv, rlv, rlh, ratelh, ratelv = [], [], [], [], [], [], [], []
cant_inv = 0
for i in range(-20, 21):
    lh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
    lv.append(numpy.array([[i, i], [20.0, -20.0]]))
    nlh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
    nlv.append(numpy.array([[i, i], [20.0, -20.0]]))
    rlh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
    rlv.append(numpy.array([[i, i], [20.0, -20.0]]))
    ratelh.append([0.0, 0.0, 0.0, 0.0])
    ratelv.append([0.0, 0.0, 0.0, 0.0])


def locator(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def det(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def approximate():
    global uv, nuv, lh, lv, nlh, nlv
    uv = numpy.round_(uv, 5)
    nuv = numpy.round_(nuv, 5)
    for i in range(41):
        lh[i] = numpy.round_(lh[i], 5)
        nlh[i] = numpy.round_(nlh[i], 5)
        lv[i] = numpy.round_(lv[i], 5)
        nlv[i] = numpy.round_(nlv[i], 5)


text10 = matrix_text.render("Inverse doesnt exist!", True, colors["red"])
text11 = matrix_text.render("Determinant (Area): ", True, colors["white"])

while run:
    screen.fill((0, 0, 0))
    if show_menu == False:
        approximate()
        if move_r == 1:
            n, m = pygame.mouse.get_pos()
            vector[0], vector[1] = (n - width / 2) / scalex, (height / 2 - m) / scaley
            fvector[0], fvector[1] = (n - width / 2) / scalex, (height / 2 - m) / scaley
        for i in range(-20, 21):
            if i == 0:
                l = 3
            else:
                l = 2
            pygame.draw.line(screen, colors["grey"], pcoord((i, 20), scalex, scaley).pcoord,
                             pcoord((i, -20), scalex, scaley).pcoord, l)
            pygame.draw.line(screen, colors["grey"], pcoord((-20, -i), scalex, scaley).pcoord,
                             pcoord((20, -i), scalex, scaley).pcoord, l)
            pygame.draw.line(screen, colors["grey"], pcoord((i - 0.5, 20 - 0.5), scalex, scaley).pcoord,
                             pcoord((i - 0.5, -20 - 0.5), scalex, scaley).pcoord, 1)
            pygame.draw.line(screen, colors["grey"], pcoord((-20 - 0.5, -i - 0.5), scalex, scaley).pcoord,
                             pcoord((20 - 0.5, -i - 0.5), scalex, scaley).pcoord, 1)
        for i in range(41):
            if i == 20:
                l = 3
            else:
                l = 1
            if move == 1:
                if lh[i][0][0] != nlh[i][0][0]:
                    lh[i][0][0] += ratelh[i][0]
                if lh[i][1][0] != nlh[i][1][0]:
                    lh[i][1][0] += ratelh[i][1]
                if lh[i][0][1] != nlh[i][0][1]:
                    lh[i][0][1] += ratelh[i][2]
                if lh[i][1][1] != nlh[i][1][1]:
                    lh[i][1][1] += ratelh[i][3]
                if lv[i][0][0] != nlv[i][0][0]:
                    lv[i][0][0] += ratelv[i][0]
                if lv[i][1][0] != nlv[i][1][0]:
                    lv[i][1][0] += ratelv[i][1]
                if lv[i][0][1] != nlv[i][0][1]:
                    lv[i][0][1] += ratelv[i][2]
                if lv[i][1][1] != nlv[i][1][1]:
                    lv[i][1][1] += ratelv[i][3]
            pygame.draw.line(screen, colors["blue"], pcoord((lh[i][0][0], lh[i][1][0]), scalex, scaley).pcoord,
                             pcoord((lh[i][0][1], lh[i][1][1]), scalex, scaley).pcoord, l)
            pygame.draw.line(screen, colors["blue"], pcoord((lv[i][0][0], lv[i][1][0]), scalex, scaley).pcoord,
                             pcoord((lv[i][0][1], lv[i][1][1]), scalex, scaley).pcoord, l)
        pygame.draw.line(screen, colors["green"], pcoord((0, 0), scalex, scaley).pcoord,
                         pcoord((uv[0][0], uv[1][0]), scalex, scaley).pcoord, 3)
        pygame.draw.polygon(screen, colors["green"], arrow(pcoord((0, 0), scalex, scaley).pcoord,
                                                           pcoord((uv[0][0], uv[1][0]), scalex, scaley).pcoord).p)
        pygame.draw.line(screen, colors["orange"], pcoord((0, 0), scalex, scaley).pcoord,
                         pcoord((uv[0][1], uv[1][1]), scalex, scaley).pcoord, 3)
        pygame.draw.polygon(screen, colors["orange"], arrow(pcoord((0, 0), scalex, scaley).pcoord,
                                                            pcoord((uv[0][1], uv[1][1]), scalex, scaley).pcoord).p)
        pygame.draw.line(screen, colors["yellow"], pcoord((0, 0), scalex, scaley).pcoord,
                         pcoord((vector[0], vector[1]), scalex, scaley).pcoord, 3)
        pygame.draw.polygon(screen, colors["yellow"], arrow(pcoord((0, 0), scalex, scaley).pcoord,
                                                            pcoord((vector[0], vector[1]), scalex, scaley).pcoord).p)
        det(screen, (255, 255, 0, 50),
            pcoord([(0, 0), (uv[0][0], uv[1][0]), (numpy.dot(uv, rvector)), (uv[0][1], uv[1][1])], scalex,
                   scaley).pcoord)
        pygame.draw.circle(screen, colors["white"], (width / 2 + 1, height / 2), 4, 2)
        pygame.draw.circle(screen, (0, 0, 0), (width / 2 + 1, height / 2), 2, 2)
        if show_l == 1:
            locator(screen, (255, 127, 39, 150), (x2, y2), 5)
            locator(screen, (150, 253, 55, 150), (x1, y1), 5)
        if move == 1:
            if uv[0][0] != nuv[0][0]:
                uv[0][0] += rateix
            if uv[1][0] != nuv[1][0]:
                uv[1][0] += rateiy
            if uv[0][1] != nuv[0][1]:
                uv[0][1] += ratejx
            if uv[1][1] != nuv[1][1]:
                uv[1][1] += ratejy
            if numpy.round_(vector[0], 5) != numpy.round_(nvector[0], 5):
                vector[0] += ratevx
            if numpy.round_(vector[1], 5) != numpy.round_(nvector[1], 5):
                vector[1] += ratevy
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = 0
            if event.key == pygame.K_F1:
                if show_menu == True:
                    show_menu = False
                else:
                    show_menu = True
            if show_menu == False:
                if event.key == pygame.K_SPACE:
                    uv = numpy.array([[1., 0.], [0., 1.]])
                    nuv = numpy.array([[1., 0.], [0., 1.]])
                    rateix, rateiy, ratejx, ratejy, ratevx, ratevy = 0, 0, 0, 0, 0, 0
                    vector = numpy.array([1., 1.])
                    rvector = numpy.array([1., 1.])
                    nvector = numpy.array([1., 1.])
                    fvector = numpy.array([1., 1.])
                    x1, y1, x2, y2 = (width / 2) + scalex, height / 2, width / 2, (height / 2) - scaley
                    lh.clear(), lv.clear(), nlh.clear(), nlv.clear(), rlv.clear(), rlh.clear(), ratelh.clear(), ratelv.clear()
                    cant_inv = 0
                    for i in range(-20, 21):
                        lh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
                        lv.append(numpy.array([[i, i], [20.0, -20.0]]))
                        nlh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
                        nlv.append(numpy.array([[i, i], [20.0, -20.0]]))
                        rlh.append(numpy.array([[-20.0, 20.0], [-i, -i]]))
                        rlv.append(numpy.array([[i, i], [20.0, -20.0]]))
                        ratelh.append([0.0, 0.0, 0.0, 0.0])
                        ratelv.append([0.0, 0.0, 0.0, 0.0])
                if event.key == pygame.K_LSHIFT:
                    pygame.mouse.set_pos((vector[0] * scalex) + width / 2, height / 2 - (vector[1] * scaley))
                    move_r = 1
                    ratevx, ratevy = 0.0, 0.0
                if event.key == pygame.K_r:
                    show_l = 1
                    if numpy.round_(numpy.linalg.det(uv), 10) != 0:
                        show_l = 1
                        x1, y1, x2, y2 = (width / 2) + scalex, height / 2, width / 2, (height / 2) - scaley
                        nuv = numpy.round_(numpy.dot(nuv, numpy.linalg.inv(nuv)), 5)
                        nvector = numpy.round_(numpy.dot(nuv, fvector), 5)
                        cant_inv = 0
                        ratejx, ratejy = numpy.round_((nuv[0][1] - uv[0][1]) / speed, 5), numpy.round_(
                            (nuv[1][1] - uv[1][1]) / speed, 5)
                        rateix, rateiy = numpy.round_((nuv[0][0] - uv[0][0]) / speed, 5), numpy.round_(
                            (nuv[1][0] - uv[1][0]) / speed, 5)
                        ratevx, ratevy = (nvector[0] - vector[0]) / speed, (nvector[1] - vector[1]) / speed
                        for i in range(41):
                            nlv[i] = numpy.dot(nuv, rlv[i])
                            nlh[i] = numpy.dot(nuv, rlh[i])
                            ratelh[i] = [numpy.round_((nlh[i][0][0] - lh[i][0][0]) / speed, 5),
                                         numpy.round_((nlh[i][1][0] - lh[i][1][0]) / speed, 5),
                                         numpy.round_((nlh[i][0][1] - lh[i][0][1]) / speed, 5),
                                         numpy.round_((nlh[i][1][1] - lh[i][1][1]) / speed, 5)]
                            ratelv[i] = [numpy.round_((nlv[i][0][0] - lv[i][0][0]) / speed, 5),
                                         numpy.round_((nlv[i][1][0] - lv[i][1][0]) / speed, 5),
                                         numpy.round_((nlv[i][0][1] - lv[i][0][1]) / speed, 5),
                                         numpy.round_((nlv[i][1][1] - lv[i][1][1]) / speed, 5)]
                        move = 1
                    else:
                        show_l = 0
                        cant_inv = 1
                        move = 0
                if event.key == pygame.K_RETURN:
                    if move == 1:
                        move = 0
                    else:
                        show_l = 0
                        nvector = numpy.round_(numpy.dot(nuv, vector), 5)
                        ratevx, ratevy = (nvector[0] - vector[0]) / speed, (nvector[1] - vector[1]) / speed
                        move = 1
                if event.key == pygame.K_UP:
                    n, m = pygame.mouse.get_pos()
                    if m != 0:
                        pygame.mouse.set_pos(n, m - 1)
                if event.key == pygame.K_DOWN:
                    n, m = pygame.mouse.get_pos()
                    if m != height:
                        pygame.mouse.set_pos(n, m + 1)
                if event.key == pygame.K_RIGHT:
                    n, m = pygame.mouse.get_pos()
                    if n != width:
                        pygame.mouse.set_pos(n + 1, m)
                if event.key == pygame.K_LEFT:
                    n, m = pygame.mouse.get_pos()
                    if n != 0:
                        pygame.mouse.set_pos(n - 1, m)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                move_r = 0
        if show_menu == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                show_l = 1
                if event.button == 3 and (x1, y1) != pygame.mouse.get_pos():
                    x1, y1 = pygame.mouse.get_pos()
                    move = 0
                    nuv.itemset((0, 0), (x1 - width / 2) / scalex)
                    nuv.itemset((1, 0), (height / 2 - y1) / scaley)
                    rateix, rateiy = numpy.round_((nuv[0][0] - uv[0][0]) / speed, 5), numpy.round_(
                        (nuv[1][0] - uv[1][0]) / speed, 5)
                    for i in range(41):
                        nlh[i] = numpy.dot(nuv, rlh[i])
                        nlv[i] = numpy.dot(nuv, rlv[i])
                        ratelh[i] = [(nlh[i][0][0] - lh[i][0][0]) / speed, (nlh[i][1][0] - lh[i][1][0]) / speed,
                                     (nlh[i][0][1] - lh[i][0][1]) / speed, (nlh[i][1][1] - lh[i][1][1]) / speed]
                        ratelv[i] = [(nlv[i][0][0] - lv[i][0][0]) / speed, (nlv[i][1][0] - lv[i][1][0]) / speed,
                                     (nlv[i][0][1] - lv[i][0][1]) / speed, (nlv[i][1][1] - lv[i][1][1]) / speed]
                if event.button == 1 and (x2, y2) != pygame.mouse.get_pos():
                    x2, y2 = pygame.mouse.get_pos()
                    move = 0
                    nuv.itemset((0, 1), (x2 - width / 2) / scalex)
                    nuv.itemset((1, 1), (height / 2 - y2) / scaley)
                    ratejx, ratejy = numpy.round_((nuv[0][1] - uv[0][1]) / speed, 5), numpy.round_(
                        (nuv[1][1] - uv[1][1]) / speed, 5)
                    for i in range(41):
                        nlv[i] = numpy.dot(nuv, rlv[i])
                        nlh[i] = numpy.dot(nuv, rlh[i])
                        ratelh[i] = [numpy.round_((nlh[i][0][0] - lh[i][0][0]) / speed, 5),
                                     numpy.round_((nlh[i][1][0] - lh[i][1][0]) / speed, 5),
                                     numpy.round_((nlh[i][0][1] - lh[i][0][1]) / speed, 5),
                                     numpy.round_((nlh[i][1][1] - lh[i][1][1]) / speed, 5)]
                        ratelv[i] = [numpy.round_((nlv[i][0][0] - lv[i][0][0]) / speed, 5),
                                     numpy.round_((nlv[i][1][0] - lv[i][1][0]) / speed, 5),
                                     numpy.round_((nlv[i][0][1] - lv[i][0][1]) / speed, 5),
                                     numpy.round_((nlv[i][1][1] - lv[i][1][1]) / speed, 5)]
        if show_menu == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                if width - x <= 226 and height - y <= 33:
                    run = 0
                    webbrowser.open('https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw')
    if show_menu == False:
        text1 = matrix_text.render("{:.2f}".format(uv[0][0]), True, colors["green"])
        text1_rect = text1.get_rect()
        text2 = matrix_text.render("{:.2f}".format(uv[1][0]), True, colors["green"])
        text2_rect = text2.get_rect()
        text3 = matrix_text.render("{:.2f}".format(uv[0][1]), True, colors["orange"])
        text3_rect = text3.get_rect()
        text4 = matrix_text.render("{:.2f}".format(uv[1][1]), True, colors["orange"])
        text4_rect = text4.get_rect()
        text5 = matrix_text.render("{:.2f}".format(fvector[0]), True, colors["yellow"])
        text5_rect = text5.get_rect()
        text6 = matrix_text.render("{:.2f}".format(fvector[1]), True, colors["yellow"])
        text6_rect = text6.get_rect()
        text7 = matrix_text.render("=", True, colors["white"])
        text7_rect = text7.get_rect()
        text8 = matrix_text.render("{:.2f}".format(vector[0]), True, colors["yellow"])
        text8_rect = text8.get_rect()
        text9 = matrix_text.render("{:.2f}".format(vector[1]), True, colors["yellow"])
        text9_rect = text9.get_rect()
        text12 = matrix_text.render("{:.2f}".format(numpy.linalg.det(uv)), True, colors["yellow"])
        text14 = matrix_text.render(
            "{:.2f}".format(numpy.round_(((vector[0] * vector[0]) + (vector[1] * vector[1])) ** 0.5), 5), True,
            colors["yellow"])
        pygame.draw.polygon(screen, colors["white"],
                            [(15, 5), (5, 5), (5, 75), (15, 75), (15, 73), (7, 73), (7, 7), (15, 7)])
        if text3_rect.width + text1_rect.width >= text4_rect.width + text2_rect.width:
            a = pygame.draw.polygon(screen, colors["white"],
                                    [(120 + text3_rect.width + text1_rect.width - 100, 5),
                                     (130 + text3_rect.width + text1_rect.width - 100, 5),
                                     (130 + text3_rect.width + text1_rect.width - 100, 75),
                                     (120 + text3_rect.width + text1_rect.width - 100, 75),
                                     (120 + text3_rect.width + text1_rect.width - 100, 73),
                                     (128 + text3_rect.width + text1_rect.width - 100, 73),
                                     (128 + text3_rect.width + text1_rect.width - 100, 7),
                                     (120 + text3_rect.width + text1_rect.width - 100, 7)])
        else:
            a = pygame.draw.polygon(screen, colors["white"],
                                    [(120 + text2_rect.width + text4_rect.width - 100, 5),
                                     (130 + text2_rect.width + text4_rect.width - 100, 5),
                                     (130 + text2_rect.width + text4_rect.width - 100, 75),
                                     (120 + text2_rect.width + text4_rect.width - 100, 75),
                                     (120 + text2_rect.width + text4_rect.width - 100, 73),
                                     (128 + text2_rect.width + text4_rect.width - 100, 73),
                                     (128 + text2_rect.width + text4_rect.width - 100, 7),
                                     (120 + text2_rect.width + text4_rect.width - 100, 7)])
        pygame.draw.polygon(screen, colors["white"],
                            [(150 + a.x - 120, 5), (140 + a.x - 120, 5),
                             (140 + a.x - 120, 75), (150 + a.x - 120, 75),
                             (150 + a.x - 120, 73), (142 + a.x - 120, 73),
                             (142 + a.x - 120, 7), (150 + a.x - 120, 7)])
        b = pygame.draw.polygon(screen, colors["white"],
                                [(190 + a.x - 120, 5), (200 + a.x - 120, 5), (200 + a.x - 120, 75),
                                 (190 + a.x - 120, 75),
                                 (190 + a.x - 120, 73), (198 + a.x - 120, 73),
                                 (198 + a.x - 120, 7), (190 + a.x - 120, 7)])
        c = pygame.draw.polygon(screen, colors["white"],
                                [(232 + b.x - 188, 5), (222 + b.x - 188, 5), (222 + b.x - 188, 75),
                                 (232 + b.x - 188, 75),
                                 (232 + b.x - 188, 73), (224 + b.x - 188, 73), (224 + b.x - 188, 7),
                                 (232 + b.x - 188, 7)])
        if text8_rect.width >= text9_rect.width:
            pygame.draw.polygon(screen, colors["white"],
                                [(c.x + text8_rect.width + 4, 5), (c.x + 10 + text8_rect.width + 4, 5),
                                 (c.x + 10 + text8_rect.width + 4, 75), (c.x + text8_rect.width + 4, 75),
                                 (c.x + text8_rect.width + 4, 73), (c.x + 8 + text8_rect.width + 4, 73),
                                 (c.x + 8 + text8_rect.width + 4, 7), (c.x + text8_rect.width + 4, 7)])
        else:
            pygame.draw.polygon(screen, colors["white"],
                                [(c.x + text9_rect.width + 4, 5), (c.x + 10 + text9_rect.width + 4, 5),
                                 (c.x + 10 + text9_rect.width + 4, 75), (c.x + text9_rect.width + 4, 75),
                                 (c.x + text9_rect.width + 4, 73), (c.x + 8 + text9_rect.width + 4, 73),
                                 (c.x + 8 + text9_rect.width + 4, 7), (c.x + text9_rect.width + 4, 7)])
        screen.blit(text1, (12, 10))
        screen.blit(text2, (12, 48))
        screen.blit(text3, (text1_rect.width + 20, 10))
        screen.blit(text4, (text2_rect.width + 20, 48))
        screen.blit(text5, (146 + a.x - 120, 10))
        screen.blit(text6, (146 + a.x - 120, 48))
        screen.blit(text7, (b.x + 16, 26))
        screen.blit(text8, (c.x + 7, 10))
        screen.blit(text9, (c.x + 7, 48))
        screen.blit(text11, (3, 90))
        screen.blit(text12, (235, 90))
        if cant_inv == 1:
            screen.blit(text10, (10, height - 30))
    if show_menu == True:
        m_text1 = menu_text1.render("Greetings!", True, colors["blue"])
        m_text2 = menu_text2.render("Key Bindings", True, colors["white"])
        m_text3 = menu_text2.render("TASK", True, colors["white"])
        m_text4 = menu_text2.render("KEY", True, colors["white"])
        m_text5 = menu_text3.render("Exit Application", True, colors["grey"])
        m_text6 = menu_text3.render("Esc.", True, colors["grey"])
        m_text7 = menu_text3.render("Show/Exit Menu", True, colors["grey"])
        m_text8 = menu_text3.render("F1", True, colors["grey"])
        m_text9 = menu_text3.render("Get Inverse Transformation", True, colors["grey"])
        m_text10 = menu_text3.render("r", True, colors["grey"])
        m_text11 = menu_text3.render("Move Yellow Vector", True, colors["grey"])
        m_text12 = menu_text3.render("Hold L-Shift", True, colors["grey"])
        m_text13 = menu_text3.render("Set Pointer for x vector", True, colors["grey"])
        m_text14 = menu_text3.render("Set Pointer for y vector", True, colors["grey"])
        m_text15 = menu_text3.render("R.M.B.", True, colors["grey"])
        m_text16 = menu_text3.render("L.M.B.", True, colors["grey"])
        m_text17 = menu_text3.render("Move Cursor Up", True, colors["grey"])
        m_text18 = menu_text3.render("Move Cursor Down", True, colors["grey"])
        m_text19 = menu_text3.render("Move Cursor Right", True, colors["grey"])
        m_text20 = menu_text3.render("Move Cursor Left", True, colors["grey"])
        m_text21 = menu_text3.render("Up Arrow", True, colors["grey"])
        m_text22 = menu_text3.render("Down Arrow", True, colors["grey"])
        m_text23 = menu_text3.render("Right Arrow", True, colors["grey"])
        m_text24 = menu_text3.render("Left Arrow", True, colors["grey"])
        m_text25 = menu_text3.render("Reset Graph", True, colors["grey"])
        m_text26 = menu_text3.render("Space", True, colors["grey"])
        m_text27 = menu_text3.render("CREDIT: 3b1b/youtube.", True, colors["blue"])
        screen.blit(m_text1, (width / 2 - 163, 0))
        screen.blit(m_text2, (width / 2 - 160, 90))
        screen.blit(m_text3, (350, 180))
        screen.blit(m_text4, (width - 505, 180))
        screen.blit(m_text5, (350, 260))
        screen.blit(m_text6, (width - 400 - 63, 260))
        screen.blit(m_text7, (350, 310))
        screen.blit(m_text8, (width - 400 - 31, 310))
        screen.blit(m_text9, (350, 360))
        screen.blit(m_text10, (width - 400 - 12, 360))
        screen.blit(m_text11, (350, 410))
        screen.blit(m_text12, (width - 400 - 187, 410))
        screen.blit(m_text13, (350, 460))
        screen.blit(m_text14, (350, 510))
        screen.blit(m_text15, (width - 400 - 97, 460))
        screen.blit(m_text16, (width - 400 - 94, 510))
        screen.blit(m_text17, (350, 560))
        screen.blit(m_text18, (350, 610))
        screen.blit(m_text19, (350, 660))
        screen.blit(m_text20, (350, 710))
        screen.blit(m_text21, (width - 400 - 145, 560))
        screen.blit(m_text22, (width - 400 - 193, 610))
        screen.blit(m_text23, (width - 400 - 187, 660))
        screen.blit(m_text24, (width - 400 - 164, 710))
        screen.blit(m_text25, (350, 760))
        screen.blit(m_text26, (width - 332 - 164, 760))
        screen.blit(m_text27, (width - 365, height - 32))
    pygame.display.update()
pygame.quit()
