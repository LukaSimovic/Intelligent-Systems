import math
import random

from agents import Agent


# Example agent, behaves randomly.
# ONLY StudentAgent and his descendants have a 0 id. ONLY one agent of this type must be present in a game.
# Agents from bots.py have successive ids in a range from 1 to number_of_bots.
class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0

    @staticmethod
    def kind():
        return '0'

    # Student shall override this method in derived classes.
    # This method should return one of the legal actions (from the Actions class) for the current state.
    # state - represents a state object.
    # max_levels - maximum depth in a tree search. If max_levels eq -1 than the tree search depth is unlimited.
    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)  # equivalent of state.get_legal_actions(self.id)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        # Example of a new_state creation (for a chosen_action of a self.id agent):
        # new_state = state.apply_action(self.id, chosen_action)
        return chosen_action

    def estimation_func(self, state, player_max, player_min_id):
        player_min = state.agents[player_min_id]
        ret = [0, self.last_action]
        best_res = -math.inf
        if player_max == 1:
            actions = self.get_legal_actions(state)

            for a in actions:
                agent_copy = self.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(self.get_id(), a)
                new_actions = self.get_legal_actions(state_next)
                player_min_actions = player_min.get_legal_actions(state_next)
                # print("MAX", len(new_actions), len(player_min_actions))
                new_res = len(new_actions) - len(player_min_actions)
                if new_res > best_res:
                    best_res = new_res
                    ret = [best_res, a]
            if best_res > 0:
                ret[0] = 1
            else:
                ret[0] = -1
        else:
            actions = player_min.get_legal_actions(state)
            for a in actions:
                agent_copy = player_min.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(player_min.get_id(), a)
                new_actions = player_min.get_legal_actions(state_next)
                player_max_actions = self.get_legal_actions(state_next)
                new_res = len(new_actions) - len(player_max_actions)
                if new_res > best_res:
                    best_res = new_res
                    ret = [best_res, a]
            if best_res > 0:
                ret[0] = -1
            else:
                ret[0] = 1
        return ret


class MinimaxAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        ret = self.minimax(state, max_levels, 1, 0)
        return ret[1]

    def minimax(self, state, max_levels, player_max, curr_level):
        best = []
        if player_max == 1:
            actions = self.get_legal_actions(state)

            if not actions:
                player_min = state.agents[1]
                return [-1, player_min.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 1, 1)

            best = [-math.inf, self.last_action]
            for a in actions:
                agent_copy = self.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(self.get_id(), a)
                a_ret = self.minimax(state_next, max_levels, 0, curr_level + 1)
                if a_ret[0] > best[0]:
                    best = [a_ret[0], a]
        else:
            player_min = state.agents[1]
            actions = player_min.get_legal_actions(state)

            if not actions:
                return [1, self.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 0, 1)

            best = [math.inf, player_min.last_action]
            for a in actions:
                agent_copy = player_min.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(player_min.get_id(), a)
                a_ret = self.minimax(state_next, max_levels, 1, curr_level + 1)
                if a_ret[0] < best[0]:
                    best = [a_ret[0], a]
        return best


class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        agents = state.agents
        if self.id != 0:
            player_min = agents[0]
        else:
            player_min = agents[1]
        ret = self.minimax_ab(state, max_levels, 1, 0, math.inf, -math.inf, player_min.get_id())
        return ret[1]

    def minimax_ab(self, state, max_levels, player_max, curr_level, alpha, beta, player_min_id):
        best = []
        if player_max == 1:
            actions = self.get_legal_actions(state)

            if not actions:
                player_min = state.agents[player_min_id]
                return [-1, player_min.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 1, player_min_id)

            best = [-math.inf, self.last_action]
            for a in actions:
                agent_copy = self.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(self.get_id(), a)
                a_ret = self.minimax_ab(state_next, max_levels, 0, curr_level + 1, alpha, beta, player_min_id)
                if a_ret[0] > best[0]:
                    best = [a_ret[0], a]
                alpha = max(alpha, best[0])
                if alpha >= beta:
                    break
        else:
            player_min = state.agents[player_min_id]
            actions = player_min.get_legal_actions(state)

            if not actions:
                return [1, self.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 0, player_min_id)

            best = [math.inf, player_min.last_action]
            for a in actions:
                agent_copy = player_min.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(player_min.get_id(), a)
                a_ret = self.minimax_ab(state_next, max_levels, 1, curr_level + 1, alpha, beta, player_min_id)
                if a_ret[0] < best[0]:
                    best = [a_ret[0], a]
                beta = min(beta, best[0])
                if alpha >= beta:
                    break
        return best


class ExpectAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        ret = self.expectimax(state, max_levels, 1, 0)
        return ret[1]

    def expectimax(self, state, max_levels, player_max, curr_level):
        best = []
        if player_max == 1:
            actions = self.get_legal_actions(state)

            if not actions:
                player_chance = state.agents[1]
                return [-1, player_chance.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 1, 1)

            best = [-math.inf, self.last_action]
            for a in actions:
                agent_copy = self.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(self.get_id(), a)
                a_ret = self.expectimax(state_next, max_levels, 0, curr_level + 1)
                if a_ret[0] > best[0]:
                    best = [a_ret[0], a]
            # print("MAX: ", best[0], best[1], curr_level)
        else:
            player_chance = state.agents[1]
            actions = player_chance.get_legal_actions(state)

            if not actions:
                return [1, self.last_action]

            if max_levels == curr_level:
                return self.estimation_func(state, 0, 1)

            best = [0, player_chance.last_action]
            for a in actions:
                agent_copy = player_chance.copy()
                agent_copy.apply_action(a)
                state_next = state.apply_action(player_chance.get_id(), a)
                a_ret = self.expectimax(state_next, max_levels, 1, curr_level + 1)
                best[0] += a_ret[0]
            best[0] = best[0] * 1.0 / len(actions)
            best[1] = actions[random.randint(0, len(actions) - 1)]
            # print("Chance: ", best[0], best[1], curr_level)
        return best


class MaxNAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        result = []
        for ag in state.agents:
            if ag.is_active():
                result.append(-1)
            else:
                result.append(0)
        ret = self.minimax_n_players(state, max_levels, 0, result)
        return ret[1]

    def estimation_n_func(self, state, myid):
        agent = state.agents[myid]
        actions = agent.get_legal_actions(state)
        best_dif = -math.inf
        ret = []
        for a in actions:
            other_actions_cnt = 0
            best_player_ind = -1
            agent_copy = self.copy()
            agent_copy.apply_action(a)
            state_next = state.apply_action(agent.get_id(), a)
            new_actions = agent.get_legal_actions(state_next)
            most_actions = len(new_actions)
            for ag in state.agents:
                if ag.get_id() != agent.get_id():
                    other_actions = ag.get_legal_actions(state_next)
                    other_actions_cnt += len(other_actions)
                    if len(other_actions) > most_actions:
                        most_actions = len(other_actions)
                        best_player_ind = ag.get_id()
            dif = len(new_actions) - other_actions_cnt
            # print("ag", myid, ", ", a, ": ", len(new_actions), " - ", other_actions_cnt)
            if dif > best_dif:
                best_dif = dif
                score = []
                for ag in state.agents:
                    if ag.get_id() == best_player_ind:
                        score.append(1)
                    else:
                        score.append(0)
                ret = [score, a]
        return ret

    def minimax_n_players(self, state, max_levels, curr_level, result):
        best = []
        agents = state.agents
        if state.last_agent_played_id is None:
            last_played_agent_id = len(agents) - 1
        else:
            last_played_agent_id = state.last_agent_played_id
        agent = agents[(last_played_agent_id + 1) % len(agents)]
        while not agent.is_active():
            agent = agents[(agent.id + 1) % len(agents)]
        # print("Ja agent ", agent.get_id(), ", cur result:", result, ", cur level: ", curr_level)
        if result[agent.get_id()] == 0:
            state.last_agent_played_id = agent.get_id()
            return self.minimax_n_players(state, max_levels, curr_level + 1, result)

        actions = state.get_legal_actions(agent.id)
        # print("Possible actions:", actions, ", Agent: ", agent.get_id(), ", Level: ", curr_level, ", Result: ", result)
        myresult = []
        for r in result:
            myresult.append(r)
        best.append(myresult)
        best.append(None)
        if len(actions) == 0:
            best[0][agent.get_id()] = 0
            active_players_cnt = 0
            i = 0
            ind_active = -1
            for t in best[0]:
                if t != 0:
                    active_players_cnt += 1
                    ind_active = i
                i += 1
            # print("Result: ", myresult)
            if active_players_cnt == 1:
                win_agent = agents[ind_active]
                best[0][ind_active] = 1
                best[1] = win_agent.last_action
                # print("Pobedio agent ", win_agent.get_id(), ", Best: ", best, curr_level)
                return best
            else:
                state.last_agent_played_id = agent.get_id()
                return self.minimax_n_players(state, max_levels, curr_level + 1, best[0])

        if curr_level == max_levels:
            return self.estimation_n_func(state, agent.get_id())

        for a in actions:
            agent_copy = agent.copy()
            agent_copy.apply_action(a)
            state_next = state.apply_action(agent.get_id(), a)
            a_ret = self.minimax_n_players(state_next, max_levels, curr_level+1, result)
            if a_ret[0][agent.get_id()] > best[0][agent.get_id()]:
                best = [a_ret[0], a]
        # print("Agent ", agent.get_id(), ", Best:", best, ", cur level: ", curr_level)
        return best
