import pygame
import random

class GuessColor:
    def __init__(self, screen, return_to_menu_callback=None):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown', 'Aqua', 'Magenta']
        self.score = 0
        self.background = (180, 180, 180)  # Darker background for better contrast
        self.timeleft = 60
        self.highest_score = 0
        self.user_input = ''

        self.screen = screen
        self.return_to_menu_callback = return_to_menu_callback
        pygame.init()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 40)
        self.instruction_text = self.font.render("Type in the colour of the words, and not the word text!", True, (0, 0, 0))
        self.score_text = self.font.render("Press enter to start", True, (0, 0, 0))
        self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
        self.label_text = self.font.render("", True, (0, 0, 0))
        self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))
        self.input_box_text = self.font.render("", True, (0, 0, 0))

        self.input_box = pygame.Rect(150, 450, 500, 50)
        self.reset_button = pygame.Rect(250, 520, 300, 50)
        self.main_menu_button = pygame.Rect(250, 580, 300, 50)
        self.is_game_active = False

    def start_game(self):
        if not self.is_game_active:
            self.is_game_active = True
            self.score = 0
            self.timeleft = 60
            self.user_input = ''
            self.score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            self.next_colour()

    def countdown(self):
        if self.timeleft > 0:
            self.timeleft -= 1
            self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
        else:
            self.is_game_active = False
            self.highscore()

    def next_colour(self):
        if self.timeleft > 0:
            self.score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            random.shuffle(self.colours)
            self.label_text = self.font.render(self.colours[0], True, self.get_colour(self.colours[1]))
            self.current_colour = self.colours[1]
        else:
            self.score_text = self.font.render("Time is up! Your score is " + str(self.score), True, (0, 0, 0))
            self.highscore()

    def highscore(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            self.highscore_text = self.font.render("New highscore: " + str(self.highest_score), True, (0, 0, 0))
        else:
            self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))

    def reset_game(self):
        self.score = 0
        self.timeleft = 60
        self.user_input = ''
        self.score_text = self.font.render("Press enter to start", True, (0, 0, 0))
        self.time_text = self.font.render("Time left: " + str(self.timeleft), True, (0, 0, 0))
        self.label_text = self.font.render("", True, (0, 0, 0))
        self.highscore_text = self.font.render("Highscore: " + str(self.highest_score), True, (0, 0, 0))
        self.is_game_active = False

    def get_colour(self, colour):
        colours_dict = {
            'Red': (255, 0, 0),
            'Blue': (0, 0, 255),
            'Green': (0, 255, 0),
            'Pink': (255, 192, 203),
            'Black': (0, 0, 0),
            'Yellow': (255, 255, 0),
            'Orange': (255, 165, 0),
            'White': (255, 255, 255),
            'Purple': (128, 0, 128),
            'Brown': (165, 42, 42),
            'Aqua': (0, 255, 255),
            'Magenta': (255, 0, 255)
        }
        return colours_dict[colour]

    def blur_screen(self):
        surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))
        self.screen.blit(surface, (0, 0))

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.reset_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.main_menu_button)
        reset_text = self.font.render('Reset Game', True, (255, 255, 255))
        main_menu_text = self.font.render('Main Menu', True, (255, 255, 255))
        self.screen.blit(reset_text, (315, 530))
        self.screen.blit(main_menu_text, (315, 590))

    def check_input(self):
        if self.user_input.lower() == self.current_colour.lower():
            self.score += 1
            self.user_input = ''
            self.next_colour()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.is_game_active:
                            self.start_game()
                        else:
                            self.check_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += event.unicode
                    self.input_box_text = self.font.render(self.user_input, True, (0, 0, 0))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.reset_button.collidepoint(event.pos):
                        self.reset_game()
                    elif self.main_menu_button.collidepoint(event.pos):
                        if self.return_to_menu_callback:
                            self.return_to_menu_callback()
                elif event.type == pygame.USEREVENT:
                    if self.is_game_active:
                        self.countdown()

            self.screen.fill(self.background)
            self.screen.blit(self.instruction_text, (50, 60))  # Moved down to avoid overlap
            self.screen.blit(self.score_text, (50, 100))
            self.screen.blit(self.time_text, (600, 20))  # Moved slightly up
            self.screen.blit(self.label_text, (350, 200))
            self.screen.blit(self.highscore_text, (50, 140))

            pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)
            self.screen.blit(self.input_box_text, (self.input_box.x + 10, self.input_box.y + 10))

            if not self.is_game_active:
                self.blur_screen()
                self.draw_buttons()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    game = GuessColor(screen, lambda: print("Returning to main menu"))
    game.run()
