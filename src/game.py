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


class Player:
    JUMP_VEL = 40
    GRAVITY = 2

    def __init__(self, game):
        self.game = game

        self.player_rect = pygame.Rect(20, 550, 50, 50)
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

        self.obstacle_rect = pygame.Rect(500, 400, 100, 200)
