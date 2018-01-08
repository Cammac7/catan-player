# ui_main contains the main function for the Catan Player.

import math
import os
import pygame
from pygame.locals import *

DATA_DIR = 'data'

def get_error():
    return SystemExit(str(pygame.compat.geterror()))

# colorkey is the color to use for transparency.
def load_image(name, colorkey=None):
    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise get_error()
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(DATA_DIR, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound: %s' % fullname)
        raise get_error()
    return sound

def draw_ngon(surface, color, n, radius, position):
    points = []
    for i in range(0, n):
        points.append((math.sin(i / n * 2 * math.pi) * radius + position[0],
                       math.cos(i / n * 2 * math.pi) * radius + position[1]))
    return pygame.draw.polygon(surface, color, points)

def draw_aa_ngon(surface, color, n, radius, position):
    points = []
    for i in range(0, n):
        points.append((math.sin(i / n * 2 * math.pi) * radius + position[0],
                       math.cos(i / n * 2 * math.pi) * radius + position[1]))
    return pygame.draw.aalines(surface, color, True, points, False)

class HexTile(pygame.sprite.Sprite):
    """HexTile represents one of the hexagonal tiles that form the board."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('test_hex.png')

    def update(self):
        pass


def main():
    if not pygame.font: print('Warning, fonts disabled')
    if not pygame.mixer: print('Warning, sound disabled')
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Settlers of Catan')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((135, 206, 250)) # "light sky blue"

    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    hex_tile = HexTile()
    all_sprites = pygame.sprite.RenderPlain(hex_tile)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                pass # TODO
            elif event.type == MOUSEBUTTONUP:
                pass # TODO

        all_sprites.update()

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        draw_ngon(screen, (255, 255, 255), 6, 32, (128, 128))
        draw_aa_ngon(screen, (255, 255, 255), 6, 32, (256, 128))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
