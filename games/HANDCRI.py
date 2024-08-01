import pygame
import random
import sys

class HandCricket:
    def __init__(self, screen):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Hand Cricket')
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.coin_buttons = self.create_buttons(["Heads", "Tails"], 300)
        self.action_buttons = self.create_buttons(["Bat", "Bowl"], 400)
        self.run_buttons = self.create_buttons([str(i) for i in range(1, 7)], 500)
        self.end_buttons = self.create_buttons(["Play Again", "Quit"], self.SCREEN_HEIGHT - 100)
        self.reset_game()

        # Load the background image
        self.background_image = pygame.image.load('cricket.png')

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.user_score = 0
        self.computer_score = 0
        self.user_batting = True
        self.coin_flip_done = False
        self.user_wins_toss = False
        self.user_toss_decision = False
        self.game_over = False
        self.second_innings = False
        self.user_choice = None
        self.computer_choice = None

    def flip_coin(self):
        """Simulate a coin flip and return 'Heads' or 'Tails'."""
        return random.choice(["Heads", "Tails"])

    def get_computer_choice(self):
        """Generate a random number between 1 and 6 for the computer's choice."""
        return random.randint(1, 6)

    def display_message(self, message, y, large=False):
        """Render and display a message at a specific vertical position."""
        if large:
            text = self.large_font.render(message, True, self.BLACK)
        else:
            text = self.font.render(message, True, self.BLACK)
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, y))
        self.screen.blit(text, text_rect)

    def create_buttons(self, labels, y):
        """Create a list of buttons with labels and positions."""
        buttons = []
        button_width = 120
        spacing = 20
        total_width = len(labels) * button_width + (len(labels) - 1) * spacing
        start_x = (self.SCREEN_WIDTH - total_width) // 2
        for i, label in enumerate(labels):
            button = pygame.Rect(start_x + i * (button_width + spacing), y, button_width, 50)
            buttons.append((button, label))
        return buttons

    def draw_buttons(self, buttons):
        """Draw buttons on the screen."""
        for button, label in buttons:
            pygame.draw.rect(self.screen, self.GRAY, button)
            text = self.font.render(label, True, self.BLACK)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)

    def handle_button_click(self, buttons, mouse_pos):
        """Check if any button was clicked and return its label."""
        for button, label in buttons:
            if button.collidepoint(mouse_pos):
                return label
        return None

    def game_logic(self):
        """Main game logic for handling the game flow and user interactions."""
        while True:
            self.screen.fill(self.WHITE)  # Clear the screen with a white background
            self.screen.blit(self.background_image, (0, 0))  # Blit the background image

            if not self.coin_flip_done:
                self.display_message('Call Heads or Tails', 150)
                self.draw_buttons(self.coin_buttons)
            elif not self.user_toss_decision and self.user_wins_toss:
                self.display_message('You won the toss! Choose to bat or bowl.', 200)
                self.draw_buttons(self.action_buttons)
            elif not self.game_over:
                self.display_message(f'User Score: {self.user_score}', 50)
                self.display_message(f'Computer Score: {self.computer_score}', 100)

                if not self.second_innings:
                    if self.user_batting:
                        self.display_message('You are batting now.', 150)
                    else:
                        self.display_message('Computer is batting now.', 150)
                else:
                    if self.user_batting:
                        self.display_message('You are batting now. Second Innings', 150)
                    else:
                        self.display_message('Computer is batting now. Second Innings', 150)

                if self.user_choice is not None and self.computer_choice is not None:
                    self.display_message(f'User Input: {self.user_choice}', 200)
                    self.display_message(f'Computer Input: {self.computer_choice}', 250)

                self.draw_buttons(self.run_buttons)
            else:
                self.display_message(f'User Score: {self.user_score}', 50)
                self.display_message(f'Computer Score: {self.computer_score}', 100)
                if self.user_score > self.computer_score:
                    self.display_message('You win!', 200, large=True)
                elif self.computer_score > self.user_score:
                    self.display_message('Computer wins!', 200, large=True)
                else:
                    self.display_message('It\'s a tie!', 200, large=True)
                self.display_message('Press Play Again to restart or Quit to exit.', 350)
                self.draw_buttons(self.end_buttons)

            pygame.display.flip()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if not self.coin_flip_done:
                        choice = self.handle_button_click(self.coin_buttons, mouse_pos)
                        if choice:
                            user_call = choice
                            coin_result = self.flip_coin()
                            print(f"Coin result: {coin_result}")
                            self.user_wins_toss = (user_call == coin_result)
                            if self.user_wins_toss:
                                print("You won the toss!")
                            else:
                                print("Computer won the toss!")
                                computer_decision = random.choice(["bat", "bowl"])
                                self.user_batting = (computer_decision == "bowl")
                                print(f"Computer chose to {computer_decision} first.")
                            self.coin_flip_done = True
                    elif self.user_wins_toss and not self.user_toss_decision:
                        choice = self.handle_button_click(self.action_buttons, mouse_pos)
                        if choice:
                            self.user_batting = (choice == "Bat")
                            self.user_toss_decision = True
                            print(f"You chose to {choice.lower()} first.")
                    elif self.coin_flip_done and not self.game_over:
                        choice = self.handle_button_click(self.run_buttons, mouse_pos)
                        if choice:
                            self.user_choice = int(choice)
                            self.computer_choice = self.get_computer_choice()
                            print(f"User chose: {self.user_choice}, Computer chose: {self.computer_choice}")

                            if self.user_choice == self.computer_choice:
                                if self.user_batting:
                                    self.display_message('You are out!', 300, large=True)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    if not self.second_innings:
                                        self.user_batting = False
                                        self.second_innings = True
                                    else:
                                        self.game_over = True
                                else:
                                    self.display_message('Computer is out!', 300, large=True)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    if not self.second_innings:
                                        self.user_batting = True
                                        self.second_innings = True
                                    else:
                                        self.game_over = True
                            else:
                                if self.user_batting:
                                    self.user_score += self.user_choice
                                    if self.second_innings and self.user_score > self.computer_score:
                                        self.game_over = True
                                else:
                                    self.computer_score += self.computer_choice
                                    if self.second_innings and self.computer_score > self.user_score:
                                        self.game_over = True

                    elif self.game_over:
                        choice = self.handle_button_click(self.end_buttons, mouse_pos)
                        if choice:
                            if choice == "Play Again":
                                self.reset_game()
                            elif choice == "Quit":
                                pygame.quit()
                                sys.exit()

    def main(self):
        """Main function to run the game."""
        self.game_logic()

if __name__ == "__main__":
    game = HandCricket(screen=None)
    game.main()
