import pygame

class Tetris:
    def __init__(self):
        self.screen = None
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0

    def run(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.score = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece