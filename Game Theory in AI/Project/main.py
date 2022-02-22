import traceback
import pygame

from game import Game

try:
    pygame.init()
    g = Game()
    g.run()
except KeyboardInterrupt:
    pass
except (Exception,):
    traceback.print_exc()
    input()
finally:
    pygame.quit()
