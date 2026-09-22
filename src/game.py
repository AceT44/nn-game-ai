import pygame


class Game:
    def __init__(self):
        self.players = Player()
        self.obstacles = Obstacle()

        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption('Game AI')

        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill('white')

            pygame.draw.rect(self.screen, 'black', self.players.player)

            pygame.display.update()

            self.clock.tick(60)


class Player:
    def __init__(self):
        self.player = pygame.Rect(x=20, y=670, width=30, height=30)

    def jump(self):
        pass


class Obstacle:
    def __init__(self):
        pass
