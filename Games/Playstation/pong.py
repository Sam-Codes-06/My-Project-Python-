import pygame
import random
import socket
from data5 import button
import pickle

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
colors = ['#cd6155', '#e74c3c', '#922b21', '#641e16', '#78281f', '#f1948a', '#9b59b6', '#bb8fce', '#6c3483', '#5b2c6f',
          '#5499c7', '#85c1e9', '#247a13', '#1a5276', '#1b4f72', '#76d7c4', '#45b39d', '#17a589', '#117864', '#0b5345',
          '#7dcea0', '#58d68d', '#229954', '#1d8348', '#f9e79f', '#f8c471', '#f4d03f', '#d68910', '#9a7d0a', '#f0b27a',
          '#d35400', '#935116', '#797d7f', '#424949', '#5d6d73', '#34495e', '#212f3d', '#979a9a', '#f7dc6f', '#aed6f1',
          ]
menu = True
current_bg = colors[random.randint(0, len(colors) - 1)]
type = 0
multi = None
sound = True
joiner, j_add = None, None
server, client = None, None
connected = False
s_on, s_off, life = pygame.image.load('data5/sound_on.png'), pygame.image.load('data5/sound_off.png'), pygame.image.load(
    'data5/heart.png')
begin = 0
typing = None
c_ip, c_port = '', ''
font = pygame.font.Font(None, 60)
error_typing = False
single_score = 0
single_life = 3
multi_life1, multi_life2 = 3, 3
multi_score1, multi_score2 = 0, 0
score_text = pygame.font.Font(None, 48)
single_over, multi_over1, multi_over2 = False, False, False
multi_collided = False
disconnect = None
multi_game_over = False
single_scores = [0]
multi_scores = [0]


class Ball():
    def __init__(self, type):
        self.x, self.y = (width / 2) - 15, (height / 2) - 15
        a = random.randint(0, 3)
        if a == 0:
            self.dir = [1, 1]
        if a == 1:
            self.dir = [-1, 1]
        if a == 2:
            self.dir = [1, -1]
        if a == 3:
            self.dir = [-1, -1]
        self.ball_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)

    def mechanics(self):
        self.ball_rect.x, self.ball_rect.y = self.x, self.y
        pygame.draw.ellipse(screen, (0, 0, 0), self.ball_rect)
        pygame.draw.ellipse(screen, (255, 255, 255),
                            (self.ball_rect.x + 1, self.ball_rect.y + 1, self.ball_rect.w - 2, self.ball_rect.h - 2))


class Bar():
    def __init__(self, x, y, type):
        self.type = type
        self.x, self.y = x, y

    def mechanics(self):
        if self.type == 2:
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 19, 104))
            self.bar_rect = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 15, 100))
        else:
            pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, 104, 19))
            self.bar_rect = pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 100, 15))


