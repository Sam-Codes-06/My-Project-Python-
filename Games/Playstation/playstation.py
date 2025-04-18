import pygame
import mysql.connector, datetime, time
import snake_game
import _2048
import tetris
import jump_up
import tron
import pong
import importlib

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()
run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}
logo = pygame.image.load('main_data/playstation.png')
g_list = ['Snake Game', '2048', 'Tetris', 'Jump Up', 'Tron', 'Pong']
current_game = None
font = pygame.font.Font(None, 64)

def create_database():
    global db_cursor, mydb
    mydb = mysql.connector.connect(user='root', host='localhost', password='password')
    db_cursor = mydb.cursor(buffered=True)
    db_cursor.execute('create database if not exists playstation')
    db_cursor.execute('use playstation')


def create_table(user):
    db_cursor.execute('show tables')
    a = db_cursor.fetchall()
    for i in a:
        if user.upper() == i[0].upper():
            break
    else:
        create_user_data = f"""
        create table if not exists {user} (
        Game varchar(50), 
        HighScore int(255),
        Playtime time)
        """
        db_cursor.execute(create_user_data)
        for i in g_list:
            db_cursor.execute(f"""insert into {user} (Game, HighScore, Playtime) Values ("{i}", 0, '00:00:00')""")
            mydb.commit()


def update_data(user, game, score=None, playtime=None):
    if playtime != None:
        db_cursor.execute(f"select playtime from {user} where game = '" + f"{game}" + "'")
        k = db_cursor.fetchall()
        playtime = (k[0][0] + datetime.timedelta(seconds=playtime)).total_seconds()
        hrs = (int(playtime / 3600))
        minutes = int((playtime - (3600 * hrs)) / 60)
        seconds = int(playtime - (60 * minutes) - (3600 * hrs))
        t = str(hrs) + ':' + str(minutes) + ':' + str(seconds)
        db_cursor.execute(f"update {user} set Playtime = '" + f"{t}" + f"' where Game = " + "'" + f"{game}'")
        mydb.commit()
    db_cursor.execute(f"select highscore from {user} where game = '" + f"{game}" + "'")
    if score != None and score > int(db_cursor.fetchall()[0][0]):
        db_cursor.execute(f"select highscore from {user} where game = '" + game + "'")
        if int(db_cursor.fetchall()[0][0]) < score:
            update = f"update {user} set HighScore = {score} where Game = '" + f"{game}" + "'"
            db_cursor.execute(update)
            mydb.commit()


def delete_data(user):
    global mydb, db_cursor
    db_cursor.execute(f'drop table {user}')


def show_data(user):
    db_cursor.execute(f'select * from {user}')
    return db_cursor.fetchall()


x = 0
fade_in = False
fade_out = False
fade_animation = False
begin = pygame.time.get_ticks()
current = 0
a = 0
b = 0
intro = pygame.mixer.Sound('main_data/intro.mp3')
show_loading1 = False
show_loading2 = False
show_loading3 = False
load = 0
menu_1 = False
menu_2 = False
start_game = 0
create_hover = 3
players = {}
f = None
players_ = []
delete_, delete = None, None
confirm_delete = None
create_player = False
yes = 3
error_creating = None
no = 3
user = ''
typing = None
current_player = None
create_user = 3
show_main_exit = False
etd, etm, cancel = 3, 3, 3
show_score = False


def fade_anim():
    global x, begin, current, fade_animation, fade_in, fade_out, show_loading1, x
    logo.set_alpha(x)
    if fade_animation == True:
        begin = pygame.time.get_ticks()
        if x < 500 and fade_in == True:
            x += 1
        else:
            fade_in = False
            fade_out == True
            x -= 1
    if x <= -10 and fade_animation == True:
        fade_animation = False
        fade_out = True
        show_loading1 = True
        x = 0
    f = pygame.font.Font(None, 100).render('Playstation', True, (255, 255, 255))
    screen.blit(logo, ((width / 2) - logo.get_width() / 2, (height / 2) - (logo.get_height() / 2) - 10))
    f.set_alpha(x)
    screen.blit(f, (((width - f.get_width()) / 2) + 10, height - 200))


