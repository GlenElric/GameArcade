import pygame
import random

class SnakeLadder:
    def __init__(self, screen):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.board = [[None for _ in range(10)] for _ in range(10)]
        self.snakes = [(25, 35), (50, 60), (75, 85)]
        self.ladders = [(10, 20), (30, 40), (55, 65)]
        self.player_position = 0

        pygame.init()
        self.screen = screen
        pygame.display.set_caption("Snake Ladder")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)

    def draw_board(self):
        for i in range(1, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 80, 0), (i * 80, 600), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (800, i * 60), 5)

    def draw_snakes(self):
        for snake in self.snakes:
            pygame.draw.line(self.screen, (255, 0, 0), (snake[0], 0), (snake[1], 600), 5)

    def draw_ladders(self):
        for ladder in self.ladders:
            pygame.draw.line(self.screen, (0, 255, 0), (ladder[0], 0), (ladder[1], 600), 5)

    def draw_player(self):
        player_text = self.font.render("P", True, (0, 0, 255))
        self.screen.blit(player_text, (self.player_position % 10 * 80 + 30, self.player_position // 10 * 60 + 30))

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self):
        roll = self.roll_dice()
        self.player_position += roll
        if self.player_position > 100:
            self.player_position = 200 - self.player_position
        for snake in self.snakes:
            if self.player_position == snake[0]:
                self.player_position = snake[1]
        for ladder in self.ladders:
            if self.player_position == ladder[0]:
                self.player_position = ladder[1]

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.move_player()

            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.draw_snakes()
            self.draw_ladders()
            self.draw_player()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    game = SnakeLadder(screen)
    game.play()