import pygame
import random
import sys

class PingPong:
    def __init__(self,screen=None):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BALL_RADIUS = 20
        self.PAD_WIDTH = 10
        self.PAD_HEIGHT = 100
        self.LEFT = False
        self.RIGHT = True

        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]
        self.ball_vel = [0, 0]

        self.paddle1_pos = self.HEIGHT // 2 - self.PAD_HEIGHT // 2
        self.paddle2_pos = self.HEIGHT // 2 - self.PAD_HEIGHT // 2

        self.paddle1_vel = 0
        self.paddle2_vel = 0

        self.score1 = 0
        self.score2 = 0

        self.lives1 = 3
        self.lives2 = 3
        self.game_over = False

        self.DARK_MODE = {
            "background": (0, 0, 0),
            "mid_line": (255, 255, 255),
            "paddle1": (0, 0, 255),
            "paddle2": (0, 128, 0),
            "ball_outer": (255, 0, 0),
            "ball_inner": (255, 255, 255),
            "text": (255, 255, 255),
            "game_over": (255, 0, 0),
        }
        self.LIGHT_MODE = {
            "background": (255, 255, 255),
            "mid_line": (0, 0, 0),
            "paddle1": (0, 0, 255),
            "paddle2": (0, 128, 0),
            "ball_outer": (255, 0, 0),
            "ball_inner": (0, 0, 0),
            "text": (0, 0, 0),
            "game_over": (0, 0, 0),
        }
        self.current_mode = self.DARK_MODE

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.spawn_ball(self.RIGHT)

    def spawn_ball(self, direction):
        self.ball_pos = [self.WIDTH // 2, self.HEIGHT // 2]
        vx = random.randrange(120, 240) / 60
        vy = -random.randrange(60, 180) / 60
        if direction == self.LEFT:
            vx = -vx
        self.ball_vel = [vx, vy]

    def draw(self):
        self.screen.fill(self.current_mode["background"])

        if self.game_over:
            font = pygame.font.Font(None, 50)
            text = font.render("GAME OVER", True, self.current_mode["game_over"])
            self.screen.blit(text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50))
            if self.score1 > self.score2:
                text = font.render("Player 1 Wins!", True, self.current_mode["game_over"])
                self.screen.blit(text, (self.WIDTH // 2 - 120, self.HEIGHT // 2 + 50))
            elif self.score2 > self.score1:
                text = font.render("Player 2 Wins!", True, self.current_mode["game_over"])
                self.screen.blit(text, (self.WIDTH // 2 - 120, self.HEIGHT // 2 + 50))
            else:
                text = font.render("It's a Tie!", True, self.current_mode["game_over"])
                self.screen.blit(text, (self.WIDTH // 2 - 70, self.HEIGHT // 2 + 50))
            text = font.render(f"Final Score: Player 1 - {self.score1}, Player 2 - {self.score2}", True, self.current_mode["game_over"])
            self.screen.blit(text, (self.WIDTH // 2 - 160, self.HEIGHT // 2 + 100))
        else:
            # Draw mid line
            pygame.draw.line(self.screen, self.current_mode["mid_line"], (self.WIDTH / 2, 0), (self.WIDTH / 2, self.HEIGHT), 3)

            # Update ball
            self.ball_pos[0] += self.ball_vel[0]
            self.ball_pos[1] += self.ball_vel[1]

            # Ball collision with top and bottom
            if self.ball_pos[1] <= self.BALL_RADIUS or self.ball_pos[1] >= self.HEIGHT - self.BALL_RADIUS:
                self.ball_vel[1] = -self.ball_vel[1]

            # Ball collision with paddles
            if self.ball_pos[0] <= self.PAD_WIDTH + self.BALL_RADIUS:
                if self.paddle1_pos <= self.ball_pos[1] <= self.paddle1_pos + self.PAD_HEIGHT:
                    self.ball_vel[0] = -self.ball_vel[0]
                else:
                    self.lives1 -= 1
                    if self.lives1 == 0:
                        self.game_over = True
                    self.spawn_ball(self.RIGHT)
                    self.score2 += 1
            if self.ball_pos[0] >= self.WIDTH - self.PAD_WIDTH - self.BALL_RADIUS:
                if self.paddle2_pos <= self.ball_pos[1] <= self.paddle2_pos + self.PAD_HEIGHT:
                    self.ball_vel[0] = -self.ball_vel[0]
                else:
                    self.lives2 -= 1
                    if self.lives2 == 0:
                        self.game_over = True
                    self.spawn_ball(self.LEFT)
                    self.score1 += 1

            # Draw ball
            pygame.draw.circle(self.screen, self.current_mode["ball_outer"], self.ball_pos, self.BALL_RADIUS)
            pygame.draw.circle(self.screen, self.current_mode["ball_inner"], self.ball_pos, self.BALL_RADIUS - 5)

            # Draw paddles
            pygame.draw.rect(self.screen, self.current_mode["paddle1"], (0, self.paddle1_pos, self.PAD_WIDTH, self.PAD_HEIGHT))
            pygame.draw.rect(self.screen, self.current_mode["paddle2"], (self.WIDTH - self.PAD_WIDTH, self.paddle2_pos, self.PAD_WIDTH, self.PAD_HEIGHT))

            # Draw scores
            font = pygame.font.Font(None, 50)
            score1_text = font.render(str(self.score1), True, self.current_mode["text"])
            score2_text = font.render(str(self.score2), True, self.current_mode["text"])
            self.screen.blit(score1_text, (self.WIDTH // 4, 20))
            self.screen.blit(score2_text, (self.WIDTH * 3 // 4, 20))

            # Draw lives
            lives1_text = font.render(f"Lives: {self.lives1}", True, self.current_mode["text"])
            lives2_text = font.render(f"Lives: {self.lives2}", True, self.current_mode["text"])
            self.screen.blit(lives1_text, (self.WIDTH // 4, 70))
            self.screen.blit(lives2_text, (self.WIDTH * 3 // 4, 70))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.paddle1_vel = -5
                elif event.key == pygame.K_s:
                    self.paddle1_vel = 5
                elif event.key == pygame.K_UP:
                    self.paddle2_vel = -5
                elif event.key == pygame.K_DOWN:
                    self.paddle2_vel = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.paddle1_vel = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.paddle2_vel = 0

    def update(self):
        self.paddle1_pos += self.paddle1_vel
        self.paddle2_pos += self.paddle2_vel

        # Keep paddles on the screen
        if self.paddle1_pos < 0:
            self.paddle1_pos = 0
        elif self.paddle1_pos > self.HEIGHT - self.PAD_HEIGHT:
            self.paddle1_pos = self.HEIGHT - self.PAD_HEIGHT

        if self.paddle2_pos < 0:
            self.paddle2_pos = 0
        elif self.paddle2_pos > self.HEIGHT - self.PAD_HEIGHT:
            self.paddle2_pos = self.HEIGHT - self.PAD_HEIGHT

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = PingPong()
    game.run()
