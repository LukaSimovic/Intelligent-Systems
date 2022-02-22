import math

import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
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
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


def are_adjacent(row1, col1, row2, col2):
    if row1 == row2:
        if col2 - col1 == 1 or col2 - col1 == -1:
            return True
    elif col1 == col2:
        if row2 - row1 == 1 or row2 - row1 == -1:
            return True
    else:
        return False


class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        row = self.row
        col = self.col
        depth_list = [[row, col]]
        active_path = [[row, col]]
        sirina_mape = int(config.WIDTH / config.TILE_SIZE)
        visina_mape = int(config.HEIGHT / config.TILE_SIZE)
        while True:
            if col != goal[1] or row != goal[0]:
                depth_list.pop(0)
                sort_followers = [[-1, -1, 1001]]

                if row - 1 >= 0 and [row - 1, col] not in active_path:
                    cost = game_map[row - 1][col].cost()
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row - 1, col, cost])
                if col + 1 < sirina_mape and [row, col + 1] not in active_path:
                    cost = game_map[row][col + 1].cost()
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row, col + 1, cost])
                if row + 1 < visina_mape and [row + 1, col] not in active_path:
                    cost = game_map[row + 1][col].cost()
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row + 1, col, cost])
                if col - 1 >= 0 and [row, col - 1] not in active_path:
                    cost = game_map[row][col - 1].cost()
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row, col - 1, cost])

                if sort_followers[0][2] != 1001:
                    sort_followers.pop()
                    temp = 0
                    for follower in sort_followers:
                        depth_list.insert(temp, [follower[0], follower[1]])
                        temp += 1
                else:
                    while True:
                        last = active_path.pop()
                        ret = are_adjacent(depth_list[0][0], depth_list[0][1], last[0], last[1])
                        if ret:
                            active_path.append([last[0], last[1]])
                            break

                row, col = depth_list[0][0], depth_list[0][1]

            else:
                break
            active_path.append([row, col])

        for nood in active_path:
            path.append(game_map[nood[0]][nood[1]])
        return path


def neighbour_cost(row, col, active_path, game_map, sirina_mape, visina_mape):
    cost = 0
    cnt = 0
    if row - 1 >= 0 and [row - 1, col] not in active_path:  # severni sused
        cost += game_map[row - 1][col].cost()
        cnt += 1
    if col + 1 < sirina_mape and [row, col + 1] not in active_path:  # istocni sused
        cost += game_map[row][col + 1].cost()
        cnt += 1
    if row + 1 < visina_mape and [row + 1, col] not in active_path:  # juzni sused
        cost += game_map[row + 1][col].cost()
        cnt += 1
    if col - 1 >= 0 and [row, col - 1] not in active_path:  # zapadni sused
        cost += game_map[row][col - 1].cost()
        cnt += 1

    if cnt == 0:
        return 1001
    else:
        return cost / cnt


class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        row = self.row
        col = self.col
        # format b_l je : [   elem1:[ [r,c],[putanja do r,c] ]    ,   elem2:[ [r,c],[putanja do r,c] ]    ]
        breadth_list = [[[row, col], []]]
        active_path = [[row, col]]
        sirina_mape = int(config.WIDTH / config.TILE_SIZE)
        visina_mape = int(config.HEIGHT / config.TILE_SIZE)
        while True:
            if col != goal[1] or row != goal[0]:
                parent = breadth_list.pop(0)
                sort_followers = [[-1, -1, 1001]]

                if row - 1 >= 0 and [row - 1, col] not in active_path:
                    cost = neighbour_cost(row - 1, col, active_path, game_map, sirina_mape, visina_mape)
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row - 1, col, cost])
                if col + 1 < sirina_mape and [row, col + 1] not in active_path:
                    cost = neighbour_cost(row, col + 1, active_path, game_map, sirina_mape, visina_mape)
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row, col + 1, cost])
                if row + 1 < visina_mape and [row + 1, col] not in active_path:
                    cost = neighbour_cost(row + 1, col, active_path, game_map, sirina_mape, visina_mape)
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row + 1, col, cost])
                if col - 1 >= 0 and [row, col - 1] not in active_path:
                    cost = neighbour_cost(row, col - 1, active_path, game_map, sirina_mape, visina_mape)
                    new_position = 0
                    for follower in sort_followers:
                        if cost < follower[2]:
                            break
                        else:
                            new_position += 1
                    sort_followers.insert(new_position, [row, col - 1, cost])

                if sort_followers[0][2] != 1001:
                    sort_followers.pop()
                    list_of_previous = [[row, col]]
                    for nood in parent[1]:
                        list_of_previous.append(nood)
                    for follower in sort_followers:
                        breadth_list.append([[follower[0], follower[1]], list_of_previous])
                else:
                    active_path.pop()

                row, col = breadth_list[0][0][0], breadth_list[0][0][1]

            else:
                break
            active_path = []
            for n in breadth_list[0][1]:
                active_path.insert(0, n)
            active_path.append([row, col])

        for nood in active_path:
            path.append(game_map[nood[0]][nood[1]])
        return path


def put_into_sorted_list_bbs(path, cost, my_list):
    new_nood = [path, cost]
    new_position = 0
    should_put = True
    for follower in my_list:
        if cost < follower[1]:
            break
        else:
            # prvi if je dinamicko programiranje
            if cost > follower[1]:
                if path[len(path)-1][0] == follower[0][len(follower[0])-1][0] and path[len(path)-1][1] == follower[0][len(follower[0])-1][1]:
                    should_put = False
                    break
            if cost == follower[1] and len(path) < len(follower[0]):
                break
            new_position += 1

    if should_put:
        my_list.insert(new_position, new_nood)


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        row = self.row
        col = self.col
        # format b_l je : [  e1:[ [putanja], cena]  ,   e2:[[putanja], cena]  ]
        branch_and_bound_list = [[[[row, col]], 0]]
        active_path = [[row, col]]
        sirina_mape = int(config.WIDTH / config.TILE_SIZE)
        visina_mape = int(config.HEIGHT / config.TILE_SIZE)
        while True:
            if col != goal[1] or row != goal[0]:
                old_nood = branch_and_bound_list.pop(0)
                old_path = old_nood[0]
                old_cost = old_nood[1]

                if row - 1 >= 0 and [row - 1, col] not in active_path:
                    new_cost = old_cost + game_map[row - 1][col].cost()
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row-1, col])
                    put_into_sorted_list_bbs(new_path, new_cost, branch_and_bound_list)
                if col + 1 < sirina_mape and [row, col + 1] not in active_path:
                    new_cost = old_cost + game_map[row][col+1].cost()
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row, col+1])
                    put_into_sorted_list_bbs(new_path, new_cost, branch_and_bound_list)
                if row + 1 < visina_mape and [row + 1, col] not in active_path:
                    new_cost = old_cost + game_map[row + 1][col].cost()
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row + 1, col])
                    put_into_sorted_list_bbs(new_path, new_cost, branch_and_bound_list)
                if col - 1 >= 0 and [row, col - 1] not in active_path:
                    new_cost = old_cost + game_map[row][col-1].cost()
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row, col-1])
                    put_into_sorted_list_bbs(new_path, new_cost, branch_and_bound_list)

                temp_nood = branch_and_bound_list[0][0].pop()
                row, col = temp_nood[0], temp_nood[1]
                branch_and_bound_list[0][0].append([row, col])
            else:
                break

            active_path = []
            for tmp in branch_and_bound_list[0][0]:
                active_path.append(tmp)

        for nood in active_path:
            path.append(game_map[nood[0]][nood[1]])
        return path


def get_heuristic(row, col, goal):
    if goal[0] == row and goal[1] == col:
        return 0
    else:
        dist = math.sqrt((goal[0] - row)*(goal[0] - row) + (goal[1] - col)*(goal[1] - col))
        return float("{:.3f}".format(dist))


def put_into_sorted_list_a_star(path, cost, my_list):
    new_nood = [path, cost]
    new_position = 0
    for follower in my_list:
        if cost < follower[1]:
            break
        else:
            if cost == follower[1] and len(path) < len(follower[0]):
                break
            new_position += 1
    my_list.insert(new_position, new_nood)


class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        row = self.row
        col = self.col
        a_star_list = [[[[row, col]], 0]]
        active_path = [[row, col]]
        sirina_mape = int(config.WIDTH / config.TILE_SIZE)
        visina_mape = int(config.HEIGHT / config.TILE_SIZE)
        while True:
            if col != goal[1] or row != goal[0]:
                old_nood = a_star_list.pop(0)
                old_path = old_nood[0]
                old_cost = old_nood[1]

                if row - 1 >= 0 and [row - 1, col] not in active_path:
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row-1, col])
                    if len(new_path) >= 3:
                        new_cost = old_cost - get_heuristic(new_path[-2][0], new_path[-2][1], goal)
                        new_cost += game_map[row - 1][col].cost() + get_heuristic(row-1, col, goal)
                    else:
                        new_cost = old_cost + game_map[row - 1][col].cost() + get_heuristic(row-1, col, goal)
                    put_into_sorted_list_a_star(new_path, new_cost, a_star_list)
                if col + 1 < sirina_mape and [row, col + 1] not in active_path:
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row, col+1])
                    if len(new_path) >= 3:
                        new_cost = old_cost - get_heuristic(new_path[-2][0], new_path[-2][1], goal)
                        new_cost += game_map[row][col+1].cost() + get_heuristic(row, col+1, goal)
                    else:
                        new_cost = old_cost + game_map[row][col+1].cost() + get_heuristic(row, col+1, goal)
                    put_into_sorted_list_a_star(new_path, new_cost, a_star_list)
                if row + 1 < visina_mape and [row + 1, col] not in active_path:
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row + 1, col])
                    if len(new_path) >= 3:
                        new_cost = old_cost - get_heuristic(new_path[-2][0], new_path[-2][1], goal)
                        new_cost += game_map[row + 1][col].cost() + get_heuristic(row+1, col, goal)
                    else:
                        new_cost = old_cost + game_map[row + 1][col].cost() + get_heuristic(row+1, col, goal)
                    put_into_sorted_list_a_star(new_path, new_cost, a_star_list)
                if col - 1 >= 0 and [row, col - 1] not in active_path:
                    new_path = []
                    for tmp in old_path:
                        new_path.append(tmp)
                    new_path.append([row, col-1])
                    if len(new_path) >= 3:
                        new_cost = old_cost - get_heuristic(new_path[-2][0], new_path[-2][1], goal)
                        new_cost += game_map[row][col - 1].cost() + get_heuristic(row, col - 1, goal)
                    else:
                        new_cost = old_cost + game_map[row][col - 1].cost() + get_heuristic(row, col - 1, goal)
                    put_into_sorted_list_a_star(new_path, new_cost, a_star_list)

                temp_nood = a_star_list[0][0].pop()
                row, col = temp_nood[0], temp_nood[1]
                a_star_list[0][0].append([row, col])
            else:
                break

            active_path = []
            for tmp in a_star_list[0][0]:
                active_path.append(tmp)

        for nood in active_path:
            path.append(game_map[nood[0]][nood[1]])
        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
