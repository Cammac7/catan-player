# gui_main contains the main function for the Catan Player's GUI.
# To run gui_main, first install pipenv. See http://docs.python-guide.org/en/latest/dev/virtualenvs/
# Then install pygame via the following command: "pipenv install pygame"
# Then you can run gui_main with the following command: "pipenv run python gui_main.py"

import math
import os
import pygame
from enum import Enum
from pygame.locals import *

DATA_DIR = 'data'
HEX_RADIUS = 32
BOARD = [
    [0, 0, 3, 0, 6, 0, 2, 0, 0],
    [0, 4, 0, 5, 0, 4, 0, 6, 0],
    [1, 0, 3, 0, 2, 0, 3, 0, 2],
    [0, 4, 0, 6, 0, 6, 0, 5, 0],
    [0, 0, 5, 0, 2, 0, 3, 0, 0],
]

class Terrain(Enum):
    NONE = 0
    DESERT = 1
    FIELDS = 2
    FOREST = 3
    HILLS = 4
    MOUNTAINS = 5
    PASTURE = 6

IMAGE_NAME = {
    Terrain.DESERT: 'desert.png',
    Terrain.FIELDS: 'fields.png',
    Terrain.FOREST: 'forest.png',
    Terrain.HILLS: 'hills.png',
    Terrain.MOUNTAINS: 'mountains.png',
    Terrain.PASTURE: 'pasture.png',
}

def get_error():
    return SystemExit(str(pygame.compat.geterror()))

def get_image_name(terrain):
    return IMAGE_NAME.get(terrain, 'test_hex.png')

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


class HexTile(pygame.sprite.Sprite):
    """HexTile represents one of the hexagonal tiles that form the board."""
    def __init__(self, terrain, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(get_image_name(terrain))
        self.rect.topleft = x, y

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

    # TODO: Center the board on the screen.
    #center_x, center_y = screen.get_rect().center
    #board_height = len(BOARD) * HEX_RADIUS
    #board_width = len(BOARD[0]) * HEX_RADIUS * 3 / 2
    #start_x = center_x - (board_width / 2)
    #start_y = center_y - (board_height / 2)
    start_x = 0
    start_y = 0
    sprites = []
    for i in range(len(BOARD)):
        for j in range(len(BOARD[i])):
            terrain = Terrain(BOARD[i][j])
            if terrain != Terrain.NONE:
                # Multiple the height by 3/2 so that the hex tiles are touching.
                sprites.append(HexTile(
                        terrain,
                        start_x + j * HEX_RADIUS,
                        start_y + i * HEX_RADIUS * 3 / 2))
    all_sprites = pygame.sprite.Group(sprites)

    clock = pygame.time.Clock()
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
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
