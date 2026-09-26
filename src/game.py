import random
import pygame
import numpy as np
from ai import NeuralNetwork


class Game:
    GAME_WIDTH = 800
    GAME_HEIGHT = 600

    def __init__(self):
        self.screen = pygame.display.set_mode((
            self.GAME_WIDTH,
            self.GAME_HEIGHT
        ))
        pygame.display.set_caption('Game AI')

        self.game_font = pygame.font.SysFont('Arial', 36)

        self.player = Player(self)
        self.obstacle = Obstacle(self)
        self.neural_network = NeuralNetwork()

        self.running = True
        self.game_state = 'menu'
        self.score = 0
        self.game_mode = None
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.game_state == 'menu':
                        self.game_mode = 'normal'
                        self.game_state = 'playing'

                    if event.key == pygame.K_2 and self.game_state == 'menu':
                        self.game_mode = 'ai'
                        self.game_state = 'playing'

                    if event.key in (pygame.K_SPACE, pygame.K_UP) and self.player.jumping == False and self.game_state == 'playing':
                        self.player.jump()  # player jump while playing

                    if event.key == pygame.K_SPACE and self.game_state == 'game over':
                        self.reset_game()  # restart the game after losing

                    if event.key == pygame.K_q and self.game_state == 'game over':
                        self.menu()

            self.screen.fill('white')

            if self.game_state == 'menu':
                self.menu()

            if self.game_state == 'playing':
                self.player.update()
                self.obstacle.update()

                self.check_collision()

                self.get_score()
                self.draw_score()

                pygame.draw.rect(  # draw the player
                    self.screen,
                    'black',
                    self.player.player_rect
                )

                pygame.draw.rect(  # draw the obstacles
                    self.screen,
                    'black',
                    self.obstacle.obstacle_rect
                )

                if self.game_mode == 'ai':  # defining the inputs for the AI
                    distance = self.obstacle.obstacle_rect.left - self.player.player_rect.right
                    obstacle_height = self.obstacle.choose_height
                    player_velocity = self.player.vel_y

                    inputs = np.array([
                        distance,
                        obstacle_height,
                        player_velocity
                    ])

                    output = self.neural_network.predict(inputs)
                    print(output[0])  # remove later

            if self.game_state == 'game over':
                self.game_over()

            pygame.display.update()

            self.clock.tick(60)

    def menu(self):
        self.reset_game()
        self.game_state = 'menu'

        normal_mode_text = self.game_font.render(
            'PRESS 1 FOR NORMAL MODE',
            False,
            'black'
        )

        ai_mode_text = self.game_font.render(
            'PRESS 2 FOR AI MODE',
            False,
            'black'
        )

        self.screen.blit(
            normal_mode_text,
            (self.GAME_WIDTH // 4, self.GAME_HEIGHT // 8)
        )

        self.screen.blit(
            ai_mode_text,
            (self.GAME_WIDTH // 4, self.GAME_HEIGHT // 4)
        )

    def check_collision(self):  # could be improved with stricter collision detection
        if self.player.player_rect.colliderect(self.obstacle.obstacle_rect):
            if self.player.vel_y > 0 and self.player.player_rect.y < self.obstacle.obstacle_rect.y:
                self.player.player_rect.bottom = self.obstacle.obstacle_rect.top
                self.player.vel_y = 0
                self.player.jumping = False
            else:
                self.game_state = 'game over'

    def get_score(self):
        if self.obstacle.passed_obstacle == True:
            self.score += 1

    def draw_score(self):
        score_text = self.game_font.render(
            str(self.score),
            False,
            'black'
        )

        self.screen.blit(
            score_text,
            (self.GAME_WIDTH // 2, self.GAME_HEIGHT // 8)
        )

    def game_over(self):
        game_over_text = self.game_font.render(
            'GAME OVER!',
            False,
            'black'
        )

        final_score_text = self.game_font.render(
            f'FINAL SCORE: {str(self.score)}',
            False,
            'black'
        )

        restart_text = self.game_font.render(
            'PRESS SPACE TO PLAY AGAIN',
            False,
            'black'
        )

        return_menu_text = self.game_font.render(
            'PRESS Q TO RETURN TO THE MENU',
            False,
            'black'
        )

        self.screen.blit(
            game_over_text,
            (self.GAME_WIDTH // 3, self.GAME_HEIGHT // 10)
        )

        self.screen.blit(
            final_score_text,
            (self.GAME_WIDTH // 3, self.GAME_HEIGHT // 4)
        )

        self.screen.blit(
            restart_text,
            (self.GAME_WIDTH // 6, self.GAME_HEIGHT // 2)
        )

        self.screen.blit(
            return_menu_text,
            (self.GAME_WIDTH // 7, self.GAME_HEIGHT // 1.5)
        )

    def reset_game(self):
        self.score = 0

        if self.game_state == 'game over':
            self.game_state = 'playing'

        self.obstacle.obstacle_rect.x = self.GAME_WIDTH
        self.obstacle.vel_x = -3
        self.obstacle.passed_obstacle = False

        self.player.vel_y = 0
        self.player.player_rect.y = self.GAME_HEIGHT - self.player.PLAYER_HEIGHT
        self.player.jumping = False


class Player:
    JUMP_VEL = 17
    GRAVITY = 0.8
    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 50

    def __init__(self, game):
        self.game = game

        self.player_rect = pygame.Rect(
            20,
            550,
            self.PLAYER_WIDTH,
            self.PLAYER_HEIGHT
        )
        self.vel_y = 0
        self.jumping = False

    def jump(self):
        self.jumping = True
        self.vel_y -= self.JUMP_VEL

    def update(self):
        self.vel_y += self.GRAVITY
        self.player_rect.y += self.vel_y

        if self.player_rect.y + self.player_rect.height > self.game.GAME_HEIGHT:
            self.player_rect.y = self.game.GAME_HEIGHT - self.player_rect.height
            self.jumping = False
            self.vel_y = 0


class Obstacle:
    def __init__(self, game):
        self.game = game

        self.vel_x = -3
        self.passed_obstacle = False

        self.generate_obstacle()

    def generate_obstacle(self):
        obstacle_heights = (25, 75, 125)

        self.choose_height = random.choices(
            obstacle_heights,
            weights=[5, 3, 2]
        )[0]

        self.obstacle_rect = pygame.Rect(
            self.game.GAME_WIDTH,
            self.game.GAME_HEIGHT - self.choose_height,
            50,
            self.choose_height
        )

    def update(self):
        self.passed_obstacle = False
        self.obstacle_rect.x += self.vel_x

        if self.obstacle_rect.right < 0:  # resetting obstacle after passing the screen
            self.passed_obstacle = True
            self.obstacle_rect.x = self.game.GAME_WIDTH
            self.vel_x -= 0.2
            self.generate_obstacle()
