import pygame
from constants import WIDTH, HEIGHT

class Menu:
    def __init__(self):
        self.options = ["Easy", "Normal", "Hard"]
        self.selected = 0
        self.font = pygame.font.SysFont("arial", 32)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % 3
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 3
            if event.key == pygame.K_RETURN:
                return self.options[self.selected]
        return None

    def draw(self, screen):
        screen.fill((180,180,180))
        for i, opt in enumerate(self.options):
            color = (0,0,0) if i == self.selected else (100,100,100)
            txt = self.font.render(opt, True, color)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 150+i*50))
