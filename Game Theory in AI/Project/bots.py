import random

from agents import Agent
from students import MinimaxABAgent, MaxNAgent


class BotAgent(Agent):
    agent_names = {'1': 'Aki', '2': 'Jocke', '3': 'Draza', '4': 'Bole'}
    ID = 0

    def __init__(self, position, file_name):
        super(BotAgent, self).__init__(position, file_name)
        BotAgent.ID += 1
        self.id = BotAgent.ID


class Aki(BotAgent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)

    @staticmethod
    def kind():
        return '1'

    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)
        states_list = [state.apply_action(self.id, act) for act in actions]
        coll = list(zip(actions, states_list))
        if len(coll):
            coll = sorted(coll, key=lambda st: sum(tuple(map(lambda i, j: abs(i - j),
                          st[1].agents[0].position(), st[1].agents[self.id].position()))))
            return coll[0][0]
        return None


class Jocke(BotAgent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)

    @staticmethod
    def kind():
        return '2'

    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)
        return actions[random.randint(0, len(actions) - 1)]


class Draza(BotAgent, MinimaxABAgent):
    def __init__(self, position, file_name):
        MinimaxABAgent.__init__(self, position, file_name)
        BotAgent.__init__(self, position, file_name)

    @staticmethod
    def kind():
        return '3'

    def get_next_action(self, state, max_levels):
        return MinimaxABAgent.get_next_action(self, state, max_levels)


class Bole(BotAgent, MaxNAgent):
    def __init__(self, position, file_name):
        MaxNAgent.__init__(self, position, file_name)
        BotAgent.__init__(self, position, file_name)

    @staticmethod
    def kind():
        return '4'

    def get_next_action(self, state, max_levels):
        return MaxNAgent.get_next_action(self, state, max_levels)
