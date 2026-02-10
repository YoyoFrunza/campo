import pygame
from constants import TILE_SIZE, SPRITES_PATH, PLAYER_SCALE

def load_tile(name, crop=True):
    img = pygame.image.load(f"{SPRITES_PATH}{name}").convert_alpha()
    if crop:
        w, h = img.get_size()
        img = img.subsurface(2, 2, w-4, h-4)
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

def load_number(name):
    img = pygame.image.load(f"{SPRITES_PATH}{name}").convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

def load_player(name):
    img = pygame.image.load(f"{SPRITES_PATH}{name}").convert_alpha()
    size = int(TILE_SIZE * PLAYER_SCALE)
    return pygame.transform.scale(img, (size, size))

def load_face(name):
    img = pygame.image.load(f"{SPRITES_PATH}faces/{name}.png").convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

def load_digit(name):
    img = pygame.image.load(f"{SPRITES_PATH}digits/{name}.png").convert_alpha()
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
