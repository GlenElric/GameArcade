import pygame
import time
import random

class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Define the colors
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

        # Define the display dimensions
        self.dis_width = 800
        self.dis_height = 600

        # Set up the display
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')

        # Set the clock
        self.clock = pygame.time.Clock()

        # Snake block size and speed
        self.snake_block = 10
        self.snake_speed = 15

        # Define the font styles
        self.font_style = pygame.font.SysFont(None, 50)
        self.score_font = pygame.font.SysFont(None, 35)

        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.game_close = False

        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2

        self.x1_change = 0
        self.y1_change = 0

        self.snake_List = []
        self.Length_of_snake = 1

        self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0

    def our_snake(self):
        for x in self.snake_List:
            pygame.draw.rect(self.dis, self.black, [x[0], x[1], self.snake_block, self.snake_block])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.black)
        self.dis.blit(value, [0, 0])

    def gameLoop(self):
        while not self.game_over:

            while self.game_close:
                self.dis.fill(self.blue)
                self.message("You Lost! Press Q-Quit or C-Play Again", self.red)
                self.your_score(self.Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = self.snake_block
                        self.x1_change = 0

            if self.x1 >= self.dis_width or self.x1 < 0 or self.y1 >= self.dis_height or self.y1 < 0:
                self.game_close = True
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            self.dis.fill(self.blue)
            pygame.draw.rect(self.dis, self.green, [self.foodx, self.foody, self.snake_block, self.snake_block])
            snake_Head = [self.x1, self.y1]
            self.snake_List.append(snake_Head)
            if len(self.snake_List) > self.Length_of_snake:
                del self.snake_List[0]

            for x in self.snake_List[:-1]:
                if x == snake_Head:
                    self.game_close = True

            self.our_snake()
            self.your_score(self.Length_of_snake - 1)

            pygame.display.update()

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                self.foody = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                self.Length_of_snake += 1

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.gameLoop()
