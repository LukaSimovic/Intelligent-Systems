import random

import config
from sprites import BaseSprite


class Tile(BaseSprite):
    def __init__(self, position, file_name):
        super(Tile, self).__init__(position, file_name, config.DARK_GREEN)


class Hole(Tile):
    def __init__(self, position):
        super().__init__(position, f'hole{random.randint(0, 9)}.png')

    @staticmethod
    def kind():
        return 'h'


class Road(Tile):
    def __init__(self, position):
        super().__init__(position, 'road.png')

    @staticmethod
    def kind():
        return 'r'


class X(Tile):
    def __init__(self, position):
        super().__init__(position, 'x.png')

    @staticmethod
    def kind():
        return 'x'
