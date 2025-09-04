import pygame
import math


class Vect2d(pygame.sprite.Sprite):
    def __init__(self, x=1, y=1, show=1):
        global width, height, screen, sx, sy
        sx, sy = x, y
        super().__init__()
        if x <= 0 or y <= 0:
            raise Exception("Scale must be greater than 0.")
        if type(show) == float or show > 1 or show < 0:
            raise Exception("Third argument must be bool.")
        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()
        screen = pygame.display.get_surface()
        font1 = pygame.font.SysFont('calibri', 18)
        font2 = pygame.font.SysFont('calibri', 18, 1)
        ox, oy = font2.render("0", True, (255, 0, 0)), font2.render("0", True, (0, 0, 255))
        al = (width / 2) - 10
        ar = (width / 2) + 10
        bt = (height / 2) - 10
        bd = (height / 2) + 10
        mx, my = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        for i in range(int(width / 20)):
            if (width / 2 - al) % 50 != 0:
                pygame.draw.line(screen, (100, 100, 100), (al, 0), (al, height), 1)
            elif (width / 2 - al) % 100 == 0:
                pygame.draw.line(screen, (0, 0, 0), (al, 0), (al, height), 3)
                xlc = font2.render(f"{(al - width / 2) * x / 100}", True, (255, 0, 0))
                screen.blit(xlc, (al, height / 2 + 3))
            elif (width / 2 - al) % 50 == 0:
                pygame.draw.line(screen, (0, 0, 0), (al, 0), (al, height), 2)
            al -= 10
        for i in range(int(width / 20)):
            if (ar - width / 2) % 50 != 0:
                pygame.draw.line(screen, (100, 100, 100), (ar, 0), (ar, height), 1)
            elif (ar - width / 2) % 100 == 0:
                pygame.draw.line(screen, (0, 0, 0), (ar, 0), (ar, height), 3)
                xrc = font2.render(f"{(ar - width / 2) * x / 100}", True, (255, 0, 0))
                screen.blit(xrc, (ar, height / 2 + 3))
            elif (ar - width / 2) % 50 == 0:
                pygame.draw.line(screen, (0, 0, 0), (ar, 0), (ar, height), 2)
            ar += 10
        for i in range(int(height / 20)):
            if (height / 2 - bt) % 50 != 0:
                pygame.draw.line(screen, (100, 100, 100), (0, bt), (width, bt), 1)
            elif (height / 2 - bt) % 100 == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, bt), (width, bt), 3)
                ytc = font2.render(f"{(height / 2 - bt) * y / 100}", True, (0, 0, 255))
                screen.blit(ytc, (width / 2 + 3, bt))
            elif (height / 2 - bt) % 50 == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, bt), (width, bt), 2)
            bt -= 10
        for i in range(int(height / 20)):
            if (bd - height / 2) % 50 != 0:
                pygame.draw.line(screen, (100, 100, 100), (0, bd), (width, bd), 1)
            elif (bd - height / 2) % 100 == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, bd), (width, bd), 3)
                ydc = font2.render(f"{(height / 2 - bd) * y / 100}", True, (0, 0, 255))
                screen.blit(ydc, (width / 2 + 3, bd))
            elif (bd - height / 2) % 50 == 0:
                pygame.draw.line(screen, (0, 0, 0), (0, bd), (width, bd), 2)
            bd += 10
        if mx - 2 <= width / 2 and my <= height / 2:
            cx, cy = mx - width / 2, height / 2 - my
        if mx - 2 > width / 2 and my <= height / 2:
            cx, cy = mx - width / 2, height / 2 - my
        if mx - 2 <= width / 2 and my > height / 2:
            cx, cy = mx - width / 2, height / 2 - my
        if mx - 2 > width / 2 and my > height / 2:
            cx, cy = mx - width / 2, height / 2 - my
        pygame.draw.line(screen, (0, 0, 0), (width / 2, 0),
                         (width / 2, height), 4)
        pygame.draw.line(screen, (0, 0, 0), (0, height / 2),
                         (width, height / 2), 4)
        screen.blit(ox, (width / 2 + 4, height / 2 + 3))
        screen.blit(oy, (width / 2 + 4, height / 2 - 18))
        cx, cy = ((cx - 1) * x / 100), cy * y / 100
        text = font1.render(f"{cx, cy}", True, (0, 0, 0), (255, 255, 255))
        if mx - text.get_width() / 2 <= 0:
            mx = text.get_width() / 2
        if my - 20 <= 0:
            my = 20
        if mx >= width - text.get_width() / 2:
            mx = width - text.get_width() / 2
        if show == 1:
            screen.blit(text, (mx - text.get_width() / 2, my - 20))

    def get_vect(self, a, b):
        if type(a) != tuple or type(b) != tuple:
            if type(a) == int or type(b) == int or type(a) == float or type(b) == float:
                pass
            else:
                raise Exception("Incorrect Argument.")
        if type(b) != tuple:
            if b < -math.pi or b > math.pi:
                raise Exception("angle must be between -pi and pi")
        if type(a) == tuple or type(b) == tuple:
            lista = [a[0], a[1]]
            listb = [b[0], b[1]]
            value = math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
            deltax = []
            deltay = []
            if a[0] <= 0 and a[1] > 0:
                lista[0] = lista[0] * 100 / sx + width / 2 - 1
                lista[1] = height / 2 - lista[1] * 100 / sy
                deltax.append(lista[0] - width / 2 - 1)
                deltay.append(height / 2 - lista[1])
            elif a[0] > 0 and a[1] > 0:
                lista[0] = lista[0] * 100 / sx + width / 2 - 1
                lista[1] = height / 2 - lista[1] * 100 / sy
                deltax.append(lista[0] - width / 2 - 1)
                deltay.append(height / 2 - lista[1])
            elif a[0] <= 0 and a[1] <= 0:
                lista[0] = lista[0] * 100 / sx + width / 2 - 1
                lista[1] = height / 2 - lista[1] * 100 / sy
                deltax.append(lista[0] - width / 2 - 1)
                deltay.append(height / 2 - lista[1])
            elif a[0] > 0 and a[1] <= 0:
                lista[0] = lista[0] * 100 / sx + width / 2 - 1
                lista[1] = height / 2 - lista[1] * 100 / sy
                deltax.append(lista[0] - width / 2 - 1)
                deltay.append(height / 2 - lista[1])
            if b[0] <= 0 and b[1] > 0:
                listb[0] = listb[0] * 100 / sx + width / 2 - 1
                listb[1] = height / 2 - listb[1] * 100 / sy
                deltax.append(listb[0] - width / 2 - 1)
                deltay.append(height / 2 - listb[1])
            elif b[0] > 0 and b[1] > 0:
                listb[0] = listb[0] * 100 / sx + width / 2 - 1
                listb[1] = height / 2 - listb[1] * 100 / sy
                deltax.append(listb[0] - width / 2 - 1)
                deltay.append(height / 2 - listb[1])
            elif b[0] <= 0 and b[1] <= 0:
                listb[0] = listb[0] * 100 / sx + width / 2 - 1
                listb[1] = height / 2 - listb[1] * 100 / sy
                deltax.append(listb[0] - width / 2 - 1)
                deltay.append(height / 2 - listb[1])
            elif b[0] > 0 and b[1] <= 0:
                listb[0] = listb[0] * 100 / sx + width / 2 - 1
                listb[1] = height / 2 - listb[1] * 100 / sy
                deltax.append(listb[0] - width / 2 - 1)
                deltay.append(height / 2 - listb[1])
            dx = deltax[1] - deltax[0]
            dy = deltay[1] - deltay[0]
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle = -angle
            if angle > math.pi / 2:
                angle = math.pi - angle
            if dx < 0 and dy > 0:
                angle = math.pi - angle
            elif dx == 0 and dy > 0:
                angle = math.pi / 2
            elif dx > 0 and dy > 0:
                angle = angle
            elif dx > 0 and dy == 0:
                angle = 0
            elif dx > 0 and dy < 0:
                angle = -angle
            elif dx == 0 and dy < 0:
                angle = -angle
            elif dx < 0 and dy < 0:
                angle = -(math.pi - angle)
            elif dx < 0 and dy == 0:
                angle = math.pi
            return [
                [(lista[0] + 1, lista[1]), (listb[0] + 1, listb[1])],
                value, angle, dx, dy, a, b]
        if type(a) == int or type(a) == float and b >= -math.pi and b <= math.pi:
            theta = b
            f = (0, 0)
            dx, dy = a * math.cos(b) * 100 / sx, a * math.sin(b) * 100 / sy
            if b == math.pi or b == -math.pi:
                b = math.pi
                lx = width / 2 - a * 100 / sx
                ly = height / 2
                e = ((lx - width / 2) * sx / 100, 0)
            elif b == 0:
                b = 0
                lx = width / 2 + a * 100 / sx
                ly = height / 2
                e = ((lx - width / 2) * sx / 100, 0)
            elif b == -math.pi / 2:
                b = math.pi / 2
                lx = width / 2
                ly = height / 2 + a * 100 / sy
                e = (0, (height / 2 - ly) * sy / 100)
            elif b == math.pi / 2:
                b = math.pi / 2
                lx = width / 2
                ly = height / 2 - a * 100 / sy
                e = (0, (height / 2 - ly) * sy / 100)
            elif b > math.pi / 2 and b < math.pi:
                b = math.pi - b
                lx = width / 2 - a * math.cos(b) * 100 / sx
                ly = height / 2 - a * math.sin(b) * 100 / sy
                e = ((lx - width / 2) * sx / 100, (height / 2 - ly) * sy / 100)
            elif b < math.pi / 2 and b > 0:
                b = b
                lx = width / 2 + a * math.cos(b) * 100 / sx
                ly = height / 2 - a * math.sin(b) * 100 / sy
                e = ((lx - width / 2) * sx / 100, (height / 2 - ly) * sy / 100)
            elif b < 0 and b > -math.pi / 2:
                b = -b
                lx = width / 2 + a * math.cos(b) * 100 / sx
                ly = height / 2 + a * math.sin(b) * 100 / sy
                e = ((lx - width / 2) * sx / 100, (height / 2 - ly) * sy / 100)
            elif b < -math.pi / 2 and b > -math.pi:
                b = -b
                b = math.pi - b
                lx = width / 2 - a * math.cos(b) * 100 / sx
                ly = height / 2 + a * math.sin(b) * 100 / sy
                e = ((lx - width / 2) * sx / 100, (height / 2 - ly) * sy / 100)
            return [[(width / 2, height / 2), (lx, ly)], a, theta,
                    dx, dy, f, e]

    def get_resultant(self, vects):
        for i in range(len(vects)):
            if len(vects[i]) != 7 or len(vects[i][0]) != 2 or type(vects[i][0][0]) != tuple or type(
                    vects[i][0][1]) != tuple or type(
                vects[i][len(vects[i]) - 1]) != tuple or type(vects[i][len(vects[i]) - 2]) != tuple:
                raise Exception("Argument must be a list of vectors")
        if len(vects) == 1:
            return vects[0]
        elif len(vects) > 1:
            rsp, rep, rdx, rdy, rda, rm, ra, rb = 0, 0, 0, 0, 0, 0, vects[0][5], 0
            for i in range(len(vects)):
                rdx += vects[i][3]
                rdy += vects[i][4]
            rm = math.sqrt(((rdx * sx) / 100 * (rdx * sx) / 100) + ((rdy / 100) * (sy / 100) * rdy))
            ta = math.atan2(rdy, rdx)
            if ta < 0:
                ta = -ta
            if ta > math.pi / 2:
                ta = math.pi - ta
            if rdx <= 0 and rdy > 0:
                rt = math.pi - math.atan2(rdy, -rdx)
            if rdx == 0 and rdy > 0:
                rt = math.pi / 2
            if rdx > 0 and rdy > 0:
                rt = math.atan2(rdy, rdx)
            if rdx > 0 and rdy == 0:
                rt = 0
            if rdx > 0 and rdy <= 0:
                rt = -math.atan2(-rdy, rdx)
            if rdx == 0 and rdy <= 0:
                rt = -math.pi / 2
            if rdx <= 0 and rdy <= 0:
                rt = math.atan2(-rdy, -rdx) - math.pi
            if rdx <= 0 and rdy == 0:
                rt = math.pi
            if rdx <= 0:
                epx = -math.cos(ta) * rm * 100 / sx
            elif rdx > 0:
                epx = math.cos(ta) * rm * 100 / sx
            if rdy <= 0:
                epy = -math.sin(ta) * rm
            elif rdy > 0:
                epy = math.sin(ta) * rm
            rsp = (vects[0][0][0][0] + 1, vects[0][0][0][1])
            rep = (rsp[0] + rdx, (rsp[1] - rdy))
            rb = (epx * sx / 100, epy * sy / 100)
            return [[rsp, rep], rm, rt, rdx, rdy, ra, rb]