import pygame
import random
from data2 import exit

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0))
width, height = screen.get_size()


def transform_(c):
    x, y = c
    return (x + (width / 2) - 150, y + (height / 2) - 300)


shapes = [0, 1, 2, 3, 4, 5, 6]
types = [0, 1, 2, 3]
blocks = [0 for n in range(465)]
block_rects = []
fps = 1
speed_up = False
fixed_rect = []
fixed_rect_colour = []
fixed_rect_check = []
future_block = ((random.randint(1, 96)) % 6) + 1
x = 0
y = 0
for a in range(450, 465):
    fixed_rect.append(a)
gp = 0
bg1 = pygame.transform.scale(pygame.image.load("data2/bg.jpeg"), (300, 600))
bg2 = pygame.transform.scale(pygame.image.load("data2/blocks.png"), (width, height))
# blocks
blue = pygame.transform.scale(pygame.image.load("data2/blue.png"), (20, 20))
cyan = pygame.transform.scale(pygame.image.load("data2/cyan.png"), (20, 20))
green = pygame.transform.scale(pygame.image.load("data2/green.png"), (20, 20))
red = pygame.transform.scale(pygame.image.load("data2/red.png"), (20, 20))
yellow = pygame.transform.scale(pygame.image.load("data2/yellow.png"), (20, 20))
purple = pygame.transform.scale(pygame.image.load("data2/purple.png"), (20, 20))
orange = pygame.transform.scale(pygame.image.load("data2/orange.png"), (20, 20))
audio = True
menu = True
font = pygame.font.Font(None, 48)
show_exit = False
score = 0
scores = [0]
roko = False
for a in range(31):
    for f in range(15):
        gp += 1
        a, b = transform_((x, y))
        re = pygame.Rect(a, b, 20, 20)
        block_rects.append(re)
        fixed_rect_check.append(0)
        fixed_rect_colour.append(0)
        x += 20
    y += 20
    x = 0
fix, change, move_, game_over_sound = pygame.mixer.Sound('data2/set.mp3'), pygame.mixer.Sound(
    'data2/change.mp3'), pygame.mixer.Sound('data2/move.mp3'), pygame.mixer.Sound('data2/game_over.mp3')
game_over = False
game_over_ = False


class Shapes:
    def __init__(self, main_block, q):
        self.main_block = main_block
        self.q = q
        self.movement_counter = 0
        self.parts = []
        self.type = 1
        self.coll = False

    def draw_shapes(self, block):
        global score
        global blocks, fixed_rect
        if self.type > 4:
            self.type = 1
        if self.q == 1:
            if self.type == 1 or self.type == 3:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 2, self.main_block - 1]
            if self.type == 2 or self.type == 4:
                self.parts = [self.main_block, self.main_block - 15, self.main_block + 15, self.main_block + 30]
        if self.q == 2:
            if self.type == 1:
                self.parts = [self.main_block, self.main_block + 1, self.main_block - 1, self.main_block - 16]
            if self.type == 2:
                self.parts = [self.main_block, self.main_block + 15, self.main_block - 15, self.main_block - 14]
            if self.type == 3:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 16, self.main_block - 1]
            if self.type == 4:
                self.parts = [self.main_block, self.main_block + 15, self.main_block + 14, self.main_block - 15]

        if self.q == 3:
            if self.type == 1:
                self.parts = [self.main_block, self.main_block + 1, self.main_block - 1, self.main_block - 14]
            if self.type == 2:
                self.parts = [self.main_block, self.main_block + 15, self.main_block - 15, self.main_block + 16]
            if self.type == 3:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 14, self.main_block - 1]
            if self.type == 4:
                self.parts = [self.main_block, self.main_block + 15, self.main_block - 16, self.main_block - 15]

        if self.q == 4:
            self.parts = [self.main_block, self.main_block + 1, self.main_block - 15, self.main_block - 14]

        if self.q == 5:
            if self.type == 1 or self.type == 3:
                self.parts = [self.main_block, self.main_block - 1, self.main_block - 15, self.main_block - 14]
            if self.type == 2 or self.type == 4:
                self.parts = [self.main_block, self.main_block + 1, self.main_block - 15, self.main_block + 16]

        if self.q == 6:
            if self.type == 1:
                self.parts = [self.main_block, self.main_block + 1, self.main_block - 15, self.main_block - 1]
            if self.type == 2:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 15, self.main_block - 15]
            if self.type == 3:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 15, self.main_block - 1]
            if self.type == 4:
                self.parts = [self.main_block, self.main_block - 1, self.main_block + 15, self.main_block - 15]
        if self.q == 7:
            if self.type == 1 or self.type == 3:
                self.parts = [self.main_block, self.main_block + 1, self.main_block - 15, self.main_block - 16]
            if self.type == 2 or self.type == 4:
                self.parts = [self.main_block, self.main_block + 1, self.main_block + 15, self.main_block - 14]

        for part in self.parts:
            block[part] = self.q

        if self.movement_counter >= 20:
            self.movement_counter = 0
            self.main_block += 15
            blocks = [0 for n in range(465)]
            self.collide()

    def collide(self):
        global block_rects, fixed_rect, fixed_rect_check, score
        for part in self.parts:
            for x in fixed_rect:
                if block_rects[part] == block_rects[x - 15]:
                    self.coll = True
        if self.coll == True:
            score += 10
            for part in self.parts:
                fixed_rect.append(part)
                fixed_rect_colour[part] = self.q
                fixed_rect_check[part] = 1
            csll()

    def draw_fixed_rect(self):
        global blocks, fixed_rect, fixed_rect_colour
        for x in fixed_rect:
            blocks[x] = fixed_rect_colour[x]


