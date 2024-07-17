import pygame
import random

class PaintCanvas:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.colors = ["red", "green", "blue", "yellow", "indigo", "orange", "grey", "purple", "pink", "navy", "brown", "cyan", "lime", "magenta"]
        self.color_index = random.randint(0, len(self.colors) - 1)
        self.grid_size = 15
        self.cell_size = 50

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Paint Canvas")
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                pygame.draw.rect(self.screen, (128, 128, 128), (x1, y1, x2, y2), 1)

    def handle_cell_click(self, event):
        x = event.pos[0]
        y = event.pos[1]
        col = x // self.cell_size
        row = y // self.cell_size
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        pygame.draw.rect(self.screen, self.colors[self.color_index], (x1, y1, x2, y2))
        self.color_index = random.randint(0, len(self.colors) - 1)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_cell_click(event)

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    paint_canvas = PaintCanvas()
    paint_canvas.run()