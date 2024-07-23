import pygame
import random
import time

class Tetris:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    CELL_SIZE = 30

    def __init__(self, screen=None):
        self.screen = screen
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.time_elapsed = 0
        self.start_time = time.time()
        self.piece_colors = [pygame.Color('cyan'), pygame.Color('blue'), pygame.Color('orange'), 
                             pygame.Color('yellow'), pygame.Color('green'), pygame.Color('purple'), pygame.Color('red')]
        self.piece_shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1], [1, 1]],  # O
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]],  # Z
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]]   # J
        ]
        self.piece_positions = [(0, 3)] * len(self.piece_shapes)  # Default position
        self.fall_time = 0
        self.fall_speed = 500  # Starting speed (milliseconds)
        self.last_line_clear_time = pygame.time.get_ticks()
        self.time_bonus_factor = 0.1  # Time bonus factor for scoring
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 36)

    def generate_piece(self):
        shape = random.choice(self.piece_shapes)
        color = random.choice(self.piece_colors)
        return {'shape': shape, 'color': color, 'position': [0, 3]}

    def draw_grid(self):
        grid_x = (self.SCREEN_WIDTH - self.GRID_WIDTH * self.CELL_SIZE) // 2
        grid_y = (self.SCREEN_HEIGHT - self.GRID_HEIGHT * self.CELL_SIZE) // 2
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                pygame.draw.rect(self.screen, pygame.Color('darkgrey'), pygame.Rect(grid_x + x * self.CELL_SIZE, grid_y + y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 1)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], pygame.Rect(grid_x + x * self.CELL_SIZE, grid_y + y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def draw_piece(self, piece):
        shape = piece['shape']
        color = piece['color']
        position = piece['position']
        grid_x = (self.SCREEN_WIDTH - self.GRID_WIDTH * self.CELL_SIZE) // 2
        grid_y = (self.SCREEN_HEIGHT - self.GRID_HEIGHT * self.CELL_SIZE) // 2
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, pygame.Rect(grid_x + (position[1] + x) * self.CELL_SIZE, grid_y + (position[0] + y) * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def move_piece_left(self):
        self.current_piece['position'][1] -= 1
        if self.check_collision():
            self.current_piece['position'][1] += 1

    def move_piece_right(self):
        self.current_piece['position'][1] += 1
        if self.check_collision():
            self.current_piece['position'][1] -= 1

    def move_piece_down(self):
        self.current_piece['position'][0] += 1
        if self.check_collision():
            self.current_piece['position'][0] -= 1
            self.update_grid()
            self.clear_lines()
            self.current_piece = self.generate_piece()
            if self.check_collision():
                self.game_over()

    def rotate_piece(self):
        shape = self.current_piece['shape']
        self.current_piece['shape'] = [list(row) for row in zip(*shape[::-1])]
        if self.check_collision():
            self.current_piece['shape'] = shape

    def update_grid(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        position = self.current_piece['position']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[position[0] + y][position[1] + x] = color

    def check_collision(self):
        shape = self.current_piece['shape']
        position = self.current_piece['position']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = position[1] + x
                    grid_y = position[0] + y
                    if grid_x < 0 or grid_x >= self.GRID_WIDTH or grid_y >= self.GRID_HEIGHT or (grid_y >= 0 and self.grid[grid_y][grid_x]):
                        return True
        return False

    def clear_lines(self):
        current_time = pygame.time.get_ticks()
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for line in full_lines:
            self.grid.pop(line)
            self.grid.insert(0, [0 for _ in range(self.GRID_WIDTH)])
        self.score += len(full_lines) * (1000 - (current_time - self.last_line_clear_time) * self.time_bonus_factor)
        self.last_line_clear_time = current_time
        self.adjust_speed()

    def adjust_speed(self):
        level = self.score // 500  # Adjust the divisor to change how quickly the speed increases
        self.fall_speed = max(100, 500 - level * 50)  # Minimum speed of 100 ms

    def blur_screen(self):
        surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))
        self.screen.blit(surface, (0, 0))

    def draw_buttons(self):
        button_width = 150
        button_height = 50
        button_margin = 20
        button_y = self.SCREEN_HEIGHT - button_height - button_margin
        pygame.draw.rect(self.screen, (0, 0, 0), (self.SCREEN_WIDTH - button_width - button_margin, button_y, button_width, button_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.SCREEN_WIDTH - 2 * button_width - 2 * button_margin, button_y, button_width, button_height))
        reset_text = self.button_font.render('Reset Game', True, (255, 255, 255))
        main_menu_text = self.button_font.render('Main Menu', True, (255, 255, 255))
        self.screen.blit(reset_text, (self.SCREEN_WIDTH - button_width - button_margin + 10, button_y + 10))
        self.screen.blit(main_menu_text, (self.SCREEN_WIDTH - 2 * button_width - 2 * button_margin + 10, button_y + 10))

    def game_over(self):
        print(f"Game Over! Your score was {self.score}")
        self.screen.blit(self.font.render("Score: " + str(self.score), True, (0, 0, 0)), (100, 100))
        self.blur_screen()
        self.draw_buttons()
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause to show the game over screen
        pygame.quit()
        exit()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.score = 0
        self.fall_time = pygame.time.get_ticks()

        while True:
            current_time = pygame.time.get_ticks()
            self.time_elapsed = int(time.time() - self.start_time)
            if current_time - self.fall_time > self.fall_speed:
                self.move_piece_down()
                self.fall_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    button_width = 150
                    button_height = 50
                    button_margin = 20
                    button_y = self.SCREEN_HEIGHT - button_height - button_margin
                    if pygame.Rect(self.SCREEN_WIDTH - button_width - button_margin, button_y, button_width, button_height).collidepoint(pos):
                        self.reset_game()
                    elif pygame.Rect(self.SCREEN_WIDTH - 2 * button_width - 2 * button_margin, button_y, button_width, button_height).collidepoint(pos):
                        pygame.quit()
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece_right()
                    elif event.key == pygame.K_DOWN:
                        self.move_piece_down()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.screen.fill(pygame.Color('PeachPuff'))
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_buttons()
            score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            time_text = self.font.render(f"Time: {self.time_elapsed}", True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(time_text, (10, 50))
            pygame.display.flip()
            self.clock.tick(30)  # Fixed frame rate

    def reset_game(self):
        self.grid = [[0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.score = 0
        self.fall_time = pygame.time.get_ticks()
        self.start_time = time.time()

if __name__ == "__main__":
    Tetris().run()