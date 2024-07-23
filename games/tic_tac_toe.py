import pygame
import sys

class TicTacToe:
    def __init__(self, screen):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.tie = False

        self.screen = screen

        pygame.init()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 36)

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
        if not self.winner and not self.tie:
            x = event.pos[0] // 200
            y = event.pos[1] // 200
            if self.board[y][x] is None:
                self.board[y][x] = self.current_player
                if self.check_win():
                    self.winner = self.current_player
                elif self.check_tie():
                    self.tie = True
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            # Handle button clicks
            if 150 <= event.pos[0] <= 450 and 250 <= event.pos[1] <= 300:
                self.reset_game()
            elif 150 <= event.pos[0] <= 450 and 350 <= event.pos[1] <= 400:
                self.return_to_menu_callback()

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

    def check_tie(self):
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True


    def blur_screen(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))
        self.screen.blit(surface, (0, 0))

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (150, 250, 300, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), (150, 350, 300, 50))
        reset_text = self.button_font.render('Reset Game', True, (255, 255, 255))
        main_menu_text = self.button_font.render('Main Menu', True, (255, 255, 255))
        self.screen.blit(reset_text, (225, 260))
        self.screen.blit(main_menu_text, (225, 360))

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
                self.blur_screen()
                self.draw_buttons()
            elif self.tie:
                self.screen.blit(self.font.render("It's a Tie!", True, (0, 0, 0)), (150, 100))
                self.blur_screen()
                self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 600))
    game = TicTacToe(screen, lambda: print("Returning to main menu"))
    game.run()
