# IMPORT LIBRARIES AND MODULES
import pygame
import threading
import random
import math
from pygame import mixer
import os
import sys

# START PYGAME
pygame.init()
# GAME WINDOW VARIABLES AND TOOLS
game_state = True
height, width = 600, 1230
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load('data/spaceship.png'))
background_img = pygame.image.load('data/bg.jpg')
main_bg = pygame.image.load('data/main_menu.png')
# MENU TOOLS
play, over = 0, 0
load, loading = 0, 0
win = 0
win_text_style = pygame.font.Font(None, 100)
win_text = win_text_style.render("You Won", True, (255, 255, 255))
end_text_style = pygame.font.Font(None, 60)
end_text = end_text_style.render("Press Anywhere To Exit", True, (255, 255, 255))
# SPACESHIP VARIABLE AND TOOLS
ship = pygame.image.load('data/ship.png')
ship_rect = ship.get_rect()
ship_x, ship_y = (width / 2) - 32, height - 64
change_in_bullet_x, change_in_ship_y = 0, 0
can_move = 1
# ENEMY VARIABLE AND TOOLS
enemy = []
enemy_rect = []
enemy_x, enemy_y = [], []
enemy_counter = 2
# MAIN ENEMY
main_enemy = []
boss_rect = 0
move_boss_x, move_boss_y = random.randint(10, width - 600), -250
get_ready_style = pygame.font.Font(None, 60)
game_over = get_ready_style.render("GAME OVER", True, (255, 255, 255))
get_ready_text = get_ready_style.render("GET READY!!!", True, (255, 255, 255))
get_ready_player, boss_arriving, call_boss, life_of_boss, life_boss = 0, 0, 0, 150, 50
boss_bullet, laser_on, laser, laser_off_timer = [], 0, [], 0
boss_healer, healer_rect, healer_called, bye_healer, healer_x, healer_y, healer_side, healing, stopping = [], 0, 0, 0, 0, -100, 0, 0, 1
a = 0
# USED TO GET A RANDOM NUMBER EVERY 2 SECONDS
# SO AS TO CHAMGE THE DIRECTION OF ENEMY EVERY 2 SECONDS
get_rand = pygame.USEREVENT
pygame.time.set_timer(get_rand, 2000)
# BULLET VARIABLES AND TOOLS FOR SHOOTING AND RELOAD FOR SHIP AND ENEMY
bullet_ship = []
bullet_enemy = []
timer = 0
ammo = 12
bullet_state = "ready"
bullet_x, bullet_y = 0, 0
red = (255, 0, 0)
green = (10, 250, 10)
reload_state = False
event_rate = 0
# TEXTS AND EXTRAS
n = 5
score = 0
score_style = pygame.font.Font(None, 45)
ammo_style = pygame.font.Font(None, 30)
p_style = pygame.font.Font(None, 100)
q_style = pygame.font.Font(None, 100)
play_text = p_style.render("Play", True, (255, 255, 255))
play_again = p_style.render("Play Again", True, (255, 255, 255))
quit_text = p_style.render("Quit", True, (255, 255, 255))
mx, my = 0, 0
# HEAL
heart = pygame.image.load('data/heart.png')
lh, ch, rh = 1, 1, 1
extra_he = []
ehe_rect = 0
drop_x_he, drop_y_he = 0, -100
# SCORE
ss = pygame.image.load('data/score_sac.png')
extra_sc = []
drop_x_sc, drop_y_sc = 0, -100
esc_rect = 0
# FREEZE
fr = pygame.image.load('data/freeze.png')
fre = pygame.image.load('data/frozen_enemy.png')
extra_fr = []
efr_rect = 0
drop_x_fr, drop_y_fr = 0, -100
freeze, stop_freeze = 0, 0
# POWER
sh = pygame.image.load('data/power.png')
extra_pw = []
esh_rect = 0
drop_x_sh, drop_y_sh = 0, -100
activate_power, power_timer, immortal = 0, 0, 0


# FUNCTIONS FOR SHIP, ENEMY, BULLET & BULLET RELOAd FOR SHIP AND ENEMY & SHIP
def show_off():
    global play, loading, load
    play = 1
    loading = 0
    load.cancel()


