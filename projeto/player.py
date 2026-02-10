import pygame
from constants import TILE_SIZE, SPRITES_PATH

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.alive = True

        # Estado atual
        self.state = "idle"
        self.direction = "down"

        # Controle de animação
        self.anim_index = 0
        self.anim_counter = 0
        self.anim_speed = 4
        self.current_anim = None
        self.anim_triggered = False  # indica se a animação foi acionada

        # -----------------------------
        # Define animações do player
        # key: nome da animação
        # value: (pasta, qtd_frames, tamanho_em_pixels)
        # -----------------------------
        self.anim_data = {
            # Entry (maior, ocupa quase 2 tiles)
            "entry": ("Entry", 15, TILE_SIZE * 2),

            # Walking unknown
            "walk_right_unknown": ("walking/Walk_Right_Unknown", 14, TILE_SIZE),
            "walk_left_unknown": ("walking/Walk_Left_Unknown", 14, TILE_SIZE),

            # Walking known
            "walk_right_known": ("walking/Walk_Right_Known", 8, TILE_SIZE),
            "walk_left_known": ("walking/Walk_Left_Known", 9, TILE_SIZE),

            # Vertical walking
            "walk_up": ("walking/Walk_Up", 11, TILE_SIZE),
            "walk_down": ("walking/Walk_Down", 14, TILE_SIZE),

            # Flags
            "flag_right": ("flag/Flag_Right", 10, int(TILE_SIZE * 1.5)),
            "flag_left": ("flag/Flag_Left", 10, int(TILE_SIZE * 1.5)),
            "flag_up": ("flag/Flag_Up", 10, int(TILE_SIZE * 1.5)),
            "flag_down": ("flag/Flag_Down", 10, int(TILE_SIZE * 1.5)),
        }

        # Carrega todas as animações
        self.animations = {}
        for name, (folder, count, size) in self.anim_data.items():
            self.animations[name] = self.load_anim(folder, count, size)

        # Começa com animação entry
        self.set_animation("entry", force=True)

    # -----------------------------
    # Carrega animação
    # -----------------------------
    def load_anim(self, folder, count, size):
        frames = []
        for i in range(count):
            path = f"{SPRITES_PATH}Player/{folder}/{folder.split('/')[-1]}_{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
            except FileNotFoundError:
                img = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

            # Escala proporcional
            img_w, img_h = img.get_size()
            scale = size / max(img_w, img_h)
            img = pygame.transform.scale(img, (int(img_w*scale), int(img_h*scale)))

            # Canvas fixo
            frame = pygame.Surface((size, size), pygame.SRCALPHA)
            frame.blit(
                img,
                ((size - img.get_width()) // 2,
                 (size - img.get_height()) // 2)
            )

            frames.append(frame)
        return frames

    # -----------------------------
    # Inicia animação
    # -----------------------------
    def set_animation(self, name, force=False):
        if force or self.current_anim != self.animations[name]:
            self.current_anim = self.animations[name]
            self.anim_index = 0
            self.anim_counter = 0
            self.anim_triggered = True

            if "walk" in name:
                self.state = "walk"
            elif "flag" in name:
                self.state = "flag"
            elif name == "entry":
                self.state = "entry"
            else:
                self.state = "idle"

    # -----------------------------
    # Atualiza animação
    # -----------------------------
    def update_animation(self):
        if not self.anim_triggered:
            return

        self.anim_counter += 1
        if self.anim_counter >= self.anim_speed:
            self.anim_counter = 0
            self.anim_index += 1

            if self.anim_index >= len(self.current_anim):
                self.anim_index = len(self.current_anim) - 1
                self.anim_triggered = False
                self.state = "idle"

    # -----------------------------
    # Movimento
    # -----------------------------
    def move(self, dr, dc, board):
        if not self.alive:
            return

        nr = self.row + dr
        nc = self.col + dc

        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            tile = board.grid[nr][nc]

            # Direção
            if dr == 0 and dc == 1: self.direction = "right"
            elif dr == 0 and dc == -1: self.direction = "left"
            elif dr == -1: self.direction = "up"
            elif dr == 1: self.direction = "down"

            # Animação correta
            if tile.revealed:
                if self.direction in ["left", "right"]:
                    self.set_animation(f"walk_{self.direction}_known", force=True)
                else:
                    self.set_animation(f"walk_{self.direction}", force=True)
            else:
                if self.direction in ["left", "right"]:
                    self.set_animation(f"walk_{self.direction}_unknown", force=True)
                else:
                    self.set_animation(f"walk_{self.direction}", force=True)

            self.row = nr
            self.col = nc
            board.reveal(nr, nc)

            # Morre apenas se for mina SEM bandeira
            if tile.mine and not tile.flagged:
                self.alive = False

    # -----------------------------
    # Colocar bandeira
    # -----------------------------
    def place_flag(self, dr, dc, board):
        if not self.alive:
            return  # morto não coloca bandeira

        nr = self.row + dr
        nc = self.col + dc

        if 0 <= nr < board.rows and 0 <= nc < board.cols:
            tile = board.grid[nr][nc]
            if not tile.revealed:
                tile.flagged = not tile.flagged

                if dr == 0 and dc == 1:
                    self.set_animation("flag_right", force=True)
                elif dr == 0 and dc == -1:
                    self.set_animation("flag_left", force=True)
                elif dr == -1:
                    self.set_animation("flag_up", force=True)
                elif dr == 1:
                    self.set_animation("flag_down", force=True)

    # -----------------------------
    # Desenhar player
    # -----------------------------
    def draw(self, screen, offset_x, offset_y):
        img = self.current_anim[self.anim_index]
        size = img.get_width()

        # Offset extra só para entry
        left_shift = 10 if self.state == "entry" else 0

        px = offset_x + self.col * TILE_SIZE + TILE_SIZE // 2 - size // 2 - left_shift
        py = offset_y + (self.row + 1) * TILE_SIZE - size - 6

        screen.blit(img, (px, py))
