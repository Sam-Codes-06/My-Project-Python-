import pygame
from data1 import exit
from data1 import tile
import random

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
grid_ = []
check = []
grid_coord = [[(24, 24), (164, 24), (304, 24), (444, 24)],
              [(24, 164), (164, 164), (304, 164), (444, 164)],
              [(24, 304), (164, 304), (304, 304), (444, 304)],
              [(24, 444), (164, 444), (304, 444), (444, 444)]]
dir = None
moved_up = None
moved_down = None
moved_left = None
moved_right = None
movable = t = False
adding = False
game_over = False
swap = pygame.mixer.Sound(r'data1/swap.mp3')
font1 = pygame.font.Font('freesansbold.ttf', 48)
sound = True
sound_on = pygame.image.load('data1/sound_on.png')
sound_off = pygame.image.load('data1/sound_off.png')
exit_ = pygame.image.load('data1/power.png')
exit_menu = False
etd = exit.Button('Exit to Desktop', 330, 60, ((width - 330) / 2, 380), 3)
etm = exit.Button('Exit to Main-Menu', 330, 60, ((width - 330) / 2, 300), 3)
cancel = exit.Button('Cancel', 330, 60, ((width - 330) / 2, 460), 3)
game_over_menu = False
change = True
pause = False

def transform(x, y):
    return x - 300 + (width / 2), y - 300 + height / 2


def get_tile():
    global v, n, m
    a, b = random.randint(0, 3), random.randint(0, 3)
    if grid[a][b] == 0:
        if random.randint(1, 10) == 10:
            grid[a][b] = 4
        else:
            grid[a][b] = 2
        if change == True:
            v, n, m = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        if started == True and sound:
            pygame.mixer.Sound.play(swap)
    else:
        get_tile()


def move_up(r, c):
    global grid, moved_up
    if grid[r][c] != 0 and grid[r - 1][c] == 0 and r != 0:
        f = grid[r][c]
        grid[r - 1][c] = f
        grid[r][c] = 0
        moved_up = False


def move_down(r, c):
    global grid, moved_down
    if grid[r][c] != 0 and r != 3 and grid[r + 1][c] == 0:
        f = grid[r][c]
        grid[r + 1][c] = f
        grid[r][c] = 0
        moved_down = False


def move_left(r, c):
    global grid, moved_left
    if c != 0 and grid[r][c - 1] == 0 and grid[r][c] != 0:
        f = grid[r][c]
        grid[r][c - 1] = f
        grid[r][c] = 0
        moved_left = False


def move_right(r, c):
    global grid, moved_right
    if c != 3 and grid[r][c] != 0 and grid[r][c + 1] == 0:
        f = grid[r][c]
        grid[r][c + 1] = f
        grid[r][c] = 0
        moved_right = False


def add(di, check_=False):
    global adding, check, grid, score, change
    adding = False
    if check_ == True:
        demo = grid.copy()
    if di == 'up':
        for i in range(4):
            for j in range(4):
                if j < 3 and grid[j][i] == grid[j + 1][i] and grid[j][i] != 0:
                    grid[j][i] *= 2
                    score += grid[j][i]
                    grid[j + 1][i] = 0
                    adding = True
                move_up(j, i)
    elif di == 'down':
        for i in range(3, -1, -1):
            for j in range(3, -1, -1):
                if j > 0 and grid[j][i] == grid[j - 1][i] and grid[j][i] != 0:
                    grid[j][i] *= 2
                    score += grid[j][i]
                    grid[j - 1][i] = 0
                    adding = True
                move_down(j, i)
    elif di == 'left':
        for i in range(0, 4):
            for j in range(0, 4):
                if j < 3 and grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    score += grid[i][j]
                    grid[i][j + 1] = 0
                    adding = True
                move_left(i, j)
    elif di == 'right':
        for i in range(3, -1, -1):
            for j in range(3, -1, -1):
                if j > 0 and grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                    grid[i][j] *= 2
                    score += grid[i][j]
                    grid[i][j - 1] = 0
                    adding = True
                move_right(i, j)
    if check_ == True:
        grid = demo.copy()


def check_():
    global game_over
    game_over = True
    for i in range(4):
        for j in range(4):
            if j < 3 and grid[j][i] == grid[j + 1][i] and grid[j][i] != 0:
                game_over = False
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            if j > 0 and grid[j][i] == grid[j - 1][i] and grid[j][i] != 0:
                game_over = False
    for i in range(0, 4):
        for j in range(0, 4):
            if j < 3 and grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                game_over = False
    for i in range(3, -1, -1):
        for j in range(3, -1, -1):
            if j > 0 and grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                game_over = False


started = False
get_tile()
get_tile()
v, n, m = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
started = True
score = 0
menu = True
current = 0
scores = [0]

