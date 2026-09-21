import pygame


class Game:
    def __init__(self):
        pass

    def run(self):
        root = pygame.display.set_mode((700, 700))
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