def player(x, y):
    screen.blit(ship, (x, y))


# SHOOTING BULLLET FOR SHIP
def shoot_ship(bullet):
    global bullet_state
    global ammo
    global bullet_x
    global bullet_y
    bullet_x, bullet_y = ship_x, ship_y
    if bullet_state == "fire":
        bullet.append(pygame.draw.rect(screen, red, (bullet_x + 30, bullet_y - 2, 4, 10)))
        bullet_state = "ready"
        ammo -= 1
    for i in bullet:
        i.y -= 15
        pygame.draw.rect(screen, red, i)
        if i.y < -64:
            bullet.remove(i)


# BULLET RELOAD FOR SHIP
def reload():
    global ammo
    if immortal == 0:
        ammo = 12
    timer.cancel()


# BULLET RELOAD CALL AFTER 4 SECONDS FOR SHIP
def reloading():
    global reload_state
    global ammo
    global timer
    if reload_state == False:
        reload_state = True
        timer = threading.Timer(4.0, reload)
        timer.start()


# ENEMY SHOOTS BULLETS
def spawn_enemy():
    global enemy_counter
    enemy.append(pygame.image.load('data/enemy.png'))
    a = random.randint(150, 990)
    enemy_x.append(a)
    enemy_y.append(-100)
    for i in range(len(enemy)):
        enemy_rect.append(enemy[i].get_rect())
    enemy_counter -= 1


def shoot_enemy(bullet):
    for i in bullet:
        i.y += 6
        pygame.draw.rect(screen, red, i)


def despawn(x):
    if enemy_x[x] in enemy_x:
        enemy_x.remove(enemy_x[x])
    if enemy_y[x] in enemy_y:
        enemy_y.remove(enemy_y[x])
    if enemy[x] in enemy:
        enemy.remove(enemy[x])


def boss_coming():
    global call_boss, boss_arriving, lh, rh, can_move
    lh = 1
    ch = 1
    rh = 1
    boss_arriving = True
    can_move = 1
    call_boss.cancel()


def show_text(sco, amm):
    global lh, rh, ch, boss_arriving, call_boss, text_score
    text_score = score_style.render("Score:" + str(sco), True, (255, 255, 255))
    call_boss = threading.Timer(1.0, boss_coming)
    if amm >= 10:
        text_ammo = ammo_style.render("Ammo:" + str(amm), True, (255, 255, 255))
    elif amm <= 9:
        text_ammo = ammo_style.render("Ammo:0" + str(amm), True, (255, 255, 255))
    screen.blit(text_score, (5, 5))
    if rh == 1:
        screen.blit(heart, (width - 35, 5))
    if ch == 1:
        screen.blit(heart, (width - 73, 5))
    if lh == 1:
        screen.blit(heart, (width - 111, 5))
    screen.blit(text_ammo, (width - 97, 40))
    if get_ready_player == True and boss_arriving == 0:
        screen.blit(get_ready_text, (width / 2 - 120, height / 2 - 30))
        call_boss.start()


def drop_extra_he(y):
    global drop_x_he, ehe_rect, extra_he, lh, ch, drop_y_he
    if len(extra_he) == 1:
        ehe_rect = extra_he[0].get_rect()
    ehe_rect.y = y
    ehe_rect.x = drop_x_he
    screen.blit(extra_he[0], (drop_x_he, y))
    if ehe_rect.colliderect(ship_rect) and (boss_arriving == 0 or get_ready_player == True) and len(main_enemy) == 0:
        if abs(ehe_rect.top - ship_rect.bottom <= 8):
            if rh == 1:
                lh = 1
                ch = 1
                extra_he.remove(extra_he[0])
                drop_y_he = -100
                drop_x_he = random.randint(64, width - 64)


def drop_extra_sc(y):
    global drop_x_sc, drop_y_sc, esc_rect, extra_sc, score
    if len(extra_sc) == 1:
        esc_rect = extra_sc[0].get_rect()
    esc_rect.y = y
    esc_rect.x = drop_x_sc
    screen.blit(extra_sc[0], (drop_x_sc, y))
    if esc_rect.colliderect(ship_rect) and rh == 1 and boss_arriving == 0 or get_ready_player == 1 and len(
            main_enemy) == 0:
        if abs(esc_rect.top - ship_rect.bottom <= 8):
            extra_sc.remove(extra_sc[0])
            score += 100
            drop_y_sc = -100
            drop_x_sc = random.randint(64, width - 64)


