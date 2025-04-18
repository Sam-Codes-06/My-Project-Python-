import pygame
from data4 import exit

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
grid_coord = [[(60, 57), (151, 57), (242, 57), (333, 57), (424, 57), (515, 57), (605, 57)],
              [(60, 149), (151, 149), (242, 149), (333, 149), (424, 149), (515, 149), (605, 149)],
              [(60, 241), (151, 241), (242, 241), (333, 241), (424, 241), (515, 241), (605, 241)],
              [(60, 333), (151, 333), (242, 333), (333, 333), (424, 333), (515, 333), (605, 333)],
              [(60, 425), (151, 425), (242, 425), (333, 425), (424, 425), (515, 425), (605, 425)],
              [(60, 517), (151, 517), (242, 517), (333, 517), (424, 517), (515, 517), (605, 517)]]


def transform(c):
    x, y = c
    return (x + (width / 2) - 333, y + (height / 2) - 287)


chance = 1
winner = None
game_over = False
menu = True
current = 0
begin = pygame.time.get_ticks()
font = pygame.font.Font(None, 64)
win_text, go_text = 0, 0
scorey, scorer = 0, 0
for i in range(len(grid_coord)):
    for j in range(len(grid_coord[i])):
        grid_coord[i][j] = transform(grid_coord[i][j])


class goti():
    def __init__(self):
        self.goti = None

    def draw_gotis(self, c):
        x, y = c
        if self.goti == 1:
            color = (255, 255, 0)
        elif self.goti == -1:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.circle(screen, color, (x, y), 35)


show_exit = False
etd = exit.Button('Exit to Desktop', 330, 60, ((width - 330) / 2, 380), 3)
etm = exit.Button('Exit to Main-Menu', 330, 60, ((width - 330) / 2, 300), 3)
cancel = exit.Button('Cancel', 330, 60, ((width - 330) / 2, 460), 3)
gotis = []
for i in range(6):
    gotis.append([goti(), goti(), goti(), goti(), goti(), goti(), goti()])


def draw_game_bg(c):
    global show_exit, etd, etm, cancel


def make_chance():
    global chance, gotis, grid_coord
    a, b = pygame.mouse.get_pos()
    for i in range(len(grid_coord)):
        for j in range(len(grid_coord[i])):
            if a >= grid_coord[i][j][0] - 35 and a <= grid_coord[i][j][0] + 35 and b >= grid_coord[i][j][
                1] - 35 and b <= grid_coord[i][j][1] + 35 and gotis[i][j].goti == None:
                if i < 5:
                    if gotis[i + 1][j].goti != None:
                        if chance == 1:
                            gotis[i][j].goti = 1
                        else:
                            gotis[i][j].goti = -1
                        chance *= -1
                elif i == 5:
                    if chance == 1:
                        gotis[i][j].goti = 1
                    else:
                        gotis[i][j].goti = -1
                    chance *= -1


def dekho_kon_jeeta(gotis):
    for i in range(len(gotis)):
        for j in range(len(gotis[i])):
            if j <= 3 and gotis[i][j].goti == gotis[i][j + 1].goti and gotis[i][j + 1].goti == gotis[i][j + 2].goti and \
                    gotis[i][j + 2].goti == gotis[i][j + 3].goti and gotis[i][j].goti != None:
                return gotis[i][j]
            if i <= 2 and gotis[i][j].goti == gotis[i + 1][j].goti and gotis[i + 1][j].goti == gotis[i + 2][j].goti and \
                    gotis[i + 2][j].goti == gotis[i + 3][j].goti and gotis[i][j].goti != None:
                return gotis[i][j]
            if i >= 3 and j <= 3 and gotis[i][j].goti == gotis[i - 1][j + 1].goti and gotis[i - 1][j + 1].goti == \
                    gotis[i - 2][j + 2].goti and gotis[i - 2][j + 2].goti == gotis[i - 3][j + 3].goti and gotis[i][
                j].goti != None:
                return gotis[i][j]
            if i >= 3 and j >= 3 and gotis[i][j].goti == gotis[i - 1][j - 1].goti and gotis[i - 1][j - 1].goti == \
                    gotis[i - 2][j - 2].goti and gotis[i - 2][j - 2].goti == gotis[i - 3][j - 3].goti and gotis[i][
                j].goti != None:
                return gotis[i][j]

def main():
    global chance, winner, game_over, menu, current, begin, font, win_text, go_text, width, height, scorer, scorey, show_exit, etd, etm, cancel, gotis
    current = pygame.time.get_ticks()
    if show_exit == False:
        if menu == False:
            screen.fill((0, 0, 0))
            a, b = transform((0, 0))
            pygame.draw.rect(screen, (10, 240, 250), (a, b, 666, 574))
            for i in range(len(gotis)):
                for j in range(len(gotis[i])):
                    gotis[i][j].draw_gotis(grid_coord[i][j])
        else:
            screen.fill((10, 240, 250))
            a = font.render('Press Enter to Start.', True, (0, 0, 0))
            screen.blit(a, ((width / 2) - a.get_width() / 2, (height / 2) - 100))
            a = font.render('Press Escape to Exit.', True, (0, 0, 0))
            screen.blit(a, ((width / 2) - a.get_width() / 2, (height / 2) + 50))
    if show_exit == True:
        screen.fill((0, 0, 0))
        etd.draw(screen)
        etm.draw(screen)
        cancel.draw(screen)
        etd.check_click()
        etm.check_click()
        cancel.check_click()
        if cancel.pressed == True:
            cancel.pressed = False
            show_exit = False
        if etd.pressed == True:
            return (scorer, 'whole')
        if etm.pressed == True:
            return (scorer, 'menu')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over == False:
            if menu == False:
                make_chance()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_exit == False:
                if menu == True or winner != None:
                    menu = False
                    chance = 1
                    winner = None
                    game_over = False
                    current = 0
                    begin = pygame.time.get_ticks()
                    font = pygame.font.Font(None, 64)
                    win_text, go_text = 0, 0
                    gotis.clear()
                    show_exit = False
                    for i in range(6):
                        gotis.append([goti(), goti(), goti(), goti(), goti(), goti(), goti()])

            if event.key == pygame.K_ESCAPE:
                if show_exit == True:
                    show_exit = False
                else:
                    show_exit = True
    if winner == None:
        winner = dekho_kon_jeeta(gotis)
        begin = pygame.time.get_ticks()
        if winner != None:
            if winner.goti == -1:
                scorer += 1
            else:
                scorey += 1
    else:
        game_over = True
        if current - begin >= 2000:
            if winner.goti == -1:
                win_text = font.render('Red Won!', True, (255, 0, 0))
            else:
                win_text = font.render('Yellow Won1', True, (255, 255, 0))
            go_text = font.render('Game Over!', True, (0, 0, 0))
    if game_over == True and win_text != 0 and show_exit == False:
        game_over = False
        screen.fill((10, 240, 250))
        a = font.render('Press Enter to Play Again.', True, (0, 0, 0))
        screen.blit(a, ((width / 2) - a.get_width() / 2, (height / 2) - 50))
        a = font.render('Press Escape to Exit.', True, (0, 0, 0))
        screen.blit(a, ((width / 2) - a.get_width() / 2, (height / 2) + 50))
        screen.blit(go_text, ((width / 2) - go_text.get_width() / 2, 10))
        screen.blit(win_text, ((width / 2) - win_text.get_width() / 2, 100))
    pygame.display.update()