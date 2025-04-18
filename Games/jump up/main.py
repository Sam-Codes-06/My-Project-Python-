import pygame, random, sys
from pygame import mixer

pygame.init()
mixer.init()
width, height = 480, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jump Up")
pygame.display.set_icon(pygame.image.load("data/icon.png"))
bg = pygame.image.load(("data/sky.jpg"))
menu_image = pygame.image.load("data/menu(1, 1).jpg")
trophy = pygame.image.load("data/trophy.png")
win, select, out1, out2, jump_sound = pygame.mixer.Sound('data/win.mp3'), pygame.mixer.Sound(
    'data/select.mp3'), pygame.mixer.Sound('data/out1.mp3'), pygame.mixer.Sound('data/out2.mp3'), pygame.mixer.Sound(
    'data/jump.mp3')
m, s = 1, 1
bg1y, bg2y = 0, -700
fps = pygame.time.Clock()
run = 1
up, gv, g = 0, 0, 2.8
wb, hb, bx, by, dir = 60, 10, 30, 500, 0
bv = 3
move_ball = []
cc, count = 0, 0
speed = 60
score = 0
game, menu = 0, 1
font_score = pygame.font.Font('freesansbold.ttf', 64)
info_text = pygame.font.Font('freesansbold.ttf', 32)
show_score = 0
winner = 0


class BALL(pygame.sprite.Sprite):
    def __init__(self, ball_i):
        super().__init__()
        self.image = pygame.image.load(ball_i)
        self.rect = self.image.get_rect()
        self.rect.topleft = width / 2, 625


def jump(ball, v):
    ball.rect.y += v


class bars(pygame.sprite.Sprite):
    def __init__(self, wb, hb, bx, by, dir):
        super().__init__()
        self.image = pygame.Surface([wb, hb])
        self.rect = self.image.get_rect(topleft=(bx, by))
        self.get_range()
        pygame.draw.rect(self.image, self.color, (bx, by, wb, hb))
        self.dir = dir

    def get_range(self):
        a, b, c = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        if a >= 140 and a <= 160 and b >= 200 and b <= 230 and c >= 220 and c <= 250:
            self.get_range()
        else:
            self.color = (a, b, c)


def move_bars(all_bars, bv):
    for i in range(len(all_bars)):
        for k in range(5):
            all_bars[i][k].rect.x += all_bars[i][k].dir * bv


ball = BALL("data/ball.png")
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)
all_bars = []


def create_bars():
    global all_bars, bx, by
    for i in range(6):
        if i != 0:
            all_bars.append(
                [bars(wb, hb, bx, by, -(all_bars[i - 1][0].dir)), bars(wb, hb, bx + 120, by, -(all_bars[i - 1][0].dir)),
                 bars(wb, hb, bx + 240, by, -(all_bars[i - 1][0].dir)),
                 bars(wb, hb, bx + 360, by, -(all_bars[i - 1][0].dir)),
                 bars(wb, hb, bx + 480, by, -(all_bars[i - 1][0].dir))])
        else:
            all_bars.append(
                [bars(wb, hb, bx, by, 1), bars(wb, hb, bx + 120, by, 1),
                 bars(wb, hb, bx + 240, by, 1),
                 bars(wb, hb, bx + 360, by, 1),
                 bars(wb, hb, bx + 480, by, 1)])
        bx = 30
        by -= 150