def stop_power():
    global power_timer, activate_power, immortal, ammo
    immortal = 0
    ammo = 12
    activate_power = 0
    if power_timer != 0:
        power_timer.cancel()


def drop_extra_pw(y):
    global drop_x_sh, drop_y_sh, esh_rect, extra_pw, activate_power, power_timer, immortal, lh, ch, ammo
    power_timer = threading.Timer(6.0, stop_power)
    if len(extra_pw) == 1:
        esh_rect = extra_pw[0].get_rect()
    esh_rect.y = y
    esh_rect.x = drop_x_sh
    screen.blit(extra_pw[0], (drop_x_sh, y))
    if esh_rect.colliderect(ship_rect) and rh == 1 and boss_arriving == 0 or get_ready_player == 1 and len(
            main_enemy) == 0:
        if abs(esh_rect.top - ship_rect.bottom <= 8):
            if rh == 1:
                extra_pw.remove(extra_pw[0])
                lh, ch = 1, 1
                ammo = 99
                drop_y_sh = -100
                drop_x_sh = random.randint(64, width - 64)
                activate_power = True
                immortal = True
                power_timer.start()


def unfreeze_enemy():
    global freeze, stop_freeze
    freeze = 0
    if freeze != 0:
        stop_freeze.cancel()


def drop_extra_fr(y):
    global drop_x_fr, drop_y_fr, extra_fr, efr_rect, freeze, stop_freeze
    stop_freeze = threading.Timer(5.0, unfreeze_enemy)
    if len(extra_fr) == 1:
        efr_rect = extra_fr[0].get_rect()
    efr_rect.y = y
    efr_rect.x = drop_x_fr
    screen.blit(extra_fr[0], (drop_x_fr, y))
    if efr_rect.colliderect(ship_rect) and rh == 1 and boss_arriving == 0 or get_ready_player == 1 and len(
            main_enemy) == 0:
        if abs(efr_rect.top - ship_rect.bottom <= 8):
            extra_fr.remove(extra_fr[0])
            drop_x_fr = random.randint(64, width - 64)
            drop_y_fr = -100
            freeze = True
            stop_freeze.start()


def turn_off_laser():
    global laser_on, laser_off_timer
    if len(laser) == 1:
        laser_on = 0
        laser.remove(laser[0])
        laser_off_timer.cancel()


def stop_healing():
    global healer_called, healer_side, healing, bye_healer, boss_healer, healer_x, healer_y, stopping, life_of_boss, life_boss, heaaler_rect
    if len(boss_healer) == 1 and healer_x == move_boss_x + 397:
        healer_called = 0
        healer_side = 0
        healing = 0
        healer_x = 0
        healer_y = -100
        stopping = 1
        boss_healer.remove(boss_healer[0])
        life_of_boss = 150
        life_boss = 50
        healer_rect = 0
        bye_healer.cancel()
    if len(boss_healer) == 1 and healer_x == move_boss_x + 396:
        healer_called = 0
        healer_side = 0
        healing = 0
        healer_x = 0
        healer_y = -100
        stopping = 1
        boss_healer.remove(boss_healer[0])
        life_of_boss = 150
        life_boss = 50
        healer_rect = 0
        bye_healer.cancel()


