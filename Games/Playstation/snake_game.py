import pygame
import random
from data0 import button


def transform(x=-100, y=-100):
    if x == -100:
        return y + 40
    elif y == -100:
        return x + 368
    else:
        return x + 368, y + 40


def reverse(x=-100, y=-100):
    if x == -100:
        return y - 40
    elif y == -100:
        return x - 368
    else:
        return x - 368, y - 40


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0))
width, height = screen.get_size()
fps = 100
fx, fy = 0, 0
speed = 0
direction = None
game_over = False
menu = True
pause = False
score = 0
high_score = [0]
font1 = pygame.font.Font('freesansbold.ttf', 48)
font2 = pygame.font.Font('freesansbold.ttf', 32)
spawn = True
food = []
current_food = 0
for i in range(0, 21):
    food.append(pygame.image.load(f'data0/food{i}.png'))
extra_food = pygame.image.load(r'data0/extra_food.png')
spawn_extra = False
extra_x, extra_y = 0, 0
extra_timer = 0
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green1": (167, 217, 72), "green2": (142, 204, 57),
          "blue1": (91, 123, 249), "blue2": (80, 112, 238),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
play = button.Button('PLAY', 502, 60, (408, 540), 0)
settings = button.Button('', 60, 60, (911, 540), 0)
exit = button.Button('EXIT', 156, 60, (972, 540), 0)
exit_game = button.Button('Exit to Main-Menu', 330, 60, ((width - 330) / 2, 300), 0)
exit_desktop = button.Button('Exit to Desktop', 330, 60, ((width - 330) / 2, 380), 0)
exit_cancel = button.Button('Cancel', 330, 60, ((width - 330) / 2, 460), 0)
back = button.Button(' ', 60, 40, (940, 165), 0)
settings_tab = False
menu_bg = pygame.image.load('data0/intro1.png')
over_bg1 = pygame.image.load('data0/intro2.jpg')
over_bg2_b = pygame.image.load('data0/intro3_b.png')
originalbg = pygame.image.load('data0/background1.jpg')
bg1 = pygame.image.load('data0/background1.jpg')
bg2 = pygame.image.load('data0/background2.jpg')
level0 = pygame.image.load('data0/speed0.png')
level1 = pygame.image.load('data0/speed1.png')
level2 = pygame.image.load('data0/speed2.png')
level = level1
snake_color = 'blue'
bbl_b = pygame.image.load(r'data0/bbl_b.png')
bbr_b = pygame.image.load(r'data0/bbr_b.png')
bh_b = pygame.image.load(r'data0/bh_b.png')
btl_b = pygame.image.load(r'data0/btl_b.png')
btr_b = pygame.image.load(r'data0/btr_b.png')
bv_b = pygame.image.load(r'data0/bv_b.png')
shd_b = pygame.image.load(r'data0/shd_b.png')
shu_b = pygame.image.load(r'data0/shu_b.png')
shl_b = pygame.image.load(r'data0/shl_b.png')
shr_b = pygame.image.load(r'data0/shr_b.png')
dhl_b = pygame.image.load(r'data0/dhl_b.png')
dhr_b = pygame.image.load(r'data0/dhr_b.png')
dhd_b = pygame.image.load(r'data0/dhd_b.png')
dhu_b = pygame.image.load(r'data0/dhu_b.png')
eu_b = pygame.image.load(r'data0/eu_b.png')
er_b = pygame.image.load(r'data0/er_b.png')
ed_b = pygame.image.load(r'data0/ed_b.png')
el_b = pygame.image.load(r'data0/el_b.png')
stl_b = pygame.image.load(r'data0/stl_b.png')
str_b = pygame.image.load(r'data0/str_b.png')
std_b = pygame.image.load(r'data0/std_b.png')
stu_b = pygame.image.load(r'data0/stu_b.png')
eat = pygame.mixer.Sound(r'data0/eat.wav')
snake_body = [shu_b, shd_b, shl_b, shr_b, dhu_b, dhd_b, dhl_b, dhr_b, eu_b, ed_b, el_b, er_b, bh_b, bv_b, bbr_b, btr_b,
              btl_b, bbl_b, stu_b, std_b, stl_b, str_b]
