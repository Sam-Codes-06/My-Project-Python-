import pygame, random
from pygame import mixer
from data3 import button, exit

pygame.init()
mixer.init()
width, height = 480, 700
screen = pygame.display.set_mode((0, 0))


def transform(x, y):
    return (x + (screen.get_width() / 2) - 240, y + (screen.get_height() / 2) - 350)


bg = pygame.image.load(("data3/sky.jpg"))
trophy = pygame.image.load("data3/trophy.png")
audio = pygame.image.load("data3/audio.png")
music = pygame.image.load("data3/music.png")
power = pygame.image.load("data3/power.png")
win, select, out1, out2, jump_sound = pygame.mixer.Sound('data3/win.mp3'), pygame.mixer.Sound(
    'data3/select.mp3'), pygame.mixer.Sound('data3/out1.mp3'), pygame.mixer.Sound('data3/out2.mp3'), pygame.mixer.Sound(
    'data3/jump.mp3')
m, s = 1, 1
bg1y, bg2y = 0, -700
fps = pygame.time.Clock()
up, gv, g = 0, 0, 2.8
wb, hb, bx, by, dir = 60, 10, 30, 500, 0
bv = 3
move_ball = []
cc, count = 0, 0
speed = 60
score = 0
scores = [0]
game, menu = 0, 1
font_score = pygame.font.Font('freesansbold.ttf', 64)
info_text = pygame.font.Font('freesansbold.ttf', 32)
show_score = 0
winner = 0
title = pygame.image.load('data3/jump_up_title.png')
exit_menu = False

class BALL(pygame.sprite.Sprite):
    def __init__(self, ball_i):
        super().__init__()
        self.image = pygame.image.load(ball_i)
        self.rect = self.image.get_rect()
        self.rect.topleft = (width / 2, 625)


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


ball = BALL("data3/ball1.png")
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)
all_bars = []
audio_, music_ = True, True


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


