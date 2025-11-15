import pygame
import numpy as np

pygame.init()
width, height = 0, 0
screen = pygame.display.set_mode((width, height))
width, height = screen.get_size()
fps = pygame.time.Clock()
run = True
colors = {"white": (255, 255, 255), "orange": (255, 127, 39), "green": (150, 253, 55), "blue": (74, 112, 169),
          "grey": (120, 120, 120), "black": (0, 0, 0), "red": (255, 0, 0)}


class DROPS:
    def __init__(self, n_drops):
        self.n_drops = n_drops
        self.pos = np.hstack((np.random.randint(0, width, (self.n_drops, 1)),
                              np.random.randint(-height, -50, (self.n_drops, 1)),
                              np.round(np.random.uniform(0, 10, (self.n_drops, 1)), 2)))
        self.drop_vfx = np.vstack(np.round((np.linspace(15, 40, self.n_drops),
                                            np.linspace(1, 6, self.n_drops),
                                            np.linspace(18, 50, self.n_drops)), 2))
        self.drop_vfx = self.drop_vfx.T

    def rainfall(self, p):
        for i in range(self.n_drops):
            if i >= len(self.pos):
                break

            k = np.argmin(np.abs(self.pos[:, 2][i] - self.pos[:, 2]))

            if k >= len(self.drop_vfx):
                k = len(self.drop_vfx) - 1

            if self.pos[:, 1][i] > height:
                self.pos[:, 0][i] = np.random.randint(0, width)
                self.pos[:, 1][i] = np.random.randint(-height, 20)
                self.pos[:, 2][i] = np.round(np.random.uniform(0, 10), 2)

            else:
                if p:
                    self.pos[:, 1][i] += self.drop_vfx[:, 0][k]
                if dark_mode:
                    pygame.draw.rect(screen, colors['grey'], (self.pos[:, 0][i], self.pos[:, 1][i],
                                                              self.drop_vfx[:, 1][k], self.drop_vfx[:, 2][k]))
                else:
                    pygame.draw.rect(screen, colors['blue'], (self.pos[:, 0][i], self.pos[:, 1][i],
                                                               self.drop_vfx[:, 1][k], self.drop_vfx[:, 2][k]))

    def intensity(self, n):
        if n > 0:
            self.pos = np.vstack((self.pos, np.hstack((np.random.randint(0, width, (n, 1)),
                                                       np.random.randint(-height, -50, (n, 1)),
                                                       np.round(np.random.uniform(0, 10, (n, 1)), 2)))))
            self.drop_vfx = np.vstack((self.drop_vfx, np.vstack(np.round((np.linspace(15, 40, n),
                                                                          np.linspace(1, 6, n),
                                                                          np.linspace(18, 50, n)), 2)).T))
        else:
            self.pos = self.pos[10:]
            self.drop_vfx = self.drop_vfx[10:]


def sound_effects(intensity_volume):
    global thunder, thunder_sound

    rain_channel.set_volume(intensity_volume)

    if thunder == 0:
        trigger = np.random.randint(1, 100)
        if 60 <= trigger <= 66:
            thunder = 1
            thunder_sound = sounds[1].play(0)
            thunder_sound.set_volume(intensity_volume)
        elif 87 <= trigger <= 90 and intensity_volume >= 0.4:
            thunder = 2
            thunder_sound = sounds[2].play(0)
            thunder_sound.set_volume(intensity_volume)
        elif 20 <= trigger <= 26 and intensity_volume >= 0.4:
            thunder = 3
            thunder_sound = sounds[3].play(0)
            thunder_sound.set_volume(min(intensity_volume, 0.6))
        elif trigger == 69 and intensity_volume >= 0.4:
            trigger = np.random.randint(1, 100)
            if 6 <= trigger <= 10:
                thunder = 4
                thunder_sound = sounds[4].play(0)
                thunder_sound.set_volume(min(intensity_volume, 0.6))
    else:
        if thunder_sound and not thunder_sound.get_busy():
            thunder = 0
            thunder_sound = None


number = 100
rain_drops = DROPS(number)

play = False
sounds = [pygame.mixer.Sound('data/rain_sound.mp3'),
          pygame.mixer.Sound('data/thunder0.mp3'),
          pygame.mixer.Sound('data/thunder1.mp3'),
          pygame.mixer.Sound('data/thunder2.mp3'),
          pygame.mixer.Sound('data/thunder3.mp3')]

rain_channel = sounds[0].play(-1)
rain_channel.set_volume(0.00)
rain_channel.pause()

thunder = 0
thunder_sound = None
dark_mode = False

while run:
    if dark_mode:
        screen.fill((0, 0, 0))
    else:
        screen.fill((200, 230, 255))
    rain_drops.rainfall(play)

    if play:
        intensity_volume = (8 * rain_drops.n_drops / 9000) + (1 / 9)
        intensity_volume = max(0.2, min(1.0, intensity_volume))

        sound_effects(intensity_volume)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                run = False
            if event.key == pygame.K_SPACE:
                if play:
                    play = False
                    rain_channel.pause()
                    if thunder_sound:
                        thunder_sound.pause()
                else:
                    play = True
                    rain_channel.unpause()
                    if thunder_sound:
                        thunder_sound.unpause()
            if event.key == pygame.K_UP:
                if rain_drops.n_drops < 1000:
                    rain_drops.n_drops += 10
                    rain_drops.intensity(10)
            if event.key == pygame.K_DOWN:
                if rain_drops.n_drops > 100:
                    rain_drops.n_drops -= 10
                    rain_drops.intensity(-10)
            if event.key == pygame.K_RETURN:
                if dark_mode:
                    dark_mode = False
                else:
                    dark_mode = True

    fps.tick(60)
    pygame.display.update()
pygame.quit()
