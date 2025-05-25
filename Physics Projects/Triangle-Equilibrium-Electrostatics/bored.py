import pygame
import numpy as np
import matplotlib.pyplot as plt

pygame.init()
screen = pygame.display.set_mode((600, 600))
width, height = pygame.display.get_surface().get_size()
run = 1
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}

q = 1.6e-19
Q = q
a = 400
epsilon = 8.854e-12
charge = 1.6e-19
mass = 9.1e-31
k = 1 / (4 * np.pi * epsilon)
pos = np.array([[(width - a) / 2, height / 2 + (a / (2 * np.sqrt(3)))],
                [width / 2, height / 2 - (a / np.sqrt(3))],
                [(width + a) / 2, height / 2 + (a / (2 * np.sqrt(3)))]])

test = np.array([width / 2, height / 2])
m = (test - pos[0])[1] / (test - pos[0])[0]
velocity = np.array([0., 0.])
move = .005
move_left, move_right = False, False
dt = 0
start = False

accel, vel, disp, T, ke, pe, ke_x, pe_x = [], [], [], [], [], [], [], []


def calc_force(q1, q2, r):
    r = test - r
    t = np.arctan2(r[1], r[0])
    E = k * q1 / np.sum(r ** 2)
    F = E * q2
    return np.array([np.cos(t) * F, np.sin(t) * F])


def draw_charges():
    pygame.draw.line(screen, colors['black'], pos[0], pos[1], 2)
    pygame.draw.line(screen, colors['black'], pos[0], pos[2], 2)
    pygame.draw.line(screen, colors['black'], pos[1], pos[2], 2)
    pygame.draw.circle(screen, colors['orange'], pos[0], 6)
    pygame.draw.circle(screen, colors['orange'], pos[1], 6)
    pygame.draw.circle(screen, colors['orange'], pos[2], 6)
    pygame.draw.circle(screen, colors['blue'], test, 6)


def dynamics(v):
    global test
    a = np.round((calc_force(q, Q, pos[0]) + calc_force(q, Q, pos[1]) + calc_force(q, Q, pos[2])) / mass, 6)
    if a[0] <= 0:
        accel.append(-np.sqrt(np.sum(a ** 2)))
    else:
        accel.append(np.sqrt(np.sum(a ** 2)))

    inst_v = np.round(v + a * dt, 6)
    if inst_v[0] <= 0:
        vel.append(-np.sqrt(np.sum(inst_v ** 2)))
    else:
        vel.append(np.sqrt(np.sum(inst_v ** 2)))

    test += (inst_v * dt) + (a * (dt ** 2))
    test = np.round(test, 6)
    s = test - np.array([width / 2, height / 2])
    T.append(dt)
    if s[0] <= 0:
        disp.append(-np.sqrt(np.sum(s ** 2)))
    else:
        disp.append(np.sqrt(np.sum(s ** 2)))
    pe_ = ((k * q * Q / np.sqrt(np.sum((test - pos[0]) ** 2))) +
           (k * q * Q / np.sqrt(np.sum((test - pos[1]) ** 2))) +
           (k * q * Q / np.sqrt(np.sum((test - pos[2]) ** 2))))
    ke_ = 0.5 * mass * vel[-1] ** 2
    ke.append(ke_)
    pe.append(pe_)
    return inst_v


while run:
    screen.fill((180, 180, 180))
    draw_charges()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                if start:
                    start = False
                else:
                    start = True
                    dt = 0.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
    if move_left:
        test = test - np.array([move * np.cos(np.arctan(m)), move * np.sin(np.arctan(m))])
    if move_right:
        test = test + np.array([move * np.cos(np.arctan(m)), move * np.sin(np.arctan(m))])

    if start:
        velocity = dynamics(velocity)
        dt += .0001
    pygame.display.update()
pygame.quit()

plt.grid(True)
plt.plot(T, disp, color='red')
plt.title('Displacement v/s Time')
plt.show()

plt.grid(True)
plt.plot(T, vel, color='red')
plt.title('Velocity v/s Time')
plt.show()

plt.grid(True)
plt.plot(T, accel, color='red')
plt.title('Acceleration v/s Time')
plt.show()

plt.grid(True)
plt.plot(T, ke, color='red')
plt.title('Kinetic Energy v/s Time')
plt.show()

plt.grid(True)
plt.plot(T, pe, color='red')
plt.title('Potential Energy v/s Time')
plt.show()

plt.grid(True)
plt.plot(T, np.array(pe) + np.array(ke), color='red')
plt.title('Total Energy v/s Time')
plt.show()