def main_enemy_script():
    global move_boss_y, move_boss_x, boss_rect, life_of_boss, life_boss, laser_off_timer, laser_on, healer_called, healer_side, healing, healer_x, healer_y, bye_healer, stopping, healer_rect
    bye_healer = threading.Timer(2.0, stop_healing)
    laser_off_timer = threading.Timer(5.0, turn_off_laser)
    if boss_arriving == True and move_boss_y < 0 and boss_rect != 0:
        pygame.draw.rect(screen, green, (move_boss_x, move_boss_y + life_boss, 15, life_of_boss))
        move_boss_y = move_boss_y + 1
        boss_rect.x = move_boss_x
        boss_rect.y = move_boss_y
        screen.blit(main_enemy[0], (move_boss_x, move_boss_y))
    elif boss_arriving == True and move_boss_y >= 0:
        if dir == 0 or dir == 1 or dir == 2:
            if healing == 0 and laser_on == 0:
                move_boss_x -= 2
            boss_rect.x = move_boss_x
            boss_rect.y = move_boss_y
            pygame.draw.rect(screen, green, (move_boss_x, move_boss_y + life_boss, 15, life_of_boss))
            screen.blit(main_enemy[0], (move_boss_x, move_boss_y))
        if dir == 3 or dir == 4 or dir == 5:
            if healing == 0 and laser:
                move_boss_x += 2
            boss_rect.x = move_boss_x
            boss_rect.y = move_boss_y
            pygame.draw.rect(screen, green, (move_boss_x, move_boss_y + life_boss, 15, life_of_boss))
            screen.blit(main_enemy[0], (move_boss_x, move_boss_y))
        if dir == 6:
            boss_rect.x = move_boss_x
            boss_rect.y = move_boss_y
            pygame.draw.rect(screen, green, (move_boss_x, move_boss_y + life_boss, 15, life_of_boss))
            screen.blit(main_enemy[0], (move_boss_x, move_boss_y))
        if len(laser) == 1:
            for i in laser:
                i.x = move_boss_x + 185
                pygame.draw.rect(screen, red, i)
        if len(laser) == 1 and laser_on == True:
            laser_on = False
            laser_off_timer.start()
        if healer_called == True and move_boss_x >= 516 and healer_side == 0 and len(boss_healer) == 1:
            healer_x = move_boss_x - 60
            healer_called = 0
            healer_side = 1
            healing = 1
        if healer_called == True and move_boss_x + 514 <= width - 516 and healer_side == 0 and len(boss_healer) == 1:
            healer_x = move_boss_x + 514 + 60
            healer_called = 0
            healer_side = 2
            healing = 1
        if healer_side == 1 and healer_y != 200 and healing == 1 and len(boss_healer) == 1:
            healer_y += 3
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if healer_side == 1 and healer_y == 200 and healer_x != move_boss_x + 396 and healing == 1 and len(
                boss_healer) == 1:
            healer_x += 3
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if healer_side == 1 and healer_x == move_boss_x + 396 and healing == 1 and len(boss_healer) == 1:
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if stopping == 1 and healer_x == move_boss_x + 396 and len(boss_healer) == 1 and healer_side == 1:
            bye_healer.start()
            stopping = 0
        if healer_side == 2 and healer_y != 200 and healing == 1 and len(boss_healer) == 1:
            healer_y += 3
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if healer_side == 2 and healer_y == 200 and healer_x != move_boss_x + 397 and healing == 1 and len(
                boss_healer) == 1:
            healer_x -= 3
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if healer_side == 2 and healer_x == move_boss_x + 397 and healing == 1 and len(boss_healer) == 1:
            healer_rect.x = healer_x
            healer_rect.y = healer_y
            screen.blit(boss_healer[0], (healer_x, healer_y))
        if stopping == 1 and healer_x == move_boss_x + 397 and len(boss_healer) == 1 and healer_side == 2:
            bye_healer.start()
            stopping = 0
    if len(main_enemy) > 0:
        if move_boss_x <= 0:
            move_boss_x = 0
        if move_boss_x >= width - 514:
            move_boss_x = width - 514


