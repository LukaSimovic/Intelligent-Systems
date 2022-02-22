import copy

import config

from actions import Action
from sprites import BaseSprite
from tiles import Road


class Agent(BaseSprite):
    def __init__(self, position, file_name):
        super(Agent, self).__init__(position, file_name, config.DARK_GREEN)
        self.last_action = None
        self.id = None
        self.active = True

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def copy(self):
        agent_copy = copy.copy(self)
        agent_copy.rect = self.image.get_rect()
        agent_copy.place_to(self.position())
        return agent_copy

    def move_towards(self, position):
        row = position[0] - self.row
        col = position[1] - self.col
        self.rect.x += col
        self.rect.y += row

    def is_in_tile(self):
        return not self.rect.x % config.TILE_SIZE and not self.rect.y % config.TILE_SIZE

    def get_legal_actions(self, state):
        return state.get_legal_actions(self.id)

    def get_last_action(self):
        return self.last_action

    def apply_action(self, action):
        self.last_action = action
        self.place_to(tuple(map(sum, zip(self.position(), Action.actions[action]))))

    @staticmethod
    def legal_fields():
        return {Road.kind()}

    def get_next_action(self, state, max_levels):
        pass
