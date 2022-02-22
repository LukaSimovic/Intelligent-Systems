import copy

from actions import Action
from tiles import Hole


class GameState:
    initial_state = None

    def __init__(self, char_map, agents, last_agent_played_id):
        self.char_map = char_map
        self.agents = agents
        self.last_agent_played_id = last_agent_played_id
        self.win = False
        self.loss = False

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.char_map])

    def adjust_win_loss(self):
        actions_len = [len(self.get_legal_actions(agent_id)) for agent_id in range(len(self.agents))]
        if not any(actions_len[1:]) and actions_len[0]:
            self.win = True
        elif not actions_len[0] and any(actions_len[1:]):
            self.loss = True
        elif not any(actions_len):
            self.loss = True if self.last_agent_played_id is not None and self.last_agent_played_id != 0 else False
            self.win = True if self.last_agent_played_id is not None and self.last_agent_played_id == 0 else False

    def copy(self):
        char_map_copy = copy.deepcopy(self.char_map)
        agents_copy = [a.copy() for a in self.agents]
        last_agent_played_id = self.last_agent_played_id
        return GameState(char_map_copy, agents_copy, last_agent_played_id)

    def is_win(self):
        return self.win

    def is_loss(self):
        return self.loss

    def is_position_legal(self, position, agent):
        row, col = position
        return 0 <= row < len(self.char_map) and \
            0 <= col < len(self.char_map[0]) and \
            self.char_map[row][col] in agent.legal_fields() or position == agent.position()

    def get_legal_actions(self, agent_id):
        agent = self.agents[agent_id]
        if not agent.is_active():
            return []
        agent_pos = agent.position()
        actions = []
        for act_name, act_dir in Action.actions.items():
            new_agent_pos = tuple(map(sum, zip(agent_pos, act_dir)))
            if self.is_position_legal(new_agent_pos, agent):
                actions.append(act_name)
        return actions

    def apply_action(self, agent_id, action):
        state = self.copy()
        if action not in Action.actions.keys():
            raise Exception(f'ERR: {action} is not a legal action names! '
                            f'Legal names are ({", ".join(n for n in Action.actions.keys())})')
        agent = state.agents[agent_id]
        old_agent_pos = agent.position()
        new_agent_pos = tuple(map(sum, zip(old_agent_pos, Action.actions[action])))
        if not self.is_position_legal(new_agent_pos, agent):
            raise Exception(f'ERR: {action} is not legal! '
                            f'Agent position: {old_agent_pos}')
        state.char_map[old_agent_pos[0]][old_agent_pos[1]] = Hole.kind()
        state.char_map[new_agent_pos[0]][new_agent_pos[1]] = agent.kind()
        agent.apply_action(action)
        state.last_agent_played_id = agent_id
        return state
