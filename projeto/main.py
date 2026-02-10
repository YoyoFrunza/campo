import pygame
from constants import *
from board import Board
from player import Player
from utils import load_tile, load_number
from menu import Menu
from hud import HUD

pygame.init()

# ===============================
# MENU DE ESCOLHA DE DIFICULDADE
# ===============================
menu = Menu()
difficulty = None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

while difficulty is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        d = menu.handle(event)
        if d:
            difficulty = d
    screen.fill((0,0,0))
    menu.draw(screen)
    pygame.display.flip()

# ===============================
# CONFIGURAÇÃO DO JOGO
# ===============================
board = Board(difficulty)
board.level = difficulty  # guardar nível para reset
screen_width = board.cols*TILE_SIZE + 40
screen_height = board.rows*TILE_SIZE + 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

player = Player(0,0)
hud = HUD(board, player)

tiles = {
    "unknown": load_tile("TileUnknown.png", crop=False),
    "empty": load_tile("TileEmpty.png"),
    "mine": load_tile("TileMine.png"),
    "exploded": load_tile("TileExploded.png"),
    "flag": load_tile("TileFlag.png"),
}
numbers = {i: load_number(f"Tile{i}.png") for i in range(1,9)}

offset_x = 20
offset_y = 80

# ===============================
# LOOP PRINCIPAL
# ===============================
running = True
clicking_face = False

def reset_game():
    """Função para reiniciar o jogo mantendo o nível atual."""
    global board, player, hud
    board = Board(board.level)
    board.level = difficulty
    player = Player(0,0)
    hud = HUD(board, player)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===============================
        # CONTROLES DO PLAYER
        # ===============================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: player.move(-1,0,board)
            if event.key == pygame.K_s: player.move(1,0,board)
            if event.key == pygame.K_a: player.move(0,-1,board)
            if event.key == pygame.K_d: player.move(0,1,board)
            if event.key == pygame.K_UP: player.place_flag(-1,0,board)
            if event.key == pygame.K_DOWN: player.place_flag(1,0,board)
            if event.key == pygame.K_LEFT: player.place_flag(0,-1,board)
            if event.key == pygame.K_RIGHT: player.place_flag(0,1,board)

            # ===============================
            # RESET COM TECLA 'R'
            # ===============================
            if event.key == pygame.K_r:
                reset_game()

        # ===============================
        # CLIQUE NA FACE (RESET)
        # ===============================
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hud.smile_rect.collidepoint(event.pos):
                clicking_face = True
                hud.set_clicking(True)

        if event.type == pygame.MOUSEBUTTONUP:
            if clicking_face:
                if hud.smile_rect.collidepoint(event.pos):
                    reset_game()
                clicking_face = False
                hud.set_clicking(False)

    # ===============================
    # ATUALIZAÇÕES
    # ===============================
    player.update_animation()
    hud.update()

    # ===============================
    # DESENHO
    # ===============================
    screen.fill(BG_COLOR)

    # Desenha tabuleiro
    for r in range(board.rows):
        for c in range(board.cols):
            tile = board.grid[r][c]
            x = offset_x + c*TILE_SIZE
            y = offset_y + r*TILE_SIZE
            if not tile.revealed:
                screen.blit(tiles["unknown"], (x,y))
                if tile.flagged:
                    screen.blit(tiles["flag"], (x,y))
            else:
                if tile.exploded:
                    screen.blit(tiles["exploded"], (x,y))
                elif tile.mine:
                    screen.blit(tiles["mine"], (x,y))
                elif tile.adjacent==0:
                    screen.blit(tiles["empty"], (x,y))
                else:
                    screen.blit(numbers[tile.adjacent], (x,y))

    # Player e HUD
    player.draw(screen, offset_x, offset_y)
    hud.draw(screen)

    pygame.display.flip()

pygame.quit()
