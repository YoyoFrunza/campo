# tamanho de cada tile
TILE_SIZE = 32

# número de linhas e colunas do tabuleiro
ROWS = 16
COLS = 16
MINES = 40

# tamanho da janela
WIDTH = COLS * TILE_SIZE + 40
HEIGHT = ROWS * TILE_SIZE + 120

# cores
BG_COLOR = (192, 192, 192)

# caminho das sprites
SPRITES_PATH = "assets/Sprites/"

# escala do player (usado para animar PNGs maiores que o tile)
PLAYER_SCALE = 1.4

# dificuldade: (linhas, colunas, minas)
DIFFICULTY = {
    "Easy": (9, 9, 10),
    "Normal": (16, 16, 40),
    "Hard": (16, 30, 99)
}