def bg():
    global play1, play2, exit, run, menu, type, sound, multi, begin, single_over, multi_game_over, multi_over1, single_score, multi_score1, multi_score2, multi_over2, multi_life1, multi_life2, current
    screen.fill((current_bg))
    if menu == False:
        if type == 2:
            pygame.draw.line(screen, (255, 255, 255), ((width / 2), 5), (width / 2, height - 5))
    if menu == True:
        rect = pygame.Rect(0, 0, width, height)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (0, 0, 0, 150), shape_surf.get_rect())
        screen.blit(shape_surf, rect)
        if single_over == True:
            if single_score not in single_scores:
                single_scores.append(single_score)
            screen.blit(score_text.render(f'Score: {single_score}', True, '#ffffff'), (10, 10))
            screen.blit(score_text.render('Game Over!', True, '#ff0000'), ((width / 2) - 97, 10))
        if sound == True:
            screen.blit(s_on, (width - 70, 10))
        else:
            screen.blit(s_off, (width - 80, 10))
        if multi_game_over == True:
            a = score_text.render(f'Player1: {multi_score1}', True, '#ffffff')
            screen.blit(a, (10, 10))
            a = score_text.render(f'Player2: {multi_score2}', True, '#ffffff')
            screen.blit(a, (width - 10 - a.get_width(), 10))
            a = score_text.render('Game Over!', True, '#ff0000')
            screen.blit(a, ((width / 2) - a.get_width() / 2, 10))
            if multi_life1 < multi_life2:
                a = score_text.render('Player2 Won', True, '#ffffff')
                screen.blit(a, ((width / 2) - a.get_width() / 2, 80))
            else:
                a = score_text.render('Player1 Won', True, '#ffffff')
                screen.blit(a, ((width / 2) - a.get_width() / 2, 80))
            if current - begin >= 5000:
                multi_game_over = False
                begin = pygame.time.get_ticks()

        if exit.pressed == False:
            if play1.pressed == False and play2.pressed == False:
                play1.draw(screen)
                play1.check_click()
                play2.draw(screen)
                play2.check_click()
                exit.draw(screen)
                exit.check_click()
            if play1.pressed == True:
                play1.pressed = False
                menu = False
                type = 1
                start_game(type)
            if play2.pressed == True:
                host.draw(screen)
                join.draw(screen)
                host.check_click()
                join.check_click()
                back.draw(screen)
                back.check_click()
                if disconnect != None and disconnect != False:
                    multi_over1, multi_over2, multi_life2, multi_life1, multi_score1, multi_score2 = False, False, 3, 3, 0, 0
                    a = font.render(f'{disconnect} left the game!', True, (255, 255, 255))
                    screen.blit(a, ((width / 2) - a.get_width() / 2, 10))
                if back.pressed == True:
                    back.pressed = False
                    play2.pressed = False
                if host.pressed == True:
                    menu = False
                    host.pressed = False
                    multi = 'host'
                    begin = pygame.time.get_ticks()
                if join.pressed == True:
                    menu = False
                    join.pressed = False
                    multi = 'join'
                    begin = pygame.time.get_ticks()
        elif exit.pressed == True:
            screen.fill((0, 0, 0))
            etd.draw(screen)
            etm.draw(screen)
            cancel.draw(screen)
            etd.check_click()
            etm.check_click()
            cancel.check_click()
            if cancel.pressed == True:
                cancel.pressed = False
                exit.pressed = False
            if etd.pressed == True:
                return (max(single_scores), ('whole'))
            if etm.pressed == True:
                return (max(single_scores), ('menu'))



def start_game(type):
    global bx, by, start, move_status, speed1, speed2, ball, bar1, bar2, collided, single_over, single_score, multi_score1, multi_score2, multi_over1, multi_over2
    bx, by = width / 2, height / 2
    start = False
    if type == 2:
        move_status = [None, None]
        speed1, speed2 = 0, 0
        bar1 = Bar(10, (height / 2) - 50, 2)
        bar2 = Bar(width - 25, (height / 2) - 50, 2)
        ball = Ball(2)
    else:
        collided = False
        move_status = [None]
        speed1 = 0
        bar1 = Bar((width / 2) - 50, (height - 25), 1)
        if single_over == True:
            single_over = False
            single_score = 0
        ball = Ball(1)


def get_server():
    global joiner, j_add, connected, type
    joiner, j_add = server.accept()
    start_game(2)
    type = 2
    connected = True


def get_client(o, p):
    global client, connected, c_ip, c_port, error_typing, type
    client = socket.socket()
    try:
        client.connect((o, int(p)))
        connected = True
    except:
        connected = False
    if connected == True:
        start_game(2)
        error_typing = False
        type = 2
        return True
    else:
        client = None
        c_ip = ''
        c_port = ''
        error_typing = True
        return False


play1 = button.Button('Single-Player', 300, 50, ((width / 2) - 150, 350), 3)
play2 = button.Button('Multi-Player', 300, 50, ((width / 2) - 150, 410), 3)
exit = button.Button('Exit', 300, 50, ((width / 2) - 150, 470), 3)
etd = button.Button('Exit to Desktop', 330, 60, ((width - 330) / 2, 380), 3)
etm = button.Button('Exit to Main-Menu', 330, 60, ((width - 330) / 2, 300), 3)
cancel = button.Button('Cancel', 330, 60, ((width - 330) / 2, 460), 3)
host = button.Button('Host', 300, 50, ((width / 2) - 150, 350), 3)
join = button.Button('Join', 300, 50, ((width / 2) - 150, 410), 3)
back = button.Button('Back', 300, 50, ((width / 2) - 150, 470), 3)
ok = button.Button('OK', 100, 50, (((width / 2) - 20), (height / 2) + 25), 3)
hit, wall, out = pygame.mixer.Sound('data5/hit.mp3'), pygame.mixer.Sound('data5/wall.mp3'), pygame.mixer.Sound(
    'data5/out.mp3')
wall_collided = False

