import pygame
import numpy as np
import graphics

pygame.init()
screen = pygame.display.set_mode((700, 520), pygame.DOUBLEBUF | pygame.OPENGL)
width, height = pygame.display.get_surface().get_size()
fps = pygame.time.Clock()
run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (0, 162, 132),
          "grey": (64, 64, 64), "black": (0, 0, 0), "red": (255, 0, 0)}

graphics.initialize(width, height, 6)


def mag(v):
    return ((v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2])) ** 0.5


def calculate_pi(shape):
    pi = number_of_points * 3 * shape.volume / (4 * points.points_inside_mesh * (shape.radius_outer_circle ** 3))
    print('Value of Pi:', pi)
    print(points.points_inside_mesh)


number_of_points = 4000
cube = graphics.Cube()
tetrahedron = graphics.Tetrahedron()
octahedron = graphics.Octahedron()
icosahedron = graphics.Icosahedron()
dodecahedron = graphics.Dodecahedron()
shape = cube
find_pi = False
points = graphics.Points(number_of_points, shape, np.array([0., 0., 0.]))
total_points, value_of_pi = [], []
rx, ry, rz, zoom = 0, 0, 0, 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_RETURN:
                find_pi = True
            if event.key == pygame.K_SPACE:
                if not zoom:
                    zoom = .1
                else:
                    zoom = 0.
            if event.key == pygame.K_x:
                if not rx:
                    rx = .1
                else:
                    rx = 0.
            if event.key == pygame.K_y:
                if not ry:
                    ry = .1
                else:
                    ry = 0.
            if event.key == pygame.K_z:
                if not rz:
                    rz = .1
                else:
                    rz = 0.

    if find_pi:
        if len(points.points) == number_of_points:
            calculate_pi(shape)
            find_pi = False
    graphics.make_display()
    points.draw()
    shape.draw()
    graphics.rotate(zoom, rx, ry, rz)
    pygame.display.flip()
    fps.tick(60)
pygame.quit()
"""
pl.grid(True)
pl.plot(total_points, value_of_pi, 'o')
pl.xlim([10000, number_of_points])
pl.plot([i for i in range(number_of_points)], [sum(value_of_pi) / len(value_of_pi) for i in range(number_of_points)],
        color='r')
pl.plot([i for i in range(number_of_points)], [numpy.pi for i in range(number_of_points)],
        color='k')
pl.legend(['Simulated values', 'Average value', 'Actual Value'])
pl.show()
print('Average =', sum(value_of_pi) / len(value_of_pi))
"""