while game_state:
    if win == 1 and play == 0:
        screen.blit(background_img, (0, 0))
        screen.blit(win_text, (490, 150))
        screen.blit(text_score, (550, 250))
        screen.blit(end_text, (410, 400))
    if play == 0 and over == 1 and win == 0:
        enemy.clear()
        bullet_enemy.clear()
        boss_bullet.clear()
        laser.clear()
        extra_he.clear()
        extra_sc.clear()
        extra_fr.clear()
        extra_pw.clear()
        enemy_x.clear()
        boss_healer.clear()
        enemy_y.clear()
        main_enemy.clear()
        bullet_ship.clear()
        laser_on = 0
        move_boss_y, move_boss_x = -250, random.randint(200, width - 800)
        boss_rect = 0
        healer_rect = 0
        activate_power, power_timer, immortal = 0, 0, 0
        screen.blit(background_img, (0, 0))
        screen.blit(game_over, (495, 100))
        screen.blit(text_score, (558, 150))
        screen.blit(play_again, (440, 250))
        screen.blit(quit_text, (543, 350))
    if play == 0 and loading == 0 and over == 0 and win == 0:
        screen.blit(main_bg, (0, 0))
        screen.blit(play_text, (545, 250))
        screen.blit(quit_text, (543, 360))
    if play == 0 and loading == 1 and over == 0 and win == 0:
        screen.blit(background_img, (0, 0))
        screen.blit(loading_text, (480, 250))
    get_order = random.randint(1, 400)
    if enemy_counter > 0 and get_order >= 399 and play == 1 and win == 0:
        spawn_enemy()
    if enemy_counter <= 0 and len(enemy) == 0 and get_ready_player == 0 and play == 1:
        enemy_rect.clear()
        get_ready_player = True
        n = 6
        ammo = 12
        main_enemy.append(pygame.image.load('data/main_enemy.png'))
        boss_rect = main_enemy[0].get_rect()
        can_move = 0
        enemy.clear()
        ship_x, ship_y = (width / 2) - 32, height - 64
    if boss_arriving == True or get_ready_player == True and play == 1:
        extra_he.clear()
        extra_sc.clear()
        extra_pw.clear()
        extra_fr.clear()
    # SET BACKGROUND
    if play == 1:
        screen.blit(background_img, (0, 0))
    # CHANGE SHIP, ENEMY & BULLET CO-ORDINATES
    if play == 1:
        player(ship_x, ship_y)
        main_enemy_script()
    for i in range(len(enemy)):
        screen.blit(enemy[i], (enemy_x[i], enemy_y[i]))
        enemy_rect[i].x = enemy_x[i]
        enemy_rect[i].y = enemy_y[i]
    if play == 1:
        shoot_ship(bullet_ship)
        shoot_enemy(bullet_enemy)
    ship_rect.topleft = (0, 0)
    ship_rect.x = ship_x
    ship_rect.y = ship_y
    # GET INPUTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = False
        if event.type == get_rand and play == 1:
            dir = random.randint(0, n)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if win == 1:
                game_state = 0
            if (mx > 550 and mx < 690) and (my > 255 and my < 305) and play == 0:
                load = threading.Timer(2.0, show_off)
                loading_text = get_ready_style.render("Loading Space", True, (255, 255, 255))
                loading = 1
                load.start()
            if (mx > 550 and mx < 690) and (my > 370 and my < 420) and play == 0:
                game_state = 0
            if play == 0 and over == 1 and (mx > 440 and mx < 795) and (my > 250 and my < 315):
                play = 1
                over = 0
                lh, ch, rh = 1, 1, 1
                enemy_counter = 20
                score = 0
                ammo = 12
                n = 5
                ship_x, ship_y = (width / 2) - 32, height - 64
                change_in_bullet_x, change_in_ship_y = 0, 0
                get_ready_player, boss_arriving, call_boss, life_of_boss, life_boss = 0, 0, 0, 150, 50
                drop_x_sh, drop_y_sh = random.randint(64, width - 64), -100
                drop_x_fr, drop_y_fr = random.randint(64, width - 64), -100
                freeze, stop_freeze = 0, 0
                drop_y_he, drop_x_he = -100, random.randint(64, width - 64)
                drop_x_sc, drop_y_sc = random.randint(64, width - 64), -100
                ship_rect = ship.get_rect()
                healer_y = -100
                extra_he.clear()
                extra_sc.clear()
                extra_fr.clear()
                extra_pw.clear()
                enemy_x.clear()
            if play == 0 and over == 1 and (mx > 543 and mx < 691) and (my > 350 and my < 410):
                game_state = 0
        # ON KEY PRESSED
        if event.type == pygame.KEYDOWN and play == 1:
            # MOVE SHIP TO LEFT
            if event.key == pygame.K_LEFT and can_move == 1:
                change_in_bullet_x = -5
            # MOVE SHIP TO RIGHT
            if event.key == pygame.K_RIGHT and can_move == 1:
                change_in_bullet_x = 5
            # MOVE SHIP TO UP
            if event.key == pygame.K_UP and can_move == 1:
                change_in_ship_y = -5
            # MOVE SHIP TO DOWN
            if event.key == pygame.K_DOWN and can_move == 1:
                change_in_ship_y = 5
            # SHOOT BULLET
            if event.key == pygame.K_SPACE:
                if ammo > 0:
                    bullet_state = "fire"
                    reload_state = False
                # BULLET RELOAD
                elif ammo <= 0:
                    reloading()
            if event.key == pygame.K_r and immortal == False:
                reloading()
        # ON KEY RELEASED
        if event.type == pygame.KEYUP and play == 1:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_in_bullet_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                change_in_ship_y = 0
    # MOVEMENT OF SPACESHIP
    ship_x += change_in_bullet_x
    ship_y += change_in_ship_y
    # MOVEMENT BOUNDERY OF SPACESHIP
    if ship_x < 0:
        ship_x = 0
    if ship_x >= width - 64:
        ship_x = width - 64
    if ship_y < 0:
        ship_y = 0
    if ship_y >= height - 75:
        ship_y = height - 75
    # MOVEMENT OF ENEMY
    for i in range(len(enemy)):
        if enemy_y[i] <= 0 and freeze == False and play == 1:
            enemy_y[i] += 0.5
        if enemy_y[i] > 0 and freeze == False and play == 1:
            if dir == 0:
                enemy_x[i] -= 1
            if dir == 1:
                enemy_x[i] -= 1
                enemy_y[i] += 1
            if dir == 2:
                enemy_y[i] += 1
            if dir == 3:
                enemy_y[i] += 1
                enemy_x[i] += 1
            if dir == 4:
                enemy_x[i] += 1
            if enemy_x[i] <= 0:
                enemy_x[i] = 0
            if enemy_x[i] >= width - 64:
                enemy_x[i] = width - 64
    # ENEMY SHOOTS BULLET LOGIC
    event_rate = random.randint(1, 800)
    for i in range(len(enemy)):
        try:
            if (event_rate >= 795 and enemy_y[i] >= 0) and (enemy[i] in enemy) and freeze == False and play == 1:
                bullet_enemy.append(pygame.draw.rect(screen, red, (enemy_x[i] + 31, enemy_y[i] + 60, 4, 10)))
        except:
            break
    if lh == 0 and event_rate > 797 and len(
            extra_he) < 1 and rh == 1 and boss_arriving == 0 and get_ready_player == 0 and play == 1:
        extra_he.append(heart)
        drop_x_he = random.randint(64, width - 64)
    if len(extra_he) == 1:
        drop_y_he += 1
        drop_extra_he(drop_y_he)
    if len(extra_sc) == 0 and event_rate % 400 == 0 and rh == 1 and boss_arriving == 0 and get_ready_player == 0 and play == 1:
        extra_sc.append(ss)
        drop_x_sc = random.randint(64, width - 64)
    if len(extra_sc) == 1:
        drop_y_sc += 1.5
        drop_extra_sc(drop_y_sc)
    if len(extra_pw) == 0 and event_rate < 2 and activate_power == False and rh == 1 and boss_arriving == 0 and get_ready_player == 0 and play == 1:
        extra_pw.append(sh)
        drop_x_sh = random.randint(64, width - 64)
    if len(extra_pw) == 1:
        drop_y_sh += 1
        drop_extra_pw(drop_y_sh)
    if len(extra_fr) == 0 and event_rate > 798 and rh == 1 and freeze == False and boss_arriving == 0 and get_ready_player == 0 and play == 1:
        extra_fr.append(fr)
        drop_x_fr = random.randint(64, width - 64)
    if len(extra_fr) == 1:
        drop_y_fr += 1
        drop_extra_fr(drop_y_fr)
    # COLLISIONS DETECTION
    for i in bullet_ship:
        for j in range(len(enemy)):
            if i.colliderect(enemy_rect[j]) and play == 1:
                if abs(i.top - enemy_rect[j].bottom <= 8):
                    if i in bullet_ship:
                        bullet_ship.remove(i)
                        despawn(j)
                        score = score + 10
    for i in bullet_enemy:
        if i.colliderect(ship_rect) and play == 1:
            if abs(i.bottom - ship_rect.top <= 6) or abs(i.left - ship_rect.right <= 6) or abs(
                    i.right - ship_rect.left <= 6):
                if i in bullet_enemy:
                    bullet_enemy.remove(i)
                    if (lh == 1) and (ch == 1) and (rh == 1) and immortal == 0:
                        lh = 0
                    elif (lh == 0) and (ch == 1) and (rh == 1) and immortal == 0:
                        ch = 0
                    elif (lh == 0) and (ch == 0) and (rh == 1) and immortal == 0:
                        rh = 0
    for i in range(len(enemy)):
        if enemy_rect[i].colliderect(ship_rect) and play == 1:
            if abs(enemy_rect[i].bottom - ship_rect.top <= 2) or abs(enemy_rect[i].top - ship_rect.bottom <= 2) or abs(
                    enemy_rect[i].right - ship_rect.left <= 2) or abs(enemy_rect[i].left - ship_rect.right <= 2):
                if (lh == 1) and (ch == 1) and (rh == 1) and immortal == 0:
                    lh = 0
                    ship_y = height + 10
                    ship_x = width / 2
                    enemy_y[i] = height + 64
                elif (lh == 0) and (ch == 1) and (rh == 1) and immortal == 0:
                    ch = 0
                    ship_y = height + 10
                    ship_x = width / 2
                    enemy_y[i] = height + 64
                elif (lh == 0) and (ch == 0) and (rh == 1) and immortal == 0:
                    rh = 0
                    ship_y = height + 10
                    ship_x = width / 2
                    enemy_y[i] = height + 64
    for i in bullet_enemy:
        if i.y >= height + 64:
            bullet_enemy.remove(i)
    for i in range(len(enemy)):
        if enemy_y[i] >= height + 64:
            enemy_y[i] = -100
    # EXTRAS
    if drop_y_he >= height + 64:
        drop_y_he = -100
        drop_x_he = random.randint(0, width - 64)
    if drop_y_sc >= height + 64:
        drop_y_sc = -100
        drop_x_sc = random.randint(0, width - 64)
    if drop_y_sh >= height + 64:
        drop_y_sh = -100
        drop_x_sh = random.randint(64, width - 64)
    if activate_power == True and len(main_enemy) == 0:
        screen.blit(sh, (width - 35, 65))
    if freeze == True and play == 1 and len(main_enemy) == 0:
        screen.blit(fr, (width - 35, 97))
        for i in range(len(enemy)):
            screen.blit(fre, (enemy_x[i], enemy_y[i]))
    if drop_y_fr >= height + 64 and play == 1:
        drop_y_fr = -100
        drop_x_fr = random.randint(64, width - 64)
    if play == 1:
        show_text(score, ammo)
    if event_rate >= 799 and len(main_enemy) == 1 and move_boss_y == 0 and play == 1:
        boss_bullet.append(pygame.draw.rect(screen, red, (move_boss_x + 89, 130, 4, 10)))
        boss_bullet.append(pygame.draw.rect(screen, red, (move_boss_x + 290, 214, 4, 10)))
        boss_bullet.append(pygame.draw.rect(screen, red, (move_boss_x + 410, 170, 4, 10)))
    if event_rate >= 799 and len(laser) == 0 and move_boss_y == 0 and play == 1 and len(main_enemy) == 1:
        laser.append(pygame.draw.rect(screen, red, (move_boss_x + 185, 180, 4, 700)))
        laser_on = True
    if len(boss_bullet) > 0:
        for i in boss_bullet:
            i.y += 6
            pygame.draw.rect(screen, red, i)
    if life_of_boss <= 100 and len(boss_healer) == 0 and event_rate < 5 and move_boss_y == 0 and play == 1:
        boss_healer.append(pygame.image.load('data/boss_healer.png'))
        healer_rect = boss_healer[0].get_rect()
        healer_called = True
    # BOSS COLLISION
    if len(main_enemy) == 1 and (boss_rect.colliderect(ship_rect)) and play == 1:
        if abs(boss_rect.left - ship_rect.right <= 8) or abs(boss_rect.right - ship_rect.left <= 8) or abs(
                boss_rect.bottom - ship_rect.top <= 8):
            lh = 0
            ch = 0
            rh = 0
    for i in boss_bullet:
        if i.colliderect(ship_rect) and play == 1:
            if abs(i.bottom - ship_rect.top <= 2) or abs(i.left - ship_rect.right <= 2) or abs(
                    i.right - ship_rect.left <= 2):
                if i in boss_bullet:
                    boss_bullet.remove(i)
                if (lh == 1) and (ch == 1) and (rh == 1):
                    lh = 0
                elif (lh == 0) and (ch == 1) and (rh == 1):
                    ch = 0
                elif (lh == 0) and (ch == 0) and (rh == 1):
                    rh = 0
    if len(laser) == 1 and laser[0].colliderect(ship_rect) and play == 1:
        if abs(laser[0].left - ship_rect.right <= 2):
            ship_x = laser[0].x - 200
            if (lh == 1) and (ch == 1) and (rh == 1):
                lh = 0
            elif (lh == 0) and (ch == 1) and (rh == 1):
                ch = 0
            elif (lh == 0) and (ch == 0) and (rh == 1):
                rh = 0
        if abs(laser[0].right - ship_rect.left <= 2):
            ship_x = laser[0].x + 200
            if (lh == 1) and (ch == 1) and (rh == 1):
                lh = 0
            elif (lh == 0) and (ch == 1) and (rh == 1):
                ch = 0
            elif (lh == 0) and (ch == 0) and (rh == 1):
                rh = 0
    if len(boss_healer) == 1 and healer_rect.colliderect(ship_rect) and play == 1:
        if abs(healer_rect.bottom - ship_rect.top <= 2) or abs(healer_rect.left - ship_rect.right <= 2) or abs(
                healer_rect.right - ship_rect.left <= 2):
            ship_y = healer_x + 500
            healer_called = 0
            healer_side = 0
            healing = 0
            healer_x = 0
            healer_y = -100
            stopping = 1
            boss_healer.remove(boss_healer[0])
            healer_y = -100
            if (lh == 1) and (ch == 1) and (rh == 1):
                lh = 0
            elif (lh == 0) and (ch == 1) and (rh == 1):
                ch = 0
            elif (lh == 0) and (ch == 0) and (rh == 1):
                rh = 0
    for i in bullet_ship:
        if len(boss_healer) == 1 and i.colliderect(healer_rect) and play == 1:
            if abs(i.top - healer_rect.bottom <= 2):
                if i in bullet_ship:
                    bullet_ship.remove(i)
                    score += 100
                if len(boss_healer) == 1:
                    healer_called = 0
                    healer_side = 0
                    healing = 0
                    healer_x = 0
                    healer_y = -100
                    stopping = 1
                    boss_healer.remove(boss_healer[0])
                    healer_rect = 0
    for i in bullet_ship:
        if boss_rect != 0 and i.colliderect(boss_rect) and play == 1:
            if i in bullet_ship:
                bullet_ship.remove(i)
                score += 10
            if abs(i.top - boss_rect.bottom <= 2):
                life_of_boss -= 3
                life_boss += 3
    if len(extra_he) == 1 and drop_y_he >= height + 64:
        extra_he.remove(extra_he[0])
    if len(extra_sc) == 1 and drop_y_sc >= height + 64:
        extra_sc.remove(extra_sc[0])
    if len(extra_fr) == 1 and drop_y_fr >= height + 64:
        extra_fr.remove(extra_fr[0])
    if len(extra_pw) == 1 and drop_y_sh >= height + 64:
        extra_pw.remove(extra_pw[0])
    if rh == 0 and lh == 0 and ch == 0 and over == 0:
        play = 0
        over = 1
    if move_boss_y == -250 and len(main_enemy) == 1:
        lh, ch, rh = 1, 1, 1
    if healer_x < - 64 or healer_x > 1200 and len(boss_healer) == 1:
        healer_called = 0
        healer_side = 0
        healing = 0
        healer_x = 0
        healer_y = -100
        stopping = 1
        boss_healer.remove(boss_healer[0])
        healer_rect = 0
    if life_of_boss == 0 and win == 0:
        score += 10000
        text_score = score_style.render("Score:" + str(score), True, (255, 255, 255))
        win = 1
        play = 0
    pygame.display.update()
