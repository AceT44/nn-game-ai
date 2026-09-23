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

        self.player = Player(self)
        self.obstacle = Obstacle(self)

        self.running = True
        self.score = 0
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP) and self.player.jumping == False:
                        self.player.jump()

            self.player.update()
            self.obstacle.update()

            self.check_collision()
            self.get_score()

            self.screen.fill('white')

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

            pygame.display.update()

            self.clock.tick(60)

    def check_collision(self):  # could be improved with stricter collision detection
        if self.player.player_rect.colliderect(self.obstacle.obstacle_rect):
            if self.player.vel_y > 0 and self.player.player_rect.y < self.obstacle.obstacle_rect.y:
                self.player.player_rect.bottom = self.obstacle.obstacle_rect.top
                self.player.vel_y = 0
                self.player.jumping = False
            else:
                self.running = False

    def get_score(self):
        if self.obstacle.passed_obstacle == True:
            self.score += 1
            print(self.score)


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
        self.obstacle_rect = pygame.Rect(800, 500, 50, 100)
        self.passed_obstacle = False

    def update(self):
        self.passed_obstacle = False
        self.obstacle_rect.x += self.vel_x

        if self.obstacle_rect.right < 0:
            self.passed_obstacle = True
            self.obstacle_rect.x = self.game.GAME_WIDTH
