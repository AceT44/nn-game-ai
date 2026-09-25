import pygame


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

        self.running = True
        self.game_state = 'playing'  # change later to 'menu'
        self.score = 0
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP) and self.player.jumping == False and self.game_state == 'playing':
                        self.player.jump()  # player jump while playing

                    if event.key == pygame.K_SPACE and self.game_state != 'playing':
                        self.play_again()  # restart the game after losing

            self.screen.fill('white')

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

            if self.game_state == 'game over':
                self.game_over()

            pygame.display.update()

            self.clock.tick(60)

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
        score_text = self.game_font.render(str(self.score), False, 'black')

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

    def play_again(self):
        self.score = 0
        self.game_state = 'playing'

        self.obstacle.obstacle_rect.x = self.GAME_WIDTH
        self.player.vel_y = 0
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
        self.obstacle_rect = pygame.Rect(self.game.GAME_WIDTH, 500, 50, 100)
        self.passed_obstacle = False

    def update(self):
        self.passed_obstacle = False
        self.obstacle_rect.x += self.vel_x

        if self.obstacle_rect.right < 0:  # resetting obstacle after passing the screen
            self.passed_obstacle = True
            self.obstacle_rect.x = self.game.GAME_WIDTH
