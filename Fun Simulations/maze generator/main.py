import pygame
import random

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
grid, status, neighbours, stack, size, current = [], [], [], [], 20, 0
game_state = 1
rows, cols = (height / size) - 1, (width / size) - 1
start, done = 0, 0


def get_next(c):
    global current, neighbours
    for i in range(len(grid)):
        if grid[c][0] > 0 and grid[c][0] - grid[i][0] == 1 and grid[c][1] == grid[i][1] and grid[i][6] == 0:
            neighbours.append([i, "top"])
        if grid[c][1] <= cols and grid[i][1] - grid[c][1] == 1 and grid[c][0] == grid[i][0] and grid[i][6] == 0:
            neighbours.append([i, "right"])
        if grid[c][0] <= rows and grid[i][0] - grid[c][0] == 1 and grid[c][1] == grid[i][1] and grid[i][6] == 0:
            neighbours.append([i, "bottom"])
        if grid[c][1] > 0 and grid[c][1] - grid[i][1] == 1 and grid[c][0] == grid[i][0] and grid[i][6] == 0:
            neighbours.append([i, "left"])
    if len(neighbours) > 1:
        a = random.randint(0, (len(neighbours) - 1))
        if neighbours[a][1] == "top":
            grid[current][2] = 0
            grid[neighbours[a][0]][4] = 0
            current = neighbours[a][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[a][1] == "right":
            grid[current][3] = 0
            grid[neighbours[a][0]][5] = 0
            current = neighbours[a][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[a][1] == "bottom":
            grid[current][4] = 0
            grid[neighbours[a][0]][2] = 0
            current = neighbours[a][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[a][1] == "left":
            grid[current][5] = 0
            grid[neighbours[a][0]][3] = 0
            current = neighbours[a][0]
            neighbours.clear()
            stack.append(current)
            return 1
    if len(neighbours) == 1:
        if neighbours[0][1] == "top":
            grid[current][2] = 0
            grid[neighbours[0][0]][4] = 0
            current = neighbours[0][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[0][1] == "right":
            grid[current][3] = 0
            grid[neighbours[0][0]][5] = 0
            current = neighbours[0][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[0][1] == "bottom":
            grid[current][4] = 0
            grid[neighbours[0][0]][2] = 0
            current = neighbours[0][0]
            neighbours.clear()
            stack.append(current)
            return 1
        if neighbours[0][1] == "left":
            grid[current][5] = 0
            grid[neighbours[0][0]][3] = 0
            current = neighbours[0][0]
            neighbours.clear()
            stack.append(current)
            return 1
    if len(neighbours) == 0 and len(stack) > 0:
        current = stack.pop()


def make_cell(a, b):
    status = [1, 1, 1, 1, 0]
    status.insert(0, b)
    status.insert(1, a)
    return status


class cell:
    def __init__(self):
        rows = int(width / size)
        cols = int(height / size)
        for i in range(0, rows):
            for j in range(0, cols):
                cel = make_cell(j, i)
                grid.append(cel)


box = cell()
grid[current][6] = 0
while game_state:
    if start:
        get_next(current)
    if done == 1:
        current = 0
        neighbours.clear()
        stack.clear()
    grid[current][6] = 1
    screen.fill((210, 210, 210))
    pygame.draw.rect(screen, (200, 210, 20),
                     (grid[current][1] * size + 2, grid[current][0] * size + 2, size - 2, size - 2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = 1
    # pygame.time.Clock().tick(10)
    if len(neighbours) > 1:
        neighbours.clear()
    for i in range(len(grid)):
        if grid[i][2] == 1:
            pygame.draw.line(screen, (0, 0, 0), (grid[i][1] * size, grid[i][0] * size),
                             (((grid[i][1] * size) + size), grid[i][0] * size), 2)
        if grid[i][3] == 1:
            pygame.draw.line(screen, (0, 0, 0), (((grid[i][1] * size) + size), grid[i][0] * size),
                             (((grid[i][1] * size) + size), ((grid[i][0] * size) + size)), 2)
        if grid[i][4] == 1:
            pygame.draw.line(screen, (0, 0, 0), (((grid[i][1] * size) + size), ((grid[i][0] * size) + size)),
                             (grid[i][1] * size, ((grid[i][0] * size) + size)), 2)
        if grid[i][5] == 1:
            pygame.draw.line(screen, (0, 0, 0), (grid[i][1] * size, ((grid[i][0] * size) + size)),
                             (grid[i][1] * size, grid[i][0] * size), 2)
        if grid[i][2] == 0:
            pygame.draw.line(screen, (150, 0, 200), (grid[i][1] * size, grid[i][0] * size),
                             (((grid[i][1] * size) + size), grid[i][0] * size), 2)
        if grid[i][3] == 0:
            pygame.draw.line(screen, (150, 0, 200), (((grid[i][1] * size) + size), grid[i][0] * size),
                             (((grid[i][1] * size) + size), ((grid[i][0] * size) + size)), 2)
        if grid[i][4] == 0:
            pygame.draw.line(screen, (150, 0, 200), (((grid[i][1] * size) + size), ((grid[i][0] * size) + size)),
                             (grid[i][1] * size, ((grid[i][0] * size) + size)), 2)
        if grid[i][5] == 0:
            pygame.draw.line(screen, (150, 0, 200), (grid[i][1] * size, ((grid[i][0] * size) + size)),
                             (grid[i][1] * size, grid[i][0] * size), 2)
        if i != current and grid[i][6] == 1:
            pygame.draw.rect(screen, (150, 0, 200), (grid[i][1] * size + 2, grid[i][0] * size + 2, size - 2, size - 2))
    for i in range(len(grid)):
        if grid[i][6] == 1:
            done = 1
        else:
            done = 0
            break
    pygame.draw.line(screen, (0, 0, 0), (0, height - 2), (width, height - 2), 2)
    pygame.draw.line(screen, (0, 0, 0), (width - 2, 0), (width - 2, height), 2)
    pygame.display.update()
