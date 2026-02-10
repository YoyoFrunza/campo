import pygame
from constants import TILE_SIZE, WIDTH
from utils import load_face, load_digit

class HUD:
    def __init__(self, board, player):
        self.board = board
        self.player = player

        # Faces
        self.face_normal = load_face("face")
        self.face_clicking = load_face("faceClicking")
        self.face_lost = load_face("faceLost")
        self.face_won = load_face("faceWon")
        self.current_face = self.face_normal

        # Dígitos 0-9
        self.digits = [load_digit(f"displayDigit{i}") for i in range(10)]

        # Contador de minas
        self.mine_count = board.mines_count
        self.start_time = pygame.time.get_ticks()
        self.time_elapsed = 0
        self.last_tick = pygame.time.get_ticks()

        # Smile
        self.hud_y = 20
        self.smile_x = WIDTH // 2 - TILE_SIZE // 2
        self.smile_rect = pygame.Rect(self.smile_x, self.hud_y, TILE_SIZE, TILE_SIZE)

        # Controle do clique da face
        self.smile_pressed = False

    # Contador de minas restantes (dinâmico)
    def update_mine_count(self):
        flags = sum(tile.flagged for row in self.board.grid for tile in row)
        self.mine_count = max(0, self.board.mines_count - flags)

    # Atualização principal
    def update(self):
        if self.player.alive:
            now = pygame.time.get_ticks()
            if now - self.last_tick >= 1000:
                self.time_elapsed += 1
                self.last_tick += 1000

        self.update_mine_count()

        # Atualiza face
        if not self.player.alive:
            self.current_face = self.face_lost
        else:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # só muda se mouse estiver sobre a face
            if self.smile_rect.collidepoint(mouse_pos):
                if mouse_pressed and not self.smile_pressed:
                    self.current_face = self.face_clicking
                    self.smile_pressed = True
                elif not mouse_pressed and self.smile_pressed:
                    self.current_face = self.face_normal
                    self.smile_pressed = False
            else:
                self.current_face = self.face_normal
                self.smile_pressed = False

    # Clique no smile reinicia mantendo o nível
    def handle_click(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if self.smile_rect.collidepoint(mouse_pos) and mouse_pressed:
            self.board.__init__(level=getattr(self.board, 'level', 'Normal'))
            self.player.__init__(0,0)
            self.start_time = pygame.time.get_ticks()
            self.time_elapsed = 0
            self.last_tick = pygame.time.get_ticks()
            self.smile_pressed = False

    # Desenho HUD
    def draw(self, screen):
        # Minas
        mines = self.mine_count
        h = mines // 100
        t = (mines // 10) % 10
        o = mines % 10
        x_offset = 20
        screen.blit(self.digits[h], (x_offset, self.hud_y))
        screen.blit(self.digits[t], (x_offset+TILE_SIZE, self.hud_y))
        screen.blit(self.digits[o], (x_offset+TILE_SIZE*2, self.hud_y))

        # Smile
        screen.blit(self.current_face, (self.smile_x, self.hud_y))

        # Timer
        time_sec = min(self.time_elapsed, 999)
        h = time_sec // 100
        t = (time_sec // 10) % 10
        o = time_sec % 10
        timer_x = screen.get_width() - 20 - TILE_SIZE*3
        screen.blit(self.digits[h], (timer_x, self.hud_y))
        screen.blit(self.digits[t], (timer_x+TILE_SIZE, self.hud_y))
        screen.blit(self.digits[o], (timer_x+TILE_SIZE*2, self.hud_y))

    # -----------------------------
    # Define quando a face está sendo clicada
    # -----------------------------
    def set_clicking(self, clicking):
        self.current_face = self.face_clicking if clicking else self.face_normal

