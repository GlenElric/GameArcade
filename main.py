import pygame
import sys
from utils import auth, db
from games import tetris, paint_canvas, snake_and_ladder, tic_tac_toe

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Arcade")

# Load background image
background = pygame.image.load('walpaper.png')

# Database setup
db.setup_database()

# Button properties
buttons = {
    'tic_tac_toe': pygame.Rect(100, 200, 600, 50),
    'tetris': pygame.Rect(100, 270, 600, 50),
    'paint_canvas': pygame.Rect(100, 340, 600, 50),
    'snake_and_ladder': pygame.Rect(100, 410, 600, 50),
    'quit': pygame.Rect(100, 480, 600, 50),
}

def draw_buttons():
    font = pygame.font.Font(None, 36)
    for game, rect in buttons.items():
        pygame.draw.rect(screen, GRAY if game != 'quit' else BLACK, rect)
        text = font.render(game.replace('_', ' ').title(), True, BLACK if game != 'quit' else WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def main_menu():
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Display the title
        font = pygame.font.Font(None, 74)
        text = font.render('Game Arcade', True, WHITE)
        screen.blit(text, (250, 100))

        draw_buttons()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons['tic_tac_toe'].collidepoint(pos):
                    game = tic_tac_toe.TicTacToe()
                    game.run()
                elif buttons['tetris'].collidepoint(pos):
                    game = tetris.Tetris(screen)
                    game.run()
                elif buttons['paint_canvas'].collidepoint(pos):
                    game = paint_canvas.PaintCanvas(screen)
                    game.run()
                elif buttons['snake_and_ladder'].collidepoint(pos):
                    game = snake_and_ladder.SnakeLadder(screen)
                    game.run()
                elif buttons['quit'].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