def clear_line():
    global fixed_rect, fixed_rect_check, fixed_rect_colour, score
    full_line = None
    add = False
    temp_block = []
    for x in blocks:
        temp_block.append(x)
    temp_rect_color = []
    for v in fixed_rect_colour:
        temp_rect_color.append(v)
    temp_fixed_rect = []
    for b in fixed_rect:
        temp_fixed_rect.append(b)
    for x in range(0, 30):
        if fixed_rect_check[x * 15] == fixed_rect_check[x * 15 + 1] == fixed_rect_check[x * 15 + 2] == fixed_rect_check[
            x * 15 + 3] == fixed_rect_check[x * 15 + 4] == fixed_rect_check[x * 15 + 5] == fixed_rect_check[
            x * 15 + 6] == fixed_rect_check[x * 15 + 7] == fixed_rect_check[x * 15 + 8] == fixed_rect_check[
            x * 15 + 9] == fixed_rect_check[x * 15 + 10] == fixed_rect_check[x * 15 + 11] == fixed_rect_check[
            x * 15 + 12] == fixed_rect_check[x * 15 + 13] == fixed_rect_check[x * 15 + 14] == 1:
            add = True
            full_line = x
    for i in temp_fixed_rect:
        if i // 15 == full_line:
            fixed_rect_colour[i] = 0
            fixed_rect.remove(i)
            blocks[i] = 0
    for i in temp_fixed_rect:
        if full_line != None and i // 15 < full_line:
            fixed_rect[fixed_rect.index(i)] = i + 15
            fixed_rect_colour[i + 15] = temp_rect_color[i]
            blocks[i + 15] = temp_block[i]
    check_rect()
    x = full_line
    fixed_rect_check[x * 15] = fixed_rect_check[x * 15 + 1] = fixed_rect_check[x * 15 + 2] = \
        fixed_rect_check[
            x * 15 + 3] = fixed_rect_check[x * 15 + 4] = fixed_rect_check[x * 15 + 5] = fixed_rect_check[
        x * 15 + 6] = fixed_rect_check[x * 15 + 7] = fixed_rect_check[x * 15 + 8] = fixed_rect_check[
        x * 15 + 9] = fixed_rect_check[x * 15 + 10] = fixed_rect_check[x * 15 + 11] = fixed_rect_check[
        x * 15 + 12] = fixed_rect_check[x * 15 + 13] = fixed_rect_check[x * 15 + 14] = 0
    full_line = None
    if add == True:
        score += 50
        add = False


def check_rect():
    global fixed_rect, fixed_rect_check
    fixed_rect_check = [0 for n in range(465)]
    for x in fixed_rect:
        fixed_rect_check[x] = 1


def draw_grid(screen, list, block):
    for rect in list:
        if block[list.index(rect)] == 1:
            screen.blit(cyan, rect)
        if block[list.index(rect)] == 2:
            screen.blit(red, rect)
        if block[list.index(rect)] == 3:
            screen.blit(blue, rect)
        if block[list.index(rect)] == 4:
            screen.blit(green, rect)
        if block[list.index(rect)] == 5:
            screen.blit(purple, rect)
        if block[list.index(rect)] == 6:
            screen.blit(orange, rect)
        if block[list.index(rect)] == 7:
            screen.blit(yellow, rect)


b = Shapes(random.randrange(16, 28), future_block)
future_block = ((random.randint(1, 96)) % 6) + 1