up_key = pygame.image.load(r'data0/up_key.png')
down_key = pygame.image.load(r'data0/down_key.png')
right_key = pygame.image.load(r'data0/right_key.png')
left_key = pygame.image.load(r'data0/left_key.png')
w_key = pygame.image.load(r'data0/w_key.png')
a_key = pygame.image.load(r'data0/a_key.png')
s_key = pygame.image.load(r'data0/s_key.png')
d_key = pygame.image.load(r'data0/d_key.png')
esc_key = pygame.image.load(r'data0/esc_key.png')
lmb = pygame.image.load(r'data0/lmb.png')
up = pygame.mixer.Sound(r'data0/up.wav')
down = pygame.mixer.Sound(r'data0/down.wav')
right = pygame.mixer.Sound(r'data0/right.wav')
left = pygame.mixer.Sound(r'data0/left.wav')
game_over_sound = pygame.mixer.Sound(r'data0/game_over.wav')
score_img = pygame.image.load(r'data0/score.png')
high_score_img = pygame.image.load(r'data0/high_score.png')
teleport = pygame.image.load(r'data0/teleport.png')
solid = pygame.image.load(r'data0/solid.png')
wall_type = 'teleport'
audio = True
exit_status = False


def spawn_food(restrict, s=0):
    if type(s) == int:
        pass
    else:
        restrict.append(s)
    global coords
    snake_coords = coords.copy()
    for i in range(len(restrict)):
        if restrict[i] in snake_coords:
            snake_coords.remove(restrict[i])
    return snake_coords[random.randint(0, len(snake_coords) - 1)]