pygame.mixer.music.load('data/menubg.mp3')
pygame.mixer.music.play(-1)
while run:
    if menu == 0 and game == 1:
        screen.blit(bg, (0, bg1y))
        screen.blit(bg, (0, bg2y))
    if menu == 1 and game == 0:
        screen.blit(menu_image, (0, 0))
    if winner == 1:
        score_text = font_score.render(f"SCORE:{score}", 1, (255, 201, 14))
        win_text = font_score.render("YOU WON!", 1, (255, 201, 14))
        end = info_text.render("Press ESCAPE to exit.", 1, (0, 0, 0))
        screen.blit(trophy, (95, 300))
        screen.blit(score_text, (55, 60))
        screen.blit(win_text, (65, 150))
        screen.blit(end, (75, height - 64))
    for i in range(len(all_bars)):
        if all_bars[i][0].rect.y >= height:
            all_bars.append(
                [bars(wb, hb, bx, all_bars[len(all_bars) - 1][0].rect.y - 150, -all_bars[len(all_bars) - 1][0].dir),
                 bars(wb, hb, bx + 120, all_bars[len(all_bars) - 1][0].rect.y - 150,
                      -all_bars[len(all_bars) - 1][0].dir),
                 bars(wb, hb, bx + 240, all_bars[len(all_bars) - 1][0].rect.y - 150,
                      -all_bars[len(all_bars) - 1][0].dir),
                 bars(wb, hb, bx + 360, all_bars[len(all_bars) - 1][0].rect.y - 150,
                      -all_bars[len(all_bars) - 1][0].dir),
                 bars(wb, hb, bx + 480, all_bars[len(all_bars) - 1][0].rect.y - 150,
                      -all_bars[len(all_bars) - 1][0].dir)])
            all_bars.remove(all_bars[i])
    for i in range(len(all_bars)):
        for k in range(5):
            all_bars[i][k].color = all_bars[i][0].color
            if all_bars[i][k].rect.x <= -60 and all_bars[i][k].dir == -1:
                all_bars[i][k].rect.x = width + 60
            if all_bars[i][k].rect.x >= width + 60 and all_bars[i][k].dir == 1:
                all_bars[i][k].rect.x = -60
    if (ball.rect.y >= height and game == 1 and menu == 0):
        up = 0
        all_bars.clear()
        move_ball.clear()
        ball.rect.y = -100
        if random.randint(1, 10) % 2 == 0:
            pygame.mixer.music.stop()
            out1.play()
            pygame.time.delay(1500)
            show_score = 1
        else:
            pygame.mixer.music.stop()
            out2.play()
            pygame.time.delay(2000)
            show_score = 1
    if score >= 20 and score < 30 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 4
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 30 and score < 40 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 5
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 40 and score < 50 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 6
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 50 and score < 100 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 7
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 100 and winner == 0 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        pygame.mixer.music.stop()
        win.play()
        winner = 1
        game = 0
        menu = 0
        up = 0
        all_bars.clear()
        move_ball.clear()
    if show_score == 1:
        score_text = font_score.render(f"SCORE:{score}", 1, (255, 201, 14))
        game_over = font_score.render("Game Over", 1, (255, 0, 0))
        info = info_text.render("Hit Enter to play again, noob!", 1, (0, 0, 0))
        info2 = info_text.render("Press ESC to quit, QUITTER!", 1, (0, 0, 0))
        screen.blit(score_text, (100, 200))
        screen.blit(game_over, (65, 100))
        screen.blit(info, (10, 400))
        screen.blit(info2, (20, 500))
    fps.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game == 1 and menu == 0 and ball.rect.y <= height + 32 and up == 0 and show_score == 0:
                up = 1
                gv = -30
                if len(move_ball) > 0:
                    move_ball[0] = 0
            if event.key == pygame.K_RETURN and show_score == 1:
                game, menu = 1, 0
                ball.rect.topleft = width / 2, 625
                bx, by = 30, 500
                up = 0
                gv = -30
                ball.rect.topleft = width / 2, 625
                bv = 3
                create_bars()
                show_score = 0
                score = 0
                pygame.mixer.music.load('data/gamebg.mp3')
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_ESCAPE:
                run = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if mx >= 100 and mx <= 350 and my >= 235 and my <= 320:
                game = 1
                menu = 0
                create_bars()
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/gamebg.mp3')
                pygame.mixer.music.play(-1)
            if mx >= 125 and mx <= 200 and my >= 400 and my <= 465:
                if m % 2 != 0:
                    m += 1
                    pygame.mixer.music.set_volume(0)
                    if s % 2 == 0:
                        menu_image = pygame.image.load("data/menu(0, 0).jpg")
                    else:
                        menu_image = pygame.image.load("data/menu(0, 1).jpg")
                else:
                    m += 1
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                    if s % 2 == 0:
                        menu_image = pygame.image.load("data/menu(1, 0).jpg")
                    else:
                        menu_image = pygame.image.load("data/menu(1, 1).jpg")
            if mx >= 230 and mx <= 305 and my >= 400 and my <= 465:
                if s % 2 != 0:
                    s += 1
                    win.set_volume(0.0)
                    select.set_volume(0)
                    out1.set_volume(0)
                    out2.set_volume(0)
                    jump_sound.set_volume(0)
                    if m % 2 == 0:
                        menu_image = pygame.image.load("data/menu(0, 0).jpg")
                    else:
                        menu_image = pygame.image.load("data/menu(1, 0).jpg")
                else:
                    s += 1
                    win.set_volume(1)
                    select.set_volume(1)
                    out1.set_volume(1)
                    out2.set_volume(1)
                    jump_sound.set_volume(1)
                    if m % 2 == 0:
                        menu_image = pygame.image.load("data/menu(0, 1).jpg")
                    else:
                        menu_image = pygame.image.load("data/menu(1, 1).jpg")
            if mx >= 100 and mx <= 340 and my >= 560 and my <= 650:
                run = 0
    if len(all_bars) > 0 and game == 1 and menu == 0:
        for i in range(len(all_bars)):
            pygame.draw.rect(screen, all_bars[i][0].color,
                             (all_bars[i][0].rect.x, all_bars[i][0].rect.y, all_bars[i][0].rect.w,
                              all_bars[i][0].rect.h))
            pygame.draw.rect(screen, all_bars[i][1].color,
                             (all_bars[i][1].rect.x, all_bars[i][1].rect.y, all_bars[i][1].rect.w,
                              all_bars[i][1].rect.h))
            pygame.draw.rect(screen, all_bars[i][2].color,
                             (all_bars[i][2].rect.x, all_bars[i][2].rect.y, all_bars[i][2].rect.w,
                              all_bars[i][2].rect.h))
            pygame.draw.rect(screen, all_bars[i][3].color,
                             (all_bars[i][3].rect.x, all_bars[i][3].rect.y, all_bars[i][3].rect.w,
                              all_bars[i][3].rect.h))
            pygame.draw.rect(screen, all_bars[i][4].color,
                             (all_bars[i][4].rect.x, all_bars[i][4].rect.y, all_bars[i][4].rect.w,
                              all_bars[i][4].rect.h))
    if game == 1 and menu == 0:
        move_bars(all_bars, bv)
    for i in range(len(all_bars)):
        for k in range(5):
            if abs(all_bars[i][k].rect.top - ball.rect.bottom) <= 5 and gv > 0 and abs(
                    ball.rect.right - all_bars[i][k].rect.left >= 16) and abs(
                all_bars[i][k].rect.right - ball.rect.left >= 16) and ball.rect.y <= height + 32:
                jump_sound.play()
                move_ball = [1, all_bars[i][k].dir * bv]
                up = 0
                gv = -30
                ball.rect.y = all_bars[i][k].rect.y - 32
                cc = "down"
                score += 1
                print(score)
            if abs(all_bars[i][k].rect.top - ball.rect.bottom) == 0 and (
                    abs(ball.rect.right - all_bars[i][k].rect.left) <= 12 or abs(
                all_bars[i][k].rect.right - ball.rect.left) <= 12) and up == 0:
                up = 1
                gv = 0
    if len(move_ball) > 0 and move_ball[0] == 1 and game == 1 and menu == 0:
        ball.rect.x += move_ball[1]
    if ball.rect.x >= width - 32 and game == 1:
        ball.rect.x = width - 32
    if ball.rect.x <= 0 and game == 1:
        ball.rect.x = 0
    if up == 1 and game == 1:
        jump(ball, gv)
        gv += g
    if bg1y >= height and game == 1:
        bg1y = bg2y - 700
    if bg2y >= height and game == 1:
        bg2y = bg1y - 700
    if cc == "down" and count < 5 and ball.rect.y <= height / 2 and game == 1:
        for i in range(len(all_bars)):
            for k in range(5):
                all_bars[i][k].rect.y += 30
        count += 1
        ball.rect.y += 30
        bg1y += 30
        bg2y += 30
    else:
        count = 0
        cc = 0
    if game == 1 and menu == 0:
        ball_group.draw(screen)
    pygame.display.update()
