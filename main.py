import pygame
import sys
import sqlite3
from games import tic_tac_toe, tetris, Snake, HANDCRI, guesscolor, ping_pong

pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
MAGENTA = (255, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Arcade")

# Load background image
background = pygame.image.load('walpaper.png')

# Database setup
DATABASE_FILE = 'users.db'

def setup_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def sign_up(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def is_logged_in():
    return True

setup_database()

# Button properties
buttons = {
    'Tic Tac Toe': pygame.Rect(100, 200, 600, 50),
    'Tetris': pygame.Rect(100, 270, 600, 50),
    'Type Color': pygame.Rect(100, 340, 600, 50),
    'Ping Pong': pygame.Rect(100, 410, 600, 50),
    'Hand Cricket': pygame.Rect(100, 480, 600, 50),
    'Snake Game': pygame.Rect(100, 550, 600, 50),
    'quit': pygame.Rect(100, 620, 600, 50),
}

def draw_buttons():
    font = pygame.font.Font(None, 36)
    for game, rect in buttons.items():
        pygame.draw.rect(screen, GRAY if game != 'quit' else BLACK, rect)
        text = font.render(game.replace('_', ' ').title(), True, BLACK if game != 'quit' else WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_text(text, size, color, position):
    font = pygame.font.Font(None, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

def login_screen():
    username = ""
    password = ""
    input_active = 0
    running = True

    while running:
        screen.blit(background, (0, 0))

        draw_text('Login', 74, MAGENTA, (250, 100))
        draw_text('Username:', 36, MAGENTA, (100, 200))
        draw_text('Password:', 36, MAGENTA, (100, 300))

        pygame.draw.rect(screen, GRAY, pygame.Rect(100, 230, 600, 50))
        pygame.draw.rect(screen, GRAY, pygame.Rect(100, 330, 600, 50))

        draw_text(username, 36, BLACK, (110, 240))
        draw_text('*' * len(password), 36, BLACK, (110, 340))

        draw_text('Login', 36, WHITE, (100, 400))
        draw_text('Sign Up', 36, WHITE, (200, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if input_active == 0:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = 1
                    else:
                        username += event.unicode
                elif input_active == 1:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        if login(username, password):
                            return True
                    else:
                        password += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(100, 400, 100, 50).collidepoint(pos):
                    if login(username, password):
                        return True
                elif pygame.Rect(200, 400, 100, 50).collidepoint(pos):
                    if sign_up(username, password):
                        return True

def main_menu():
    logged_in = False

    while not logged_in:
        logged_in = login_screen()
        if not logged_in:
            pygame.quit()
            sys.exit()

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Display the title
        font = pygame.font.Font(None, 74)
        text = font.render('Game Arcade', True, MAGENTA)
        screen.blit(text, (250, 100))

        draw_buttons()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if buttons['Tic Tac Toe'].collidepoint(pos):
                    game = tic_tac_toe.TicTacToe(screen, lambda: main_menu())
                    game.run()
                elif buttons['Tetris'].collidepoint(pos):
                    game = tetris.Tetris(screen, lambda: main_menu())
                    game.run()
                elif buttons['Type Color'].collidepoint(pos):
                    game = guesscolor.GuessColor(screen, lambda: main_menu())
                    game.run()
                elif buttons['Ping Pong'].collidepoint(pos):
                    game = ping_pong.PingPong(lambda: main_menu())
                    game.run()
                elif buttons['Snake Game'].collidepoint(pos):
                    game = Snake.SnakeGame(screen)
                    game.gameLoop()
                elif buttons['Hand Cricket'].collidepoint(pos):
                    game = HANDCRI.HandCricket(screen, lambda: main_menu())
                    game.main()
                elif buttons['quit'].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