def main():
    global grid, grid_, dir, moved_down, moved_left, scores, movabl, t, moved_right, moved_up, adding, check, pause, game_over, v, n, m, menu, sound, exit_menu, etd, etm, cancel, begin, current, game_over_menu, change, score, started

    screen.fill((v, n, m))
    if exit_menu == True:
        screen.fill((0, 0, 0))
        etd.draw(screen)
        etm.draw(screen)
        cancel.draw(screen)
        etd.check_click()
        etm.check_click()
        cancel.check_click()
        if cancel.pressed == True:
            cancel.pressed = False
            exit_menu = False
        if etd.pressed == True:
            etd.pressed = False
            return (max(scores), 'whole')
        if etm.pressed == True:
            return (max(scores), 'menu')
    if menu == True and exit_menu == False:
        menu_text = font1.render(f'Press Enter to Start', True, (0, 0, 0))
        screen.blit(menu_text, ((width / 2) - 235, (height / 2) - 60))
        screen.blit(exit_, (width - 65, 0))
        if sound:
            screen.blit(sound_on, (width - 129, 0))
        else:
            screen.blit(sound_off, (width - 129, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if menu == True or game_over_menu == True or pause == True:
            a, b = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] == True:
                if a >= width - 129 and a <= width - 64 and b >= 0 and b <= 63 and (menu == True or game_over_menu == True):
                    if sound == True:
                        sound = False
                    else:
                        sound = True
                if a >= width - 65 and a <= width - 1 and b >= 0 and b <= 63 and (menu == True or game_over_menu == True):
                    exit_menu = True
                if pause == True:
                    if a >= width - 65 and a <= width - 1 and b >= 0 and b <= 63:
                        if sound == True:
                            sound = False
                        else:
                            sound = True
        if event.type == pygame.KEYDOWN:
            grid_ = grid.copy()
            if event.key == pygame.K_RETURN:
                if menu == True:
                    menu = False
                if game_over_menu == True:
                    game_over = False
                    game_over_menu = False
                    grid = [[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]
                    score = 0
                    started = False
                    get_tile()
                    get_tile()
                    v, n, m = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    started = True
            if event.key == pygame.K_SPACE:
                if change == True:
                    change = False
                else:
                    change = True
            if menu == False and game_over_menu == False:
                if event.key == pygame.K_ESCAPE:
                    if pause == False:
                        pause = True
                    else:
                        pause = False
            if dir == None and menu == False:
                if event.key == pygame.K_UP:
                    dir = 'up'
                    pause = False
                if event.key == pygame.K_DOWN:
                    dir = 'down'
                    pause = False
                if event.key == pygame.K_LEFT:
                    dir = 'left'
                    pause = False
                if event.key == pygame.K_RIGHT:
                    dir = 'right'
                    pause = False
    if menu == False and game_over_menu == False:
        pygame.time.Clock().tick(100)
        score_text = font1.render(f'Score: {score}', True, colors['white'])
        screen.blit(score_text, (10, 10))
        for i in range(4):
            for j in range(4):
                a, b = transform(grid_coord[i][j][0], grid_coord[i][j][1])
                t = tile.Button(f'{grid[i][j]}', 130, 130, (a, b))
                t.draw(screen)
                check.append(grid[i][j])
        for a, b in zip(range(0, 4), range(3, -1, -1)):
            for c, d in zip(range(0, 4), range(3, -1, -1)):
                if dir == 'up':
                    move_up(a, c)
                elif dir == 'down':
                    move_down(b, d)
                elif dir == 'left':
                    move_left(a, c)
                elif dir == 'right':
                    move_right(b, d)
        if dir != None:
            if moved_up == None and dir == 'up':
                add(dir)
                dir = None
                if grid_ != grid or adding == True:
                    get_tile()
            elif moved_down == None and dir == 'down':
                add(dir)
                dir = None
                if grid_ != grid or adding == True:
                    get_tile()
            elif moved_left == None and dir == 'left':
                add(dir)
                dir = None
                if grid_ != grid or adding == True:
                    get_tile()
            elif moved_right == None and dir == 'right':
                add(dir)
                dir = None
                if grid_ != grid or adding == True:
                    get_tile()
        grid_.clear()
        moved_up, moved_down, moved_left, moved_right, adding = None, None, None, None, False
        if 0 not in check:
            check_()
        if game_over == False:
            begin = pygame.time.get_ticks()
        if game_over == True and game_over_menu == False:
            current = pygame.time.get_ticks()
            if current - begin >= 2000:
                begin = pygame.time.get_ticks()
                game_over_menu = True
        check.clear()
    if game_over_menu == True:
        if exit_menu == False:
            if score not in scores:
                scores.append(score)
            game_over_text = font1.render('Game Over!', True, (0, 0, 0))
            screen.blit(game_over_text, ((width / 2) - game_over_text.get_width() / 2, (height / 2) - 90))
            game_over_score_text = font1.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(game_over_score_text, ((width / 2) - game_over_score_text.get_width() / 2, (height / 2) - 35))
            menu_text = font1.render(f'Press Enter to Start', True, (0, 0, 0))
            screen.blit(menu_text, ((width / 2) - 233, (height / 2) + 20))
        screen.blit(exit_, (width - 65, 0))
        if sound:
            screen.blit(sound_on, (width - 129, 0))
        else:
            screen.blit(sound_off, (width - 129, 0))
    if pause == True:
        if sound:
            screen.blit(sound_on, (width - 65, 0))
        else:
            screen.blit(sound_off, (width - 65, 0))
    pygame.display.update()

while True:
    main()
