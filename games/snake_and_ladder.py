import pygame
import random

class SnakeLadder:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.board = [[None for _ in range(10)] for _ in range(10)]
        self.snakes = [(25, 35), (50, 60), (75, 85)]
        self.ladders = [(10, 20), (30, 40), (55, 65)]
        self.player_position = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Ladder")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)

    def draw_board(self):
        for i in range(1, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 80, 0), (i * 80, 600), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (800, i * 60), 5)

    def draw_snakes(self):
        for snake in self.snakes:
            pygame.draw.line(self.screen, (255, 0)),