play = button.Button('PLAY', 250, 80, transform(115, 320))
etd = exit.Button('Exit to Desktop', 330, 60, ((screen.get_width() - 330) / 2, 380))
etm = exit.Button('Exit to Main-Menu', 330, 60, ((screen.get_width() - 330) / 2, 300))
cancel = exit.Button('Cancel', 330, 60, ((screen.get_width() - 330) / 2, 460))
call_score = 0
begin = pygame.time.get_ticks()
current = 0
def main():
    global menu, game, bg1y, bg2y, exit_menu, show_score, up, music_, audio_, winner, score, bx, by, bv, count, gv, ball, cc, move_ball, call_score, begin, current
    if menu == 0 and game == 1 and exit_menu == False:
        screen.blit(bg, transform(0, bg1y))
        screen.blit(bg, transform(0, bg2y))
    if menu == 1 and game == 0 and exit_menu == False:
        screen.blit(bg, transform(0, 0))
        screen.blit(title, transform(80, 0))
        play.draw(screen)
        play.check_click()
    if exit_menu == True:
        screen.fill((0, 0, 0))
        etd.draw(screen)
        etm.draw(screen)
        cancel.draw(screen)
        etd.check_click()
        etm.check_click()
        cancel.check_click()
        if cancel.pressed == True:
            exit_menu = False
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            win.set_volume(1)
            select.set_volume(1)
            out1.set_volume(1)
            out2.set_volume(1)
            jump_sound.set_volume(1)
        if etd.pressed == True:
            return (max(scores), 'whole')
        if etm.pressed == True:
            return (max(scores), 'menu')
    if (menu == 1 and game == 0) or show_score == 1 and exit_menu == False:
        screen.blit(music, transform(width - 40, height - 120))
        screen.blit(audio, transform(width - 39, height - 80))
        screen.blit(power, transform(width - 40, height - 40))
        if music_ == False:
            pygame.draw.line(screen, (255, 0, 0), transform(width - 40, height - 120), transform(width - 8, height - 88),
                             2)
        if audio_ == False:
            pygame.draw.line(screen, (255, 0, 0), transform(width - 39, height - 80), transform(width - 7, height - 48),
                             2)
        if play.pressed == True:
            play.pressed = False
            game = 1
            menu = 0
            create_bars()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('data3/gamebg.mp3')
            pygame.mixer.music.play(-1)
    if winner == 1:
        score_text = font_score.render(f"SCORE:{score}", 1, (255, 201, 14))
        win_text = font_score.render("YOU WON!", 1, (255, 201, 14))
        screen.blit(trophy, transform(95, 300))
        screen.blit(score_text, transform(65, 60))
        screen.blit(win_text, transform(65, 150))
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
        move_ball.clear()
        ball.rect.y = -100
        if random.randint(1, 10) % 2 == 0:
            pygame.mixer.music.stop()
            out1.play()
            call_score = 1
        else:
            pygame.mixer.music.stop()
            out2.play()
            call_score = 2
        begin = pygame.time.get_ticks()
    current = pygame.time.get_ticks()
    if call_score == 1:
        if current - begin >= 1500:
            show_score = 1
            call_score = 0
            all_bars.clear()
    if call_score == 2:
        if current - begin >= 2000:
            show_score = 1
            call_score = 1
            all_bars.clear()
    if score >= 20 and score < 30 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 4
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 50 and score < 40 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        bv = 5
        if move_ball[1] < 0:
            move_ball[1] = -bv
        else:
            move_ball[1] = bv
    if score >= 1000 and winner == 0 and ball.rect.y >= 0 and ball.rect.y <= height + 32:
        pygame.mixer.music.stop()
        win.play()
        winner = 1
        game = 0
        menu = 0
        up = 0
        all_bars.clear()
        move_ball.clear()
    if show_score == 1 and exit_menu == False:
        if score not in scores:
            scores.append(score)
        score_text = font_score.render(f"SCORE:{score}", 1, (255, 201, 14))
        game_over = font_score.render("Game Over", 1, (255, 0, 0))
        info1 = info_text.render("Press Enter to play again.", 1, (0, 0, 0))
        screen.blit(score_text, transform(100, 200))
        screen.blit(game_over, transform(65, 100))
        screen.blit(info1, transform(45, 350))
    fps.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game == 1 and menu == 0 and ball.rect.y <= height + 32 and up == 0 and call_score == 0:
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
                pygame.mixer.music.load('data3/gamebg.mp3')
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_ESCAPE:
                exit_menu = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if show_score == True or (menu == 1 and game == 0):
                if mx >= 972 and mx <= 1004 and my >= 702 - 40 and my <= 734 - 40:
                    if music_ == True:
                        pygame.mixer.music.set_volume(0)
                        music_ = False
                    else:
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(-1)
                        music_ = True
                if mx >= 972 and mx <= 1004 and my >= 739 - 40 and my <= 771 - 40:
                    if audio_ == True:
                        win.set_volume(0.0)
                        select.set_volume(0)
                        out1.set_volume(0)
                        out2.set_volume(0)
                        jump_sound.set_volume(0)
                        audio_ = False
                    else:
                        win.set_volume(1)
                        select.set_volume(1)
                        out1.set_volume(1)
                        out2.set_volume(1)
                        jump_sound.set_volume(1)
                        audio_ = True
                if mx >= 972 and mx <= 1004 and my >= 739 and my <= 771:
                    exit_menu = True
                    pygame.mixer.music.set_volume(0)
                    win.set_volume(0.0)
                    select.set_volume(0)
                    out1.set_volume(0)
                    out2.set_volume(0)
                    jump_sound.set_volume(0)
    if len(all_bars) > 0 and game == 1 and menu == 0:
        for i in range(len(all_bars)):
            pygame.draw.rect(screen, all_bars[i][0].color,
                             (transform(all_bars[i][0].rect.x, all_bars[i][0].rect.y)[0],
                              transform(all_bars[i][0].rect.x, all_bars[i][0].rect.y)[1], all_bars[i][0].rect.w,
                              all_bars[i][0].rect.h))
            pygame.draw.rect(screen, all_bars[i][1].color,
                             (transform(all_bars[i][1].rect.x, all_bars[i][1].rect.y)[0],
                              transform(all_bars[i][1].rect.x, all_bars[i][1].rect.y)[1], all_bars[i][1].rect.w,
                              all_bars[i][1].rect.h))
            pygame.draw.rect(screen, all_bars[i][2].color,
                             (transform(all_bars[i][2].rect.x, all_bars[i][2].rect.y)[0],
                              transform(all_bars[i][2].rect.x, all_bars[i][2].rect.y)[1], all_bars[i][2].rect.w,
                              all_bars[i][2].rect.h))
            pygame.draw.rect(screen, all_bars[i][3].color,
                             (transform(all_bars[i][3].rect.x, all_bars[i][3].rect.y)[0],
                              transform(all_bars[i][3].rect.x, all_bars[i][3].rect.y)[1], all_bars[i][3].rect.w,
                              all_bars[i][3].rect.h))
            pygame.draw.rect(screen, all_bars[i][4].color,
                             (transform(all_bars[i][4].rect.x, all_bars[i][4].rect.y)[0],
                              transform(all_bars[i][4].rect.x, all_bars[i][4].rect.y)[1], all_bars[i][4].rect.w,
                              all_bars[i][4].rect.h))
    if game == 1 and menu == 0 and call_score == 0:
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
        screen.blit(ball.image, transform(ball.rect.x, ball.rect.y))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width() / 2) - 240, 0, 480, 82))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width() / 2) - 240, screen.get_height() - 82, 480, 82))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width() / 2) - 322, 0, 82, screen.get_height()))
    pygame.draw.rect(screen, (0, 0, 0), ((screen.get_width() / 2) + 240, 0, 200, screen.get_height()))
    pygame.display.update()

while True:
    main()