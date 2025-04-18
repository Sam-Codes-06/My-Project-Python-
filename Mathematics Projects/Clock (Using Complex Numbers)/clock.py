import pygame, time, math

pygame.init()
screen = pygame.display.set_mode((0, 0))
width, height = pygame.display.get_surface().get_size()

run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}

t = int(time.time() + 19800)


def transform(x, y):
    return (width / 2) - x, (height / 2) - y


def clock(sam):
    sa, ma, ha = (sam[0] * 6 * math.pi / 180) + math.pi / 2, (sam[1] * math.pi / 30) + math.pi / 2, \
                 (sam[2] * math.pi / 6) + math.pi / 2
    sh, mh, hh = complex(0, 0), complex(0, 0), complex(0, 0)
    for i in range(100):
        sh += ((sa * complex(0, 1)) ** i) / math.factorial(i)
        mh += ((ma * complex(0, 1)) ** i) / math.factorial(i)
        hh += ((ha * complex(0, 1)) ** i) / math.factorial(i)
    return (sh, mh, hh)


sam = [round(t % 60, 3), round((t / 60) % 60, 3), round((t / 3600) % 12, 3)]

fade = {'red': [255, 0, 0], 'orange': [255, 127, 0], 'yellow': [255, 255, 0], 'green': [0, 255, 0], 'blue': [0, 0, 255],
        'indigo': [75, 0, 130], 'violet': [148, 0, 211]}
current_status = 'red'
current_color = [255, 0, 0]
c_timer = [time.time(), time.time()]
while run:
    m1, n1 = pygame.mouse.get_rel()
    m2, n2 = pygame.mouse.get_rel()
    if (m1, n1) != (m2, n2):
        run = False
    screen.fill((0, 0, 0))
    if c_timer[1] - c_timer[0] >= 60 / 1226:
        c_timer[0] = time.time()
        if current_status == 'red':
            if current_color[1] < 127:
                current_color[1] += 1
            if current_color[1] == 127:
                current_status = 'orange'
        if current_status == 'orange':
            if current_color[1] < 255:
                current_color[1] += 1
            if current_color[1] == 255:
                current_status = 'yellow'
        if current_status == 'yellow':
            if current_color[0] > 0:
                current_color[0] -= 1
            if current_color[0] == 0:
                current_status = 'green'
        if current_status == 'green':
            if current_color[1] > 0:
                current_color[1] -= 1
            if current_color[2] < 255:
                current_color[2] += 1
            if current_color[1] == 0 and current_color[2] == 255:
                current_status = 'blue'
        if current_status == 'blue':
            if current_color[0] < 75:
                current_color[0] += 1
            if current_color[2] > 130:
                current_color[2] -= 1
            if current_color[0] == 75 and current_color[2] == 130:
                current_status = 'indigo'
        if current_status == 'indigo':
            if current_color[0] < 148:
                current_color[0] += 1
            if current_color[2] < 211:
                current_color[2] += 1
            if current_color[0] == 148 and current_color[2] == 211:
                current_status = 'violet'
        if current_status == 'violet':
            if current_color[0] < 255:
                current_color[0] += 1
            if current_color[2] > 0:
                current_color[2] -= 1
            if current_color[0] == 255 and current_color[2] == 0:
                current_status = 'red'
    t = int(time.time() + 19800)
    sam = [t % 60, (t / 60) % 60, (t / 3600) % 12]
    x, y = transform(0, 0)
    hc = clock(sam)
    pygame.draw.circle(screen, current_color, (x, y), 250, 3)
    x1, y1 = transform(round(-10 * hc[0].real, 6), round(-10 * hc[0].imag, 6))
    x2, y2 = transform(round(200 * hc[0].real, 6), round(200 * hc[0].imag, 6))
    pygame.draw.line(screen, colors['white'], (x1, y1), (x2, y2), 1)
    x1, y1 = transform(round(-10 * hc[1].real, 6), round(-10 * hc[1].imag, 6))
    x2, y2 = transform(round(150 * hc[1].real, 6), round(150 * hc[1].imag, 6))
    pygame.draw.line(screen, colors['white'], (x1, y1), (x2, y2), 2)
    x1, y1 = transform(round(-10 * hc[2].real, 6), round(-10 * hc[2].imag, 6))
    x2, y2 = transform(round(80 * hc[2].real, 6), round(80 * hc[2].imag, 6))
    pygame.draw.line(screen, colors['white'], (x1, y1), (x2, y2), 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
    c_timer[1] = time.time()
    pygame.display.update()
pygame.quit()