def turn(i):
    if i >= 1 and i < len(s.snake_body) - 1:
        if s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[
                    i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -760:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -760:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -760:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 760:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 760:
            s.snake_body[i].part = snake_body[13]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 760:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 40:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -40 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -40:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[12]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -760:
            s.snake_body[i].part = snake_body[16]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == -760:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[15]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 760:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[14]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == 0 and s.snake_body[i].y - s.snake_body[i + 1].y == 760:
            s.snake_body[i].part = snake_body[17]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760 and \
                s.snake_body[i].x - s.snake_body[i + 1].x == -760 and s.snake_body[i].y - s.snake_body[i + 1].y == 0:
            s.snake_body[i].part = snake_body[17]
    if i == len(s.snake_body) - 1:
        if s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 40:
            s.snake_body[i].part = snake_body[19]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0:
            s.snake_body[i].part = snake_body[20]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -40:
            s.snake_body[i].part = snake_body[18]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 40 and s.snake_body[i].y - s.snake_body[i - 1].y == 0:
            s.snake_body[i].part = snake_body[21]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == -760:
            s.snake_body[i].part = snake_body[19]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 0 and s.snake_body[i].y - s.snake_body[i - 1].y == 760:
            s.snake_body[i].part = snake_body[18]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == 760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0:
            s.snake_body[i].part = snake_body[20]
        elif s.snake_body[i].x - s.snake_body[i - 1].x == -760 and s.snake_body[i].y - s.snake_body[i - 1].y == 0:
            s.snake_body[i].part = snake_body[21]
    return s.snake_body


class head():
    def __init__(self):
        self.part = snake_body[3]
        self.x, self.y = 400, 400


class body():
    def __init__(self, x=360, y=400):
        self.part = snake_body[12]
        self.x, self.y = x, y


class tail():
    def __init__(self):
        self.part = snake_body[20]
        self.x, self.y = 320, 400


class Snake():
    def __init__(self):
        self.snake_body = [head(), body(), tail()]

    def move_body(self, direction):
        for c in range(-len(s.snake_body) + 1, 0):
            s.snake_body[-c].x, s.snake_body[-c].y = s.snake_body[-c - 1].x, s.snake_body[-c - 1].y
        if direction == 'up':
            self.snake_body[0].part = snake_body[0]
            self.snake_body[0].y -= speed
        if direction == 'right':
            self.snake_body[0].part = snake_body[3]
            self.snake_body[0].x += speed
        if direction == 'left':
            self.snake_body[0].part = snake_body[2]
            self.snake_body[0].x -= speed
        if direction == 'down':
            self.snake_body[0].part = snake_body[1]
            self.snake_body[0].y += speed

    def add_part(self):
        self.snake_body.insert(len(self.snake_body) - 1, body(self.snake_body[len(self.snake_body) - 1].x,
                                                              self.snake_body[len(self.snake_body) - 1].y))
        if self.snake_body[len(self.snake_body) - 1].part == snake_body[20]:
            self.snake_body[len(self.snake_body) - 1].x -= 40
        elif self.snake_body[len(self.snake_body) - 1].part == snake_body[18]:
            self.snake_body[len(self.snake_body) - 1].y -= 40
        elif self.snake_body[len(self.snake_body) - 1].part == snake_body[19]:
            self.snake_body[len(self.snake_body) - 1].y += 40
        elif self.snake_body[len(self.snake_body) - 1].part == snake_body[21]:
            self.snake_body[len(self.snake_body) - 1].x += 40


s = Snake()
begin = pygame.time.get_ticks()
coords = []
for i in range(0, 20):
    for j in range(0, 20):
        coords.append((i * 40, j * 40))
restrict = []
correction = -2


def main():
    global current, begin, s, fx, fy, food, extra_x, extra_y, extra_timer, bg1, a, snake_color, level, menu, game_over, direction, correction, exit_status, spawn_extra, current_food, spawn, score, pause, speed, run, play, exit, settings, score_text, high_score_text, settings_tab, settings_text, audio, fps, wall_type, teleport, solid, level, exit_game, exit_desktop, exit_cancel
    screen.fill((0, 0, 0))
    current = pygame.time.get_ticks()
    screen.blit(bg1, transform(0, 0))
    if menu == True:
        a = transform(0, 0)
        bg1 = bg2
        screen.blit(menu_bg, (a[0] + 40, a[1] + 240))
        play.draw(screen)
        settings.draw(screen)
        exit.draw(screen)
        if settings_tab == False:
            play.check_click()
            settings.check_click()
            exit.check_click()
        if settings_tab == True:
            settings_text = []
            settings_text.append(font1.render('Key Bindings', True, colors['white']))
            settings_text.append(font2.render('UP', True, colors['white']))
            settings_text.append(font2.render('DOWN', True, colors['white']))
            settings_text.append(font2.render('LEFT', True, colors['white']))
            settings_text.append(font2.render('RIGHT', True, colors['white']))
            settings_text.append(font2.render('BACK / PAUSE', True, colors['white']))
            settings_text.append(font2.render('SELECT', True, colors['white']))
            settings_text.append(font2.render('AUDIO', True, colors['white']))
            settings_text.append(font2.render('WALL TYPE', True, colors['white']))
            settings_text.append(font2.render('SPEED', True, colors['white']))
            pygame.draw.rect(screen, (74, 196, 251), (a[0] + 160, a[1] + 160, 480, 480))
            pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 253), (a[0] + 579, a[1] + 281), 3)
            pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 293), (a[0] + 579, a[1] + 321), 3)
            pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 333), (a[0] + 579, a[1] + 361), 3)
            pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 370), (a[0] + 579, a[1] + 398), 3)
            screen.blit(up_key, (a[0] + 540, a[1] + 253))
            screen.blit(down_key, (a[0] + 540, a[1] + 292))
            screen.blit(left_key, (a[0] + 540, a[1] + 333))
            screen.blit(right_key, (a[0] + 540, a[1] + 369))
            screen.blit(w_key, (a[0] + 590, a[1] + 253))
            screen.blit(s_key, (a[0] + 590, a[1] + 292))
            screen.blit(a_key, (a[0] + 590, a[1] + 333))
            screen.blit(d_key, (a[0] + 590, a[1] + 369))
            screen.blit(esc_key, (a[0] + 565, a[1] + 405))
            screen.blit(lmb, (a[0] + 565, a[1] + 441))
            pygame.draw.line(screen, colors['white'], (a[0] + 180, a[1] + 486), (a[0] + 620, a[1] + 486), 3)
            pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 500, 30, 30), 3)
            pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 547, 30, 30), 3)
            pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 595, 30, 30), 3)
            if audio == True:
                pygame.draw.circle(screen, colors['white'], (a[0] + 590 + 15, a[1] + 500 + 15), 5)
            screen.blit(settings_text[0], (a[0] + 240, a[1] + 180))
            screen.blit(settings_text[1], (a[0] + 180, a[1] + 253))
            screen.blit(settings_text[2], (a[0] + 180, a[1] + 293))
            screen.blit(settings_text[3], (a[0] + 180, a[1] + 333))
            screen.blit(settings_text[4], (a[0] + 180, a[1] + 370))
            screen.blit(settings_text[5], (a[0] + 180, a[1] + 406))
            screen.blit(settings_text[6], (a[0] + 180, a[1] + 442))
            screen.blit(settings_text[7], (a[0] + 180, a[1] + 502))
            screen.blit(settings_text[8], (a[0] + 180, a[1] + 547))
            screen.blit(settings_text[9], (a[0] + 180, a[1] + 594))
            if wall_type == 'teleport':
                screen.blit(teleport, (a[0] + 591, a[1] + 547))
            if wall_type == 'solid':
                screen.blit(solid, (a[0] + 591, a[1] + 547))
            if level == level0:
                screen.blit(level0, (a[0] + 590, a[1] + 593))
            if level == level1:
                screen.blit(level1, (a[0] + 590, a[1] + 595))
            if level == level2:
                screen.blit(level2, (a[0] + 590, a[1] + 594))
        if play.status == 'play' and menu == True:
            play.status = None
            menu = False
        elif settings.status == 'settings' and menu == True:
            settings.status = None
            settings_tab = True
        elif exit.status == 'exit' and menu == True:
            exit.status = None
            exit_status = True
        if exit_status == True:
            screen.fill((0, 0, 0))
            exit_game.draw(screen)
            exit_desktop.draw(screen)
            exit_cancel.draw(screen)
            exit_game.check_click()
            exit_desktop.check_click()
            exit_cancel.check_click()
            if exit_cancel.status == 'cancel':
                exit_cancel.status = None
                exit_status = False
            if exit_desktop.status == 'exit_whole':
                exit_cancel.status = None
                exit_status = False
                return (max(high_score), 'whole')
            if exit_game.status == 'exit_snake_game':
                return (max(high_score), 'menu')

    elif menu == False:
        bg1 = originalbg

    if pause == True:
        pygame.draw.rect(screen, colors['white'], (10, 10, 10, 50))
        pygame.draw.rect(screen, colors['white'], (35, 10, 10, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and settings_tab:
            b = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and b[0] > a[0] + 590 and b[0] < a[0] + 620 and b[1] > a[1] + 500 and \
                    b[1] < a[1] + 530:
                if audio == True:
                    audio = False
                elif audio == False:
                    audio = True
            if pygame.mouse.get_pressed()[0] and b[0] > a[0] + 590 and b[0] < a[0] + 620 and b[1] > a[1] + 595 and \
                    b[1] < a[1] + 625:
                if level == level0:
                    level = level1
                    fps = 100
                    correction = -2
                elif level == level1:
                    level = level2
                    fps = 60
                    correction = 38
                elif level == level2:
                    level = level0
                    fps = 160
                    correction = -62
            if pygame.mouse.get_pressed()[0] and b[0] > a[0] + 590 and b[0] < a[0] + 620 and b[1] > a[1] + 548 and \
                    b[1] < a[1] + 578:
                if wall_type == 'teleport':
                    wall_type = 'solid'
                else:
                    wall_type = 'teleport'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run == False
                return 'exit'
            if event.key == pygame.K_ESCAPE:
                if menu == False and game_over == False:
                    if pause == False:
                        speed = 0
                        pause = True
                    else:
                        speed = 40
                        pause = False
                if (menu == True or game_over == True) and settings_tab == True:
                    settings_tab = False
            if menu == False and pause == False:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and s.snake_body[
                    0].part != snake_body[1] and game_over == False and direction != 'up':
                    if audio == True:
                        pygame.mixer.Sound.play(up)
                    direction = 'up'
                    if speed == 0:
                        speed = 40
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and s.snake_body[
                    0].part != snake_body[0] and game_over == False and direction != 'down':
                    if audio == True:
                        pygame.mixer.Sound.play(down)
                    direction = 'down'
                    if speed == 0:
                        speed = 40
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and s.snake_body[
                    0].part != snake_body[2] and game_over == False and direction != 'right':
                    if audio:
                        pygame.mixer.Sound.play(right)
                    direction = 'right'
                    if speed == 0:
                        speed = 40
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and s.snake_body[
                    0].part != snake_body[3] and game_over == False and direction != 'left':
                    if audio:
                        pygame.mixer.Sound.play(left)
                    direction = 'left'
    if menu == False and game_over == False:
        for i in range(len(s.snake_body) - 1, -1, -1):
            s.snake_body = turn(i)
            if i != 0:
                if s.snake_body[0].x == s.snake_body[i].x and s.snake_body[0].y == s.snake_body[i].y or (
                        (wall_type == 'solid' and (
                                s.snake_body[0].x == 760 or s.snake_body[0].x == 0 or s.snake_body[0].y == 760 or
                                s.snake_body[0].y == 0))):
                    high_score.append(score)
                    if speed != 0:
                        if audio:
                            pygame.mixer.Sound.play(game_over_sound)
                    if current - begin >= 1000:
                        play = button.Button('PLAY', 502, 60, (408, 543), 0)
                        settings = button.Button('', 60, 60, (911, 543), 0)
                        exit = button.Button('EXIT', 156, 60, (972, 543), 0)
                        game_over = True
                    speed = 0
                    if s.snake_body[0].part == snake_body[0]:
                        s.snake_body[0].part = snake_body[4]
                    if s.snake_body[0].part == snake_body[1]:
                        s.snake_body[0].part = snake_body[5]
                    if s.snake_body[0].part == snake_body[3]:
                        s.snake_body[0].part = snake_body[7]
                    if s.snake_body[0].part == snake_body[2]:
                        s.snake_body[0].part = snake_body[6]
            screen.blit(s.snake_body[i].part, transform(s.snake_body[i].x, s.snake_body[i].y))
            restrict.append((s.snake_body[i].x, s.snake_body[i].y))
        if spawn == True:
            fx, fy = spawn_food(restrict)
            spawn = False
            current_food = food[random.randint(0, len(food) - 1)]
        if s.snake_body[0].x == fx and s.snake_body[0].y == fy:
            if audio:
                pygame.mixer.Sound.play(eat)
            s.add_part()
            score += 1
            fx, fy = spawn_food(restrict)
            current_food = food[random.randint(0, len(food) - 1)]
        if len(s.snake_body) > 3 and random.randint(0, 1000 * (
                len(s.snake_body)) - 2) == 6 and spawn_extra == False and pause == False:
            spawn_extra = True
            a = spawn_food(restrict, s=(fx, fy))
            extra_x, extra_y = transform(a[0], a[1])
            extra_timer = 40
        if spawn_extra == True:
            pygame.draw.rect(screen, '#F34C50', (extra_x, extra_y - 10, extra_timer, 10))
            screen.blit(extra_food, (extra_x, extra_y))
            if current - begin + correction >= 98 and pause == False:
                extra_timer -= 1
            if extra_timer == 1 and pause == False:
                spawn_extra = False
                extra_x, extra_y = -100, -100
            if s.snake_body[0].x == reverse(x=extra_x) and s.snake_body[0].y == reverse(
                    y=extra_y) and speed > 0 and pause == False:
                spawn_extra = False
                if audio:
                    pygame.mixer.Sound.play(eat)
                s.add_part()
                s.add_part()
                score += 2
        if ((((s.snake_body[0].x - fx) ** 2) + (
                s.snake_body[0].y - fy) ** 2) ** 0.5 <= 1.414 * 80 or (
                ((s.snake_body[0].x - reverse(x=extra_x)) ** 2) + (
                (s.snake_body[0].y - reverse(y=extra_y)) ** 2)) ** 0.5 <= 1.414 * 80):
            if s.snake_body[0].part == snake_body[1]:
                screen.blit(snake_body[9], transform(s.snake_body[0].x - 2, s.snake_body[0].y + 20))
            if s.snake_body[0].part == snake_body[2]:
                screen.blit(snake_body[10], transform(s.snake_body[0].x - 2, s.snake_body[0].y - 2))
            if s.snake_body[0].part == snake_body[0]:
                screen.blit(snake_body[8], transform(s.snake_body[0].x - 2, s.snake_body[0].y - 2))
            if s.snake_body[0].part == snake_body[3]:
                screen.blit(snake_body[11], transform(s.snake_body[0].x + 20, s.snake_body[0].y - 2))
        screen.blit(current_food, transform(fx, fy))
        restrict.clear()
        if pause == False:
            screen.blit(score_img, (10, 10))
            pygame.draw.circle(screen, colors['white'], (70, 22), 5)
            pygame.draw.circle(screen, colors['white'], (70, 48), 5)
            score_text = font1.render(f'{score}', True, colors['white'])
            screen.blit(score_text, (80, 15))
        if current - begin >= fps and direction != None and speed != 0:
            begin = current
            s.move_body(direction)
        if wall_type == 'teleport':
            if s.snake_body[0].x > 760:
                s.snake_body[0].x = 0
            if s.snake_body[0].x < 0:
                s.snake_body[0].x = 760
            if s.snake_body[0].y > 760:
                s.snake_body[0].y = 0
            if s.snake_body[0].y < 0:
                s.snake_body[0].y = 760
    if game_over == True:
        bg1 = bg2
        screen.blit(over_bg1, (408, 400))
        pygame.draw.rect(screen, (74, 196, 251), (408, 200, 720, 240))
        screen.blit(over_bg2_b, (408, 320))
        screen.blit(score_img, (700, 210))
        screen.blit(high_score_img, (700, 270))
        score_text = font1.render(f'{score}', True, colors['white'])
        high_score_text = font1.render(f'{max(high_score)}', True, colors['white'])
        screen.blit(score_text, ((800, 210)))
        screen.blit(high_score_text, ((800, 275)))
        play.draw(screen)
        settings.draw(screen)
        exit.draw(screen)
        if settings_tab == False:
            play.check_click()
            settings.check_click()
            exit.check_click()
        if settings_tab == True:
            if settings_tab == True:
                settings_text = []
                settings_text.append(font1.render('Key Bindings', True, colors['white']))
                settings_text.append(font2.render('UP', True, colors['white']))
                settings_text.append(font2.render('DOWN', True, colors['white']))
                settings_text.append(font2.render('LEFT', True, colors['white']))
                settings_text.append(font2.render('RIGHT', True, colors['white']))
                settings_text.append(font2.render('BACK / PAUSE', True, colors['white']))
                settings_text.append(font2.render('SELECT', True, colors['white']))
                settings_text.append(font2.render('AUDIO', True, colors['white']))
                settings_text.append(font2.render('WALL TYPE', True, colors['white']))
                settings_text.append(font2.render('SPEED', True, colors['white']))
                pygame.draw.rect(screen, (74, 196, 251), (a[0] + 160, a[1] + 160, 480, 480))
                pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 253), (a[0] + 579, a[1] + 281), 3)
                pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 293), (a[0] + 579, a[1] + 321), 3)
                pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 333), (a[0] + 579, a[1] + 361), 3)
                pygame.draw.line(screen, colors['white'], (a[0] + 579, a[1] + 370), (a[0] + 579, a[1] + 398), 3)
                screen.blit(up_key, (a[0] + 540, a[1] + 253))
                screen.blit(down_key, (a[0] + 540, a[1] + 292))
                screen.blit(left_key, (a[0] + 540, a[1] + 333))
                screen.blit(right_key, (a[0] + 540, a[1] + 369))
                screen.blit(w_key, (a[0] + 590, a[1] + 253))
                screen.blit(s_key, (a[0] + 590, a[1] + 292))
                screen.blit(a_key, (a[0] + 590, a[1] + 333))
                screen.blit(d_key, (a[0] + 590, a[1] + 369))
                screen.blit(esc_key, (a[0] + 565, a[1] + 405))
                screen.blit(lmb, (a[0] + 565, a[1] + 441))
                pygame.draw.line(screen, colors['white'], (a[0] + 180, a[1] + 486), (a[0] + 620, a[1] + 486), 3)
                pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 500, 30, 30), 3)
                pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 547, 30, 30), 3)
                pygame.draw.rect(screen, colors['white'], (a[0] + 590, a[1] + 595, 30, 30), 3)
                if audio == True:
                    pygame.draw.circle(screen, colors['white'], (a[0] + 590 + 15, a[1] + 500 + 15), 5)
                screen.blit(settings_text[0], (a[0] + 240, a[1] + 180))
                screen.blit(settings_text[1], (a[0] + 180, a[1] + 253))
                screen.blit(settings_text[2], (a[0] + 180, a[1] + 293))
                screen.blit(settings_text[3], (a[0] + 180, a[1] + 333))
                screen.blit(settings_text[4], (a[0] + 180, a[1] + 370))
                screen.blit(settings_text[5], (a[0] + 180, a[1] + 406))
                screen.blit(settings_text[6], (a[0] + 180, a[1] + 442))
                screen.blit(settings_text[7], (a[0] + 180, a[1] + 502))
                screen.blit(settings_text[8], (a[0] + 180, a[1] + 547))
                screen.blit(settings_text[9], (a[0] + 180, a[1] + 594))
                if wall_type == 'teleport':
                    screen.blit(teleport, (a[0] + 591, a[1] + 547))
                if wall_type == 'solid':
                    screen.blit(solid, (a[0] + 591, a[1] + 547))
                if level == level0:
                    screen.blit(level0, (a[0] + 590, a[1] + 593))
                if level == level1:
                    screen.blit(level1, (a[0] + 590, a[1] + 595))
                if level == level2:
                    screen.blit(level2, (a[0] + 590, a[1] + 594))
        if play.status == 'play':
            game_over = False
            s = Snake()
            play.status = None
            direction = None
            score = 0
        elif settings.status == 'settings':
            settings.status = None
            settings_tab = True
        elif exit.status == 'exit':
            exit.status = None
            exit_status = True
        if exit_status == True:
            screen.fill((0, 0, 0))
            exit_game.draw(screen)
            exit_desktop.draw(screen)
            exit_cancel.draw(screen)
            exit_game.check_click()
            exit_desktop.check_click()
            exit_cancel.check_click()
            if exit_cancel.status == 'cancel':
                exit_cancel.status = None
                exit_status = False
            if exit_desktop.status == 'exit_whole':
                exit_cancel.status = None
                exit_status = False
                return (max(high_score), 'whole')
            if exit_game.status == 'exit_snake_game':
                exit_game.status = None
                game_over = False
                s = Snake()
                play.status = None
                direction = None
                score = 0
                wall_type = 'teleport'
                speed = 0
                direction = None
                game_over = False
                menu = True
                pause = False
                score = 0
                spawn = True
                food = []
                current_food = 0
                exit_status = False
                return (max(high_score), 'menu')
    pygame.display.update()


while main() != 'exit':
    pass
