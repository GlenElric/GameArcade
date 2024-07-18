import pygame
import sys
from games import tetris, paint_canvas, snake_and_ladder, tic_tac_toe, ping_pong, guesscolor, HANDCRI
from database import Database
from login import login
from admin import Admin

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the title and icon
pygame.display.set_caption("Game Arcade")
icon = pygame.image.load("walpaper.jpg")
pygame.display.set_icon(icon)

# Set up the background image
background_image = pygame.image.load("walpaper.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the database connection
db = Database()

# Set up the login system
login_system = login(db)

# Set up the admin system
admin = Admin(db)

# Game list
games = [
    {"name": "Tetris", "game": tetris.Tetris()},
    {"name": "Ping Pong", "game": ping_pong.PingPong()},
    {"name": "Paint Canvas", "game": paint_canvas.PaintCanvas()},
    {"name": "Guess the Color", "game": guesscolor.GuessColor()},
    {"name": "Snake and Ladder", "game": snake_and_ladder.SnakeLadder()},
    {"name": "Tic Tac Toe", "game": tic_tac_toe.TicTacToe()}
]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the game list
    game_list_rect = pygame.Rect(100, 100, 200, 300)
    pygame.draw.rect(screen, (255, 255, 255), game_list_rect)
    for i, game in enumerate(games):
        text = font.render(game["name"], True, (0, 0, 0))
        screen.blit(text, (game_list_rect.x + 10, game_list_rect.y + 10 + i * 30))

    # Handle login and signup
    if not login_system.is_logged_in():
        login.draw_login_screen(screen)
    else:
        # Draw the game selection screen
        game_selection_rect = pygame.Rect(300, 100, 200, 300)
        pygame.draw.rect(screen, (255, 255, 255), game_selection_rect)
        for i, game in enumerate(games):
            text = font.render(game["name"], True, (0, 0, 0))
            screen.blit(text, (game_selection_rect.x + 10, game_selection_rect.y + 10 + i * 30))

        # Handle game selection
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, game in enumerate(games):
                    if game_list_rect.collidepoint(event.pos):
                        game["game"].run(screen)

    # Update the screen
    pygame.display.flip()
    pygame.time.Clock().tick(60)