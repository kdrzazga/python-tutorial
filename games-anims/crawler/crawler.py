import pygame

from game import Game
from ui import UI


def main():
    game = Game(30, 30, 15, 15)
    game.start()
    game.reveal()
    ui = UI(game)
    
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            ui.draw()
            pygame.display.flip()
            
    except KeyboardInterrupt:
        pygame.quit()    


if __name__ == "__main__":
    main()
    