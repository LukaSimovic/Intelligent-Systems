import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, position, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.row = None
        self.col = None
        self.place_to(position)

    def position(self):
        return self.row, self.col

    def place_to(self, position):
        self.row = position[0]
        self.col = position[1]
        self.rect.x = self.col * config.TILE_SIZE
        self.rect.y = self.row * config.TILE_SIZE

    @staticmethod
    def kind():
        pass