def check_new_user(user):
    if user in players_:
        return "Save file already exist!"
    elif len(user) < 2:
        return "Enter atleast 2 alphabets."
    else:
        return "Save file created Successfully!"


selected_games = {'Snake Game': [148, (height - 500 - 20) / 2, 3], '2048': [568, (height - 500 - 20) / 2, 3],
                  'Tetris': [988, (height - 500 - 20) / 2, 3], 'Jump Up': [148, 270 + (height - 500 - 20) / 2, 3],
                  'Tron': [568, 270 + (height - 500 - 20) / 2, 3], 'Pong': [988, 270 + (height - 500 - 20) / 2, 3]}
exit_ = 3
view_score = 3
credit = 3
show_credit = False
playing = None

while run:
    current = pygame.time.get_ticks()
    m, n = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    if menu_1 == False and menu_2 == False:
        if current - begin >= 1500 and fade_animation == False and fade_out == False:
            fade_animation = True
            fade_in = True
            intro.play()
        if fade_animation == True:
            fade_anim()
        if show_loading1 == True:
            font = pygame.font.Font(None, 64)
            a = font.render('Preparing Resources', True, (255, 255, 255))
            a.set_alpha(x)
            x += 1
            screen.blit(a, ((width / 2) - a.get_width() / 2, height - 80))
            pygame.draw.rect(screen, (255, 255, 255), (10, height - 20, load, 10))
            a = font.render('Team Members', True, '#ffffff')
            screen.blit(a, (10, 10))
            a = font.render('Samyak Marathe (Group Leader)', True, '#ffffff')
            screen.blit(a, (10, 70))
            a = font.render('Project Given By', True, '#ffffff')
            screen.blit(a, (width - a.get_width() - 10, 10))
            a = pygame.font.Font(None, 40).render('Mr. Ramesh Bhatt (PGT. CS.)', True, '#ffffff')
            screen.blit(a, (width - a.get_width(), 60))
            a = pygame.font.Font(None, 40).render('Dakshesh Bhatnagar', True, '#ffffff')
            screen.blit(a, (10, 130))
            a = pygame.font.Font(None, 40).render('Shagun Bajpai', True, '#ffffff')
            screen.blit(a, (10, 170))
            if load <= width - 20:
                load += 1
            if x >= width + 600:
                show_loading1 = False
                menu_1 = True
                create_database()
                f = open('main_data/saves.txt', 'a+')
                f.seek(0)
                players_ = f.read().split()
                for i in players_:
                    create_table(i)
    if menu_1 == True and menu_2 == False:
        delete = None
        if m >= width - 46 and m <= width - 6 and n >= height - 46 and n <= height - 6:
            create_hover = 1
        else:
            create_hover = 3
        f = open('main_data/saves.txt', 'a+')
        f.seek(0)
        players_ = f.read().split()
        for i in players_:
            players[i] = [2, 2]
        pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 300, 90, 600, 670), 3)
        font = pygame.font.Font(None, 64)
        a = font.render('Select a Profile to Continue', True, '#ffffff')
        screen.blit(a, ((width / 2) - a.get_width() / 2, 25))
        a = font.render('Create', True, '#ffffff')
        screen.blit(a, ((width - a.get_width() - 56, height - 46)))
        pygame.draw.rect(screen, (255, 255, 255), (width - 46, height - 46, 40, 40), create_hover)
        pygame.draw.line(screen, (255, 255, 255), (width - 26, height - 40), (width - 26, height - 12), create_hover)
        pygame.draw.line(screen, (255, 255, 255), (width - 40, height - 26), (width - 12, height - 26), create_hover)
        for i in range(len(players_)):
            a = font.render(players_[i], True, '#ffffff')
            screen.blit(a, ((width / 2) - (a.get_width() / 2) - 25, 130 + (i * 110)))
            if m >= (width / 2) - 290 and m <= (width / 2) + 210 and n >= 100 + (i * 110) and n <= 200 + (
                    i * 110) and create_player == False and delete_ == None:
                players[players_[i]][0] = 1
            else:
                players[players_[i]][0] = 3
            if m >= (width / 2) + 220 and m <= (width / 2) + 290 and n >= 100 + (i * 110) and n <= 200 + (
                    i * 110) and create_player == False and delete_ == None:
                players[players_[i]][1] = 1
            else:
                players[players_[i]][1] = 3
            pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 290, 100 + (i * 110), 500, 100),
                             players[players_[i]][0])
            pygame.draw.rect(screen, (255, 255, 255), ((width / 2) + 220, 100 + (i * 110), 70, 100),
                             players[players_[i]][1])
            pygame.draw.line(screen, (255, 255, 255), ((width / 2) + 236, 130 + (i * 110)),
                             ((width / 2) + 276, 170 + (i * 110)), 3)
            pygame.draw.line(screen, (255, 255, 255), ((width / 2) + 276, 130 + (i * 110)),
                             ((width / 2) + 236, 170 + (i * 110)), 3)
        if create_player == True and yes == 3 and no == 3:
            a = font.render('Enter save file name.', True, '#ffffff')
            pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 350, 110 + ((670 - 300) / 2), 700, 280))
            pygame.draw.rect(screen, (0, 0, 0), ((width / 2) - 350 + 2, 112 + ((670 - 300) / 2), 696, 276))
            screen.blit(a, ((width / 2) - a.get_width() / 2, 310))
            a = font.render('Only Alphabets or _ (No Spaces).', True, '#ffffff')
            screen.blit(a, ((width / 2) - a.get_width() / 2, 360))
            pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 340, 420, 679, 70), 3)
            if m >= (width / 2) - 340 and m <= (width / 2) - 340 + 679 and n >= 420 and n <= 490 and typing != True:
                typing = False
            a = font.render(user, True, '#ffffff')
            screen.blit(a, (width / 2 - 330, 435))
            if typing == True:
                pygame.draw.rect(screen, (255, 255, 255), (width / 2 - 330 + a.get_width() + 5, 430, 5, 50))
                if error_creating != None and error_creating != 'Save file created Successfully!':
                    a = font.render(error_creating, True, '#ffffff')
                    screen.blit(a, (width / 2 - a.get_width() / 2, height - 70))
            a = font.render('Press Enter to Create.', True, '#ffffff')
            screen.blit(a, (width / 2 - a.get_width() / 2, 510))
    if menu_1 == False and menu_2 == True:
        if show_loading2 == True:
            a = font.render(f'Loading Profile: {current_player}', True, (255, 255, 255))
            screen.blit(a, ((width / 2) - a.get_width() / 2, height - 80))
            pygame.draw.rect(screen, (255, 255, 255), (10, height - 20, load, 10))
            load += 1
        if load > width - 20:
            show_loading2 = False
        if show_loading2 == False:
            a = font.render('Chose any of the follwoing Game to Play.', True, '#ffffff')
            screen.blit(a, ((width - a.get_width()) / 2, 10))
            for i in g_list:
                if m >= selected_games[i][0] and m <= selected_games[i][0] + 400 and n >= selected_games[i][1] and n <= \
                        selected_games[i][1] + 250:
                    selected_games[i][2] = 1
                else:
                    selected_games[i][2] = 3
                pygame.draw.rect(screen, (255, 255, 255), (selected_games[i][0], selected_games[i][1], 400, 250),
                                 selected_games[i][2])
                s = font.render(i, True, '#ffffff')
                r, t = s.get_width() / 2, s.get_height() / 2
                screen.blit(s, (selected_games[i][0] + 200 - r, selected_games[i][1] + 125 - t))
            if m >= width - 50 and m <= width - 5 and n >= 5 and n <= 50:
                exit_ = 1
            else:
                exit_ = 3
            pygame.draw.circle(screen, (255, 255, 255), (width - 27, 28), 18, 2)
            pygame.draw.rect(screen, (255, 255, 255), (width - 50, 5, 45, 45), exit_)
            pygame.draw.rect(screen, (0, 0, 0), (width - 32, 7, 10, 10))
            pygame.draw.rect(screen, (255, 255, 255), (width - 28, 8, 2, 20))
            if m >= width - 145 and m <= width - 5 and n >= height - 65 and n <= height - 5:
                credit = 1
            else:
                credit = 3
            a = pygame.font.Font(None, 50).render('Credits', True, '#ffffff')
            screen.blit(a, (width - 136, height - 53))
            pygame.draw.rect(screen, (255, 255, 255), (width - 145, height - 65, 140, 60), credit)
            if m >= width - 145 and m <= width - 5 and n >= height - 140 and n <= height - 80:
                view_score = 1
            else:
                view_score = 3
            a = pygame.font.Font(None, 50).render('Stats', True, '#ffffff')
            screen.blit(a, (width - 118, height - 127))
            pygame.draw.rect(screen, (255, 255, 255), (width - 145, height - 140, 140, 60), view_score)
            if show_main_exit == True:
                screen.fill((0, 0, 0))
                if m >= (width - 330) / 2 and m <= (width + 330) / 2 and n >= 300 and n <= 360:
                    etd = 1
                else:
                    etd = 3
                if m >= (width - 330) / 2 and m <= (width + 330) / 2 and n >= 380 and n <= 440:
                    etm = 1
                else:
                    etm = 3
                if m >= (width - 330) / 2 and m <= (width + 330) / 2 and n >= 460 and n <= 520:
                    cancel = 1
                else:
                    cancel = 3

                pygame.draw.rect(screen, (255, 255, 255), ((width - 330) / 2, 300, 330, 60), etd)
                pygame.draw.rect(screen, (255, 255, 255), ((width - 330) / 2, 380, 330, 60), etm)
                pygame.draw.rect(screen, (255, 255, 255), ((width - 330) / 2, 460, 330, 60), cancel)
                a = pygame.font.Font(None, 54).render('Exit to Desktop', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 312))
                a = pygame.font.Font(None, 54).render('Exit this Profile', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 392))
                a = pygame.font.Font(None, 54).render('Cancel', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 472))
            if show_credit == True:
                a = font.render('Press Escape to go back.', True, '#ffffff')
                screen.fill((0, 0, 0))
                screen.blit(a, ((width - a.get_width()) / 2, 10))
                a = font.render('Creator: Samyak', True, '#ffffff')
                screen.blit(a, (width - a.get_width() - 10, height - a.get_height() - 6))
                a = font.render('Special thanks to: Saubhagya (Creator of tetris)', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 100))
                a = font.render('Help from the followin sources:', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 200))
                a = font.render('flaticon.com, youtube.com, google.com', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, 270))
                a = font.render('Team Members', True, '#ffffff')
                screen.blit(a, (10, height - 120))
                a = font.render('Project Given By:', True, '#ffffff')
                screen.blit(a, (10, height - 240))
                a = pygame.font.Font(None, 40).render('Mr. Ramesh Bhatt (CS. Teacher)', True, '#ffffff')
                screen.blit(a, (16, height - 190))
                a = pygame.font.Font(None, 40).render('Dakshesh Bhatnagar', True, '#ffffff')
                screen.blit(a, (16, height - 70))
                a = pygame.font.Font(None, 40).render('Shagun Bajpai', True, '#ffffff')
                screen.blit(a, (16, height - 30))
                a = pygame.font.Font(None, 100).render('Thank You!', True, '#ffffff')
                screen.blit(a, ((width - a.get_width()) / 2, (height - a.get_height()) / 2))
            if show_score == True:
                a = font.render('Press Escape to go back.', True, '#ffffff')
                screen.fill((0, 0, 0))
                screen.blit(a, ((width - a.get_width()) / 2, 10))
                pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 300, 90, 600, 670), 3)
                pygame.draw.line(screen, (255, 255, 255), ((width / 2) - 300, 160), ((width / 2) + 300, 160), 3)
                pygame.draw.line(screen, (255, 255, 255), ((width / 2) - 100, 90), ((width / 2) - 100, 760), 3)
                pygame.draw.line(screen, (255, 255, 255), ((width / 2) + 130, 90), ((width / 2) + 130, 760), 3)
                a = pygame.font.Font(None, 50).render('Game', True, '#ffffff')
                screen.blit(a, ((width / 2) - 250, 108))
                a = pygame.font.Font(None, 50).render('Score / Wins', True, '#ffffff')
                screen.blit(a, ((width / 2) - 86, 108))
                a = pygame.font.Font(None, 50).render('Playtime', True, '#ffffff')
                screen.blit(a, ((width / 2) + 143, 108))
                a = show_data(current_player)
                l = 100
                for i in range(len(a)):
                    p = pygame.font.Font(None, 40).render(a[i][0], True, '#ffffff')
                    screen.blit(p, ((width / 2) - 300 + ((200 - p.get_width()) / 2), 195 + (i * l)))
                    p = pygame.font.Font(None, 40).render(f'{a[i][1]}', True, '#ffffff')
                    screen.blit(p, ((width / 2) - 100 + ((230 - p.get_width()) / 2), 195 + (i * l)))
                    p = pygame.font.Font(None, 40).render(f'{a[i][2]}', True, '#ffffff')
                    screen.blit(p, ((width / 2) + 130 + ((170 - p.get_width()) / 2), 195 + (i * l)))
    if menu_1 == False and menu_2 == False and playing != None:
        if playing == 'Snake Game':
            a = snake_game.main()
        if playing == '2048':
            a = _2048.main()
        if playing == 'Tetris':
            a = tetris.main()
        if playing == 'Jump Up':
            a = jump_up.main()
        if playing == 'Tron':
            a = tron.main()
        if playing == 'Pong':
            a = pong.main()
        if a != None:
            update_data(current_player, playing, a[0], time.time() - start_game)
            if playing == 'Snake Game':
                importlib.reload(snake_game)
            if playing == '2048':
                importlib.reload(_2048)
            if playing == 'Tetris':
                importlib.reload(tetris)
            if playing == 'Jump Up':
                importlib.reload(jump_up)
            if playing == 'Tron':
                importlib.reload(tron)
            if playing == 'Pong':
                importlib.reload(pong)
            if a[1] == 'whole':
                run = False
            if a[1] == 'menu':
                playing = None
                menu_2 = True

    if playing == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in g_list:
                    if menu_2 == True and selected_games[i][2] == 1 and show_main_exit == False and show_credit == False and show_score == False:
                        playing = i
                        start_game = time.time()
                        menu_2 = False
                if view_score == 1:
                    show_score = True
                if credit == 1:
                    credit = 3
                    show_credit = True
                if etd == 1:
                    run = False
                if etm == 1:
                    menu_2 = False
                    show_loading2 = False
                    menu_1 = True
                    show_main_exit = False
                    etm = 3
                    current_player = None
                    load = 0
                    players = {}
                    for i in players_:
                        players[i] = [2, 2]
                if cancel == 1:
                    cancel = 3
                    show_main_exit = False
                    print(menu_2, menu_1, playing)
                if typing == False:
                    typing = True
                if typing == True:
                    if not (m >= (width / 2) - 340 and m <= (width / 2) - 340 + 679 and n >= 420 and n <= 490):
                        typing = None
                if yes == 1 and create_hover == 3:
                    yes = 3
                    confirm_delete = True
                    delete = delete_
                if no == 1 and create_hover == 3:
                    no = 3
                    confirm_delete = None
                    delete, delete_ = None, None
                if create_hover == 1 and len(players_) < 6:
                    create_player = True
                if exit_ == 1 and menu_2 == True:
                    show_main_exit = True
                if menu_1:
                    for i in range(len(players_)):
                        if players[players_[i]][1] == 1:
                            delete_ = players_[i]
                            confirm_delete = False
                        if players[players_[i]][0] == 1:
                            current_player = players_[i]
                            menu_1 = False
                            show_loading2 = True
                            load = 0
                            menu_2 = True

            if event.type == pygame.KEYDOWN:
                if typing == True:
                    b = event.unicode
                    if b.isalpha() or b == '_':
                        user += b
                        error_creating = None
                if event.key == pygame.K_0:
                    run = False
                if event.key == pygame.K_RETURN:
                    if typing == True:
                        error_creating = check_new_user(user)
                        if error_creating == "Save file already exist!":
                            typing = True
                            user = ''
                        if error_creating == "Enter atleast 2 alphabets.":
                            typing = True
                            user = ''
                        if error_creating == "Save file created Successfully!":
                            f.close()
                            f = open('main_data/saves.txt', 'w')
                            for i in players_:
                                f.write(i + ' ')
                            f.write(user)
                            typing = None
                            create_user = 3
                            create_table(user)
                            user = ''
                            create_player = False
                if event.key == pygame.K_ESCAPE:
                    if menu_2 == True and show_score == False and playing == None and show_credit == False:
                        if show_main_exit == False:
                            show_main_exit = True
                        else:
                            show_main_exit = False
                    show_credit = False
                    show_score = False
                    if confirm_delete == False:
                        confirm_delete = None
                    if create_player == True:
                        create_hover = 3
                        user = ''
                        create_player = False
                        error_creating = None
                        typing = None
                if event.key == pygame.K_BACKSPACE:
                    t = user
                    user = ''
                    for i in range(len(t) - 1):
                        user += t[i]
    if confirm_delete == False:
        pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 350, 90 + ((670 - 300) / 2), 700, 300))
        pygame.draw.rect(screen, (0, 0, 0), ((width / 2) - 350 + 2, 92 + ((670 - 300) / 2), 696, 296))
        a1 = font.render(f'Do you want to delete the save', True, '#ffffff')
        screen.blit(a1, ((width / 2) - a1.get_width() / 2, 300))
        a2 = font.render(f'file named {delete_}.', True, '#ffffff')
        screen.blit(a2, ((width / 2) - a2.get_width() / 2, 360))
        a3 = font.render(f'All the progress will be lost.', True, '#ffffff')
        screen.blit(a3, ((width / 2) - a3.get_width() / 2, 420))
        if m >= 428 and m <= 428 + 336 and n >= 490 and n <= 564:
            yes = 1
        else:
            yes = 3
        if m >= (width / 2) + 3 and m <= (width / 2) + 339 and n >= 490 and n <= 564:
            no = 1
        else:
            no = 3
        pygame.draw.rect(screen, (255, 255, 255), ((width / 2) - 340, 490, 336, 74), yes)
        a = font.render('Yes', True, '#ffffff')
        screen.blit(a, (555, 505))
        a = font.render('No', True, '#ffffff')
        screen.blit(a, (918, 505))
        pygame.draw.rect(screen, (255, 255, 255), ((width / 2) + 3, 490, 336, 74), no)
    if delete != None and menu_1 == True and confirm_delete == True:
        f.close()
        f = open('main_data/saves.txt', 'w')
        for i in players_:
            if i != delete:
                f.write(i + ' ')
        delete_data(delete)
        delete, delete_ = None, None
    if f != None:
        f.close()
    pygame.display.update()
pygame.quit()
mydb.close()
