import pygame
import random

class TicTacToe:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 100)

    def draw_board(self):
        for i in range(1, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i * 200, 0), (i * 200, 600), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 200), (600, i * 200), 5)

    def draw_pieces(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'X':
                    self.screen.blit(self.font.render('X', True, (255, 0, 0)), (j * 200 + 80, i * 200 + 80))
                elif self.board[i][j] == 'O':
                    self.screen.blit(self.font.render('O', True, (0, 0, 255)), (j * 200 + 80, i * 200 + 80))

    def handle_click(self, event):
        x = event.pos[0] // 200
        y = event.pos[1] // 200
        if self.board[y][x] is None:
            self.board[y][x] = self.current_player
            if self.check_win():
                self.winner = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != None:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return True
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event)

            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.draw_pieces()
            if self.winner:
                self.screen.blit(self.font.render("Winner: " + self.winner, True, (0, 0, 0)), (100, 100))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()