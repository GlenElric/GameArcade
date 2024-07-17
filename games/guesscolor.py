import pygame
import random

class GuessColor:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown', 'Aqua', 'Magenta']
        self.score = 0
        self.background = (240, 240, 240)
        self.timeleft = 60
        self.highest_score = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Color Game")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 40)
        self.instruction_text = self.font.render("Type in the colour of the words, and not the word text!", True, (0, 0, 0))
        self.score_text = self.font.render("Press enter to start", True, (0, 0, 0))
        self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
        self.label_text = self.font.render("", True, (0, 0, 0))
        self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))

    def start_game(self):
        if self.timeleft == 60:
            self.countdown()
        self.next_colour()

    def countdown(self):
        if self.timeleft > 0:
            self.timeleft -= 1
            self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
            pygame.time.delay(1000)
            self.countdown()
        else:
            self.highscore()

    def next_colour(self):
        if self.timeleft > 0:
            self.score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            random.shuffle(self.colours)
            self.label_text = self.font.render(self.colours[0], True, self.get_colour(self.colours[1]))
        else:
            self.score_text = self.font.render("Time is up! Your score is " + str(self.score), True, (0, 0, 0))
            self.highscore()

    def highscore(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.highscore_text = self.font.render("New highscore: " + str(self.highest_score), True, (0, 0, 0))
        else:
            self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))

    def restart_game(self):
        self.score = 0
        self.timeleft = 60
        self.score_text = self.font.render("Press enter to start", True, (0, 0, 0))
        self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
        self.label_text = self.font.render("", True, (0, 0, 0))
        self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))

    def get_colour(self, colour):
        if colour == 'Red':
            return (255, 0, 0)
        elif colour == 'Blue':
            return (0, 0, 255)
        elif colour == 'Green':
            return (0, 255, 0)
        elif colour == 'Pink':
            return (255, 192, 203)
        elif colour == 'Black':
            return (0, 0, 0)
        elif colour == 'Yellow':
            return (255, 255, 0)
        elif colour == 'Orange':
            return (255, 165, 0)
        elif colour == 'White':
            return (255, 255, 255)
        elif colour == 'Purple':
            return (128, 0, 128)
        elif colour == 'Brown':
            return (165, 42, 42)
        elif colour == 'Aqua':
            return (0, 255, 255)
        elif colour == 'Magenta':
            return (255, 0, 255)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    pass
                   