def main():
    global ball, start, speed1, wall_collided, speed2, width, sound, height, collided, bar1, bar2, move_status, play1, play2, exit, etd, etm, cancel, host, join, back, ok, menu, current_bg, type, multi, joiner, j_add, client, server, connected, begin, typing, c_ip, c_port, font, error_typing, single_score, single_life, multi_life2, multi_life1, multi_score1, multi_score2, single_over, multi_over1, multi_over2, multi_collided, multi_game_over, disconnect
    k = bg()
    if k != None:
        return k
    current = pygame.time.get_ticks()
    if multi != None and connected == False:
        if multi == 'host' and joiner == None:
            server = socket.socket()
            server.bind((f'{socket.gethostbyname(socket.gethostname())}', 9999))
            server.listen(1)
            rect = pygame.Rect(0, 0, width, height)
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 150), shape_surf.get_rect())
            screen.blit(shape_surf, rect)
            text1 = button.Button('Waiting for opponent, do not close/click the window!', width - 190, 40, (100, 80), 3)
            text2 = button.Button(f'IP: {socket.gethostbyname(socket.gethostname())}', width - 550, 10, (290, 150), 3)
            text3 = button.Button('Port: 9999', 200, 50, (687, 185), 3)
            text4 = button.Button('* Use Port-Forwarding to play WAN.', 500, 70, (50, height - 70), 3)
            text1.draw(screen)
            text2.draw(screen)
            text3.draw(screen)
            text4.draw(screen)
            if current - begin >= 1000:
                get_server()
                begin = current
        elif multi == 'join' and client == None:
            rect = pygame.Rect(0, 0, width, height)
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, (0, 0, 0, 150), shape_surf.get_rect())
            screen.blit(shape_surf, rect)
            pygame.draw.rect(screen, (0, 0, 0), ((width / 2) - 120, (height / 2) - 100, 300, 50), 1, 0)
            pygame.draw.rect(screen, (0, 0, 0), ((width / 2) - 120, (height / 2) - 40, 300, 50), 1, 0)
            ok.draw(screen)
            ok.check_click()
            ft1 = font.render('IP', True, '#ffffff')
            ft2 = font.render('Port', True, '#ffffff')
            screen.blit(ft1, ((width / 2) - 187, (height / 2) - 94))
            screen.blit(ft2, ((width / 2) - 210, (height / 2) - 33))
            ip_text = font.render(c_ip, True, '#ffffff')
            v = ip_text.get_rect()
            if typing == 'ip':
                pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 113 + v.w, (height / 2 - 93), 2, 35))
            screen.blit(ip_text, ((width / 2) - 115, (height / 2) - 94))
            port_text = font.render(c_port, True, '#ffffff')
            v = port_text.get_rect()
            if error_typing == True:
                if c_ip == '' and c_port == '':
                    ft3 = font.render(
                        '#Can not connect, please ensure that the IP address and Port no. are correct',
                        True, '#ff0000')
                    ft4 = font.render('and opponent has hosted!', True, '#ff0000')
                    screen.blit(ft3, (10, 10))
                    screen.blit(ft4, (10, 50))
            if typing == 'port':
                pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 113 + v.w, (height / 2 - 93 + 61), 2, 35))
            screen.blit(port_text, ((width / 2) - 113, (height / 2) - 33))
            if ok.pressed == True:
                if not get_client(c_ip, c_port):
                    ok.pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if menu == True:
                m, n = pygame.mouse.get_pos()
                if m >= width - 70 and m <= width - 6 and n >= 10 and n <= 74:
                    if sound == True:
                        sound = False
                    else:
                        sound = True
                if play1.under_stress == True:
                    play1.pressed = True
                if play2.under_stress == True:
                    play2.pressed = True
                    disconnect = None
                if cancel.under_stress == True and exit.pressed == True:
                    cancel.pressed = True
                if exit.under_stress == True:
                    exit.pressed = True
                if etd.under_stress == True:
                    etd.pressed = True
                if etm.under_stress == True:
                    etm.pressed = True
                if host.under_stress == True:
                    host.pressed = True
                if join.under_stress == True:
                    join.pressed = True
                if back.under_stress == True:
                    back.pressed = True
            if ok.under_stress == True:
                if c_ip != '' and c_port != '':
                    ok.pressed = True
            if menu == False:
                if multi == 'join':
                    m, n = pygame.mouse.get_pos()
                    if m >= (width / 2) - 150 and m <= (width / 2) + 150 and n >= (height / 2) - 100 and n <= (
                            height / 2) - 50:
                        typing = 'ip'
                    elif m >= (width / 2) - 150 and m <= (width / 2) + 150 and n >= (height / 2) - 40 and n <= (
                            height / 2) + 10:
                        typing = 'port'
                    else:
                        typing = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if typing == 'ip' and len(c_ip) > 0:
                    m = c_ip
                    c_ip = ''
                    for i in range(0, len(m) - 1):
                        c_ip += m[i]
                if typing == 'port' and len(c_port) > 0:
                    m = c_port
                    c_port = ''
                    for i in range(0, len(m) - 1):
                        c_port += m[i]
            else:
                if typing == 'ip':
                    o = event.unicode
                    if o in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'):
                        c_ip += o
                if typing == 'port':
                    o = event.unicode
                    if o in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                        c_port += o
            if menu == False:
                if event.key == pygame.K_SPACE:
                    if start == False:
                        if multi == 'host' or type == 1:
                            start = True
                    current_bg = colors[random.randint(0, len(colors) - 1)]
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_status = ['right']
                    speed1 = 2
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_status = ['left']
                    speed1 = -2
                if multi == 'host' and connected == True:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        move_status[0] = 'up'
                        speed1 = -3
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        move_status[0] = 'down'
                        speed1 = 3
                if multi == 'join' and connected == True:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        move_status[1] = 'up'
                        speed2 = -3
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        move_status[1] = 'down'
                        speed2 = 3


        if event.type == pygame.KEYUP and menu == False:
            if type == 2:
                move_status = [None, None]
                speed1, speed2 = 0, 0
            else:
                move_status = [None]
                speed1 = 0
    if menu == False and type == 2:
        c = ball.ball_rect.x - width / 2
        if c <= 0:
            c = -c
        if c <= 100:
            multi_collided = False
        if multi == 'host':
            try:
                disconnect = False
                joiner.send(
                    pickle.dumps([bar1.x, bar1.y, ball.x, ball.y, ball.dir, multi_score1, multi_over1, multi_life1]))
                data = pickle.loads((joiner.recv(1024)))
                bar2.x, bar2.y, multi_score2, multi_over2, multi_life2 = data[0], data[1], data[2], data[3], data[4]
            except Exception as e:
                if e != TypeError and e != SyntaxError and e != SyntaxWarning and e != EOFError:
                    connected = False
                    type = 0
                    menu = True
                    disconnect = 'Player 2'
                    joiner.close()
                    joiner = None
                    multi = None
        if multi == 'join':
            try:
                if multi_game_over == False:
                    disconnect = False
                    client.send(pickle.dumps([bar2.x, bar2.y, multi_score2, multi_over2, multi_life2]))
                    data = pickle.loads((client.recv(1024)))
                    bar1.x, bar1.y, ball.x, ball.y, ball.dir, multi_score1, multi_over1, multi_life1 = data[0], data[1], \
                                                                                                       data[2], data[3], \
                                                                                                       data[4], data[5], \
                                                                                                       data[6], data[7]
            except Exception as e:
                if e != TypeError and e != SyntaxError and e != SyntaxWarning and e != EOFError:
                    connected = False
                    type = 0
                    menu = True
                    disconnect = 'Player 1'
                    client.close()
                    client = None
                    multi = None
        a = score_text.render(f'Player1: {multi_score1}', True, '#ffffff')
        screen.blit(a, (10, 10))
        a = score_text.render(f'Player2: {multi_score2}', True, '#ffffff')
        screen.blit(a, (width - 10 - a.get_width(), 10))
        if multi_life1 == 3:
            screen.blit(life, ((width / 2) - 38, 10))
            screen.blit(life, ((width / 2) - 78, 10))
            screen.blit(life, ((width / 2) - 118, 10))
        if multi_life2 == 3:
            screen.blit(life, ((width / 2) + 6, 10))
            screen.blit(life, ((width / 2) + 46, 10))
            screen.blit(life, ((width / 2) + 86, 10))
        if multi_life1 == 2:
            screen.blit(life, ((width / 2) - 38, 10))
            screen.blit(life, ((width / 2) - 78, 10))
        if multi_life2 == 2:
            screen.blit(life, ((width / 2) + 6, 10))
            screen.blit(life, ((width / 2) + 46, 10))
        if multi_life1 == 1:
            screen.blit(life, ((width / 2) - 38, 10))
        if multi_life2 == 1:
            screen.blit(life, ((width / 2) + 6, 10))
        if multi_life1 < 0 or multi_life2 < 0:
            begin = pygame.time.get_ticks()
            multi_game_over = True
            if multi == ' host':
                if multi_score1 not in multi_scores:
                    multi_scores.append(multi_score1)
            else:
                if multi_score2 not in multi_scores:
                    multi_scores.append(multi_score2)
            play2.pressed = False
            menu = True
            type = 0
            multi = None
            server, client = None, None
            joiner, j_add = None, None
            connected = False
            typing = None
            c_ip, c_port = None, None
            error_typing = False
            multi_collided = False
            disconnect = False
            ok.pressed = False
        ball.mechanics()
        bar1.mechanics()
        bar2.mechanics()
        if ball.ball_rect.colliderect(bar1.bar_rect) and multi_collided == False:
            multi_collided = True
            if sound == True:
                hit.play()
            ball.dir[0] *= -1
            ball.dir[1] = ball.dir[1] + 0.5 * speed1
            multi_score1 += 1
        elif ball.ball_rect.colliderect(bar2.bar_rect) and multi_collided == False:
            multi_collided = True
            if sound == True:
                hit.play()
            ball.dir[0] *= -1
            ball.dir[1] = ball.dir[1] + 0.5 * speed2
            multi_score2 += 1
        if ball.y <= 0 or ball.y >= height - 30:
            ball.dir[1] *= -1
            if sound == True:
                wall.play()
            ball.dir[1] = ball.dir[1] * 0.9999
        if ball.x <= -30:
            start = False
            ball = Ball(2)
            multi_life1 -= 1
            if sound == True:
                out.play()
        if ball.x >= width:
            start = False
            ball = Ball(2)
            if sound == True:
                out.play()
            multi_life2 -= 1
        if start == True:
            ball.x += ball.dir[0] * 1.5
            ball.y += ball.dir[1] * 1.5
        if move_status[0] == 'up':
            if bar1.y > 10:
                bar1.y += speed1
        if move_status[1] == 'up':
            if bar2.y > 10:
                bar2.y += speed2
        if move_status[0] == 'down':
            if bar1.y < height - 110:
                bar1.y += speed1
        if move_status[1] == 'down':
            if bar2.y < height - 110:
                bar2.y += speed2
    if menu == False and type == 1 and single_over == False:
        if ball.x >= 20 and ball.x <= width - 20 and ball.y >= 20:
            wall_collided = False
        screen.blit(score_text.render(f'Score: {single_score}', True, '#ffffff'), (10, 10))
        if single_life == 3:
            screen.blit(life, (width - 40, 5))
            screen.blit(life, (width - 80, 5))
            screen.blit(life, (width - 120, 5))
        if single_life == 2:
            screen.blit(life, (width - 40, 5))
            screen.blit(life, (width - 80, 5))
        if single_life == 1:
            screen.blit(life, (width - 40, 5))
        ball.mechanics()
        bar1.mechanics()
        if start == True:
            ball.x += ball.dir[0]
            ball.y += ball.dir[1]
        if move_status == ['right']:
            if bar1.x <= width - 112:
                bar1.x += speed1
        if move_status == ['left']:
            if bar1.x >= 12:
                bar1.x += speed1
        if ball.x <= 0 or ball.x >= width - 30 and wall_collided ==  False:
            ball.dir[0] *= -1
            if sound == True:
                wall.play()
            collided = False
            ball.dir[0] = ball.dir[0] * 0.9999
            wall_collided = True
        if ball.y <= 0 and wall_collided ==  False:
            ball.dir[1] *= -1
            collided = False
            if sound == True:
                wall.play()
            wall_collided = True
            ball.dir[1] = ball.dir[1] * 0.9999
        if ball.ball_rect.colliderect(bar1.bar_rect) and ball.ball_rect.y <= height - 25 and collided == False:
            single_score += 1
            if sound == True:
                hit.play()
            collided = True
            ball.dir[1] *= -1
            ball.dir[0] = ball.dir[0] + 0.3 * speed1
        if ball.y >= height:
            single_life -= 1
            if sound == True:
                out.play()
            start_game(1)
        if single_life < 0:
            single_life = 3
            single_over = True
            menu = True
            type = 0
    pygame.display.update()