def csll():
    global score, b, future_block
    if len(fixed_rect) > 0:
        if audio == True:
            fix.play()
    b = Shapes(random.randrange(16, 28), future_block)
    future_block = ((random.randint(1, 96)) % 6) + 1


etd = exit.Button('Exit to Desktop', 330, 60, ((width - 330) / 2, 380), 3)
etm = exit.Button('Exit to Main-Menu', 330, 60, ((width - 330) / 2, 300), 3)
cancel = exit.Button('Cancel', 330, 60, ((width - 330) / 2, 460), 3)
begin, current = 0, 0
def main():
    global current, menu, roko, game_over, begin, game_over_, score, audio, font, show_exit, future_block, speed_up, b, fixed_rect, fixed_rect_check, fixed_rect_colour, block_rects, blocks, gp, x, y, future_block, show_exit, etd, etm, cancel
    current = pygame.time.get_ticks()
    if menu == True:
        screen.blit(bg2, (0, 0))
        screen.blit(bg1, ((width / 2) - 150, (height / 2) - 300))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, height))
        pygame.draw.rect(screen, (0, 0, 0), (width - 400, 0, 400, height))
        font = pygame.font.Font(None, 40)
        a = font.render('Press Enter to start.', True, '#ffffff')
        screen.blit(a, transform_((16, 250)))
        a = font.render('Press Escape to exit.', True, '#ffffff')
        screen.blit(a, transform_((10, 310)))
    if menu == True:
        if audio == True:
            a = font.render('Audio', True, '#ffffff')
            screen.blit(a, (width - 105, 0))
            pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 5)
            pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 10, 1)
        else:
            a = font.render('Audio', True, '#ffffff')
            screen.blit(a, (width - 105, 0))
            pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 10, 1)
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
            return (max(scores), 'whole')
        if etm.pressed == True:
            return (max(scores), 'menu')
    if menu == False and game_over == False:
        screen.blit(bg2, (0, 0))
        font = pygame.font.Font(None, 48)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 400, height))
        pygame.draw.rect(screen, (0, 0, 0), (width - 400, 0, 400, height))
        screen.blit(bg1, ((width / 2) - 150, (height / 2) - 300))

        if roko != True:
            pygame.draw.rect(screen, (0, 0, 0), (width - 400, 0, 400, height))
            pygame.draw.rect(screen, (0, 0, 0), (width - 370, 0, 400, 200))
            pygame.draw.rect(screen, (255, 255, 255), (width - 370, 0, 369, 175), 1, 1)
            a = font.render('Next Block', True, '#ffffff')
            screen.blit(a, (1273, 10))
            a = font.render(f'Score: {score}', True, '#ffffff')
            screen.blit(a, (0, 0))
            if future_block == 1:
                screen.blit(cyan, (width - 223, 100))
                screen.blit(cyan, (width - 203, 100))
                screen.blit(cyan, (width - 183, 100))
                screen.blit(cyan, (width - 163, 100))
            if future_block == 2:
                screen.blit(red, (width - 210, 80))
                screen.blit(red, (width - 210, 100))
                screen.blit(red, (width - 190, 100))
                screen.blit(red, (width - 170, 100))
            if future_block == 3:
                screen.blit(blue, (width - 170, 80))
                screen.blit(blue, (width - 210, 100))
                screen.blit(blue, (width - 190, 100))
                screen.blit(blue, (width - 170, 100))
            if future_block == 4:
                screen.blit(green, (width - 203, 80))
                screen.blit(green, (width - 183, 80))
                screen.blit(green, (width - 203, 100))
                screen.blit(green, (width - 183, 100))
            if future_block == 5:
                screen.blit(purple, (width - 210, 100))
                screen.blit(purple, (width - 190, 100))
                screen.blit(purple, (width - 190, 80))
                screen.blit(purple, (width - 170, 80))
            if future_block == 6:
                screen.blit(orange, (width - 210, 80))
                screen.blit(orange, (width - 190, 80))
                screen.blit(orange, (width - 170, 80))
                screen.blit(orange, (width - 190, 100))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, 15, 60))
            pygame.draw.rect(screen, (255, 255, 255), (35, 10, 15, 60))
            font = pygame.font.Font(None, 40)
            if audio == True:
                a = font.render('Audio', True, '#ffffff')
                screen.blit(a, (width - 105, 0))
                pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 5)
                pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 10, 1)
            else:
                a = font.render('Audio', True, '#ffffff')
                screen.blit(a, (width - 105, 0))
                pygame.draw.circle(screen, (255, 255, 255), (width - 12, 14), 10, 1)
                font = pygame.font.Font(None, 40)

        if speed_up == False and roko == False:
            if type(b) != int and type(b) != float:
                b.movement_counter += 0.5
        elif speed_up == True and roko == False:
            if type(b) != int and type(b) != float:
                b.movement_counter += 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (menu == True or roko == True):
            l, m = pygame.mouse.get_pos()
            if l >= width - 12 - 10 and l <= width - 12 + 10 and m >= 4 and m <= 24:
                if audio == True:
                    audio = False
                else:
                    audio = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu == True or game_over_ == True:
                    show_exit = True
                if menu == False:
                    if roko == False:
                        roko = True
                    else:
                        roko = False
            if menu == False and game_over == False and roko == False:
                if event.key == pygame.K_LEFT:
                    if audio == True:
                        move_.play()
                    move = True
                    x = 0
                    while x < 4:
                        if x <= len(b.parts) - 1 and b.parts[x] % 15 == 0 or (b.parts[x] - 1 in fixed_rect):
                            move = False
                        x += 1
                    if move:
                        b.main_block -= 1
                    blocks = [0 for n in range(465)]
                if event.key == pygame.K_RIGHT:
                    if audio == True:
                        move_.play()
                    move = True
                    x = 0
                    while x < 4:
                        if x <= len(b.parts) - 1 and b.parts[x] % 15 == 14 or (b.parts[x] + 1 in fixed_rect):
                            move = False
                        x += 1
                    if move:
                        b.main_block += 1
                    blocks = [0 for n in range(465)]
                if event.key == pygame.K_DOWN:
                    speed_up = True
                    if audio == True:
                        move_.play()
                if event.key == pygame.K_SPACE:
                    if audio == True:
                        change.play()
                    blocks = [0 for n in range(465)]
                    transform = True
                    x = 0
                    while x < 4:
                        if x <= len(b.parts) - 1 and (b.parts[x] + 1 in fixed_rect):
                            transform = False
                        if (b.parts[x] - 1 in fixed_rect) and x <= len(b.parts):
                            transform = False
                        x += 1
                    if transform:
                        if b.main_block % 15 == 14:
                            b.collide()
                            if b.q in [2, 3, 6]:
                                b.main_block -= 1
                            if b.q == 1:
                                b.main_block -= 2
                        if b.main_block % 15 == 0:
                            if b.q in [2, 3, 6]:
                                b.main_block += 1
                            if b.q == 1:
                                b.main_block += 1
                        b.type += 1
            if event.key == pygame.K_RETURN:
                if menu == True or game_over == True:
                    if game_over_ == False:
                        menu = False
                    else:
                        blocks = [0 for n in range(465)]
                        block_rects = []
                        speed_up = False
                        menu = False
                        fixed_rect = []
                        fixed_rect_colour = []
                        fixed_rect_check = []
                        future_block = ((random.randint(1, 96)) % 6) + 1
                        x = 0
                        game_over_ = False
                        game_over = False
                        y = 0
                        for a in range(450, 465):
                            fixed_rect.append(a)
                        gp = 0
                        score = 0
                        for a in range(31):
                            for f in range(15):
                                gp += 1
                                a, b = transform_((x, y))
                                re = pygame.Rect(a, b, 20, 20)
                                block_rects.append(re)
                                fixed_rect_check.append(0)
                                fixed_rect_colour.append(0)
                                x += 20
                            y += 20
                            x = 0
                        b = Shapes(random.randrange(16, 28), ((random.randint(1, 96)) % 6) + 1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and menu == False and game_over == False and not roko:
                speed_up = False
    if menu == False and game_over == False and roko == False:
        try:
            blocks = [0 for n in range(465)]
            b.draw_shapes(blocks)
            b.draw_fixed_rect()
            b.collide()
            clear_line()
        except Exception as e:
            pass
        for v in fixed_rect:
            if v < 50:
                game_over = True
                begin = pygame.time.get_ticks()
                game_over_sound.play()
        draw_grid(screen, block_rects, blocks)
    if game_over == True:
        if current - begin >= 1400:
            game_over_ = True
    if game_over_ == True:
        if score not in scores:
            scores.append(score)
        font = pygame.font.Font(None, 64)
        if show_exit == False:
            screen.fill((0, 0, 0))
            k = font.render('Enter to play again.', True, '#ffffff')
            screen.blit(k, ((width - k.get_width()) / 2, (height / 2) - 50))
            k = font.render('Press Escape to exit.', True, '#ffffff')
            screen.blit(k, ((width - k.get_width()) / 2, (height / 2) + 40))
    pygame.display.update()