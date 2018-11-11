import re, random

ACTION_UP    = 'U'
ACTION_RIGHT = 'R'
ACTION_DOWN  = 'D'
ACTION_LEFT  = 'L'

ACTIONS = (ACTION_UP, ACTION_RIGHT, ACTION_DOWN, ACTION_LEFT)

STATE_ACTOR   = '웃'
STATE_EXIT    = 'X'
STATE_BLOCK   = '█'
STATE_MONSTER = 'M'
STATE_EMPTY   = '.'

REWARD_MOVEMENT = -1
REWARD_BAD_MOVE = -5
REWARD_MONSTER  = -100
REWARD_EXIT     = 100

MONSTER_RANDOMNESS = 0.2

class Environment:
    actions = ACTIONS

    def __init__(self, grid_text):
        self.grid   = self.__parse_grid_text(grid_text)
        self.height = len(self.grid)
        self.width  = len(self.grid[0])
        self.actor_in_terminal_state = False
        self.monsters = []

        for y in range(self.height):
            for x in range(self.width):
                content = self.grid[y][x]

                if content == STATE_ACTOR:
                    self.actor_x = x
                    self.actor_y = y

                elif content == STATE_MONSTER:
                    self.monsters.append(Position(x, y))

    def __parse_grid_text(self, grid_text):
        rows = re.split("\s*\n\s*", grid_text.strip())
        return list(map(lambda row:row.split(' '), rows))

    def get_actor_state(self):
        return '{},{}'.format(self.actor_x, self.actor_y)

    def get(self):
        return self.grid

    def __get_valid_monster_moves(self, current_x, current_y):
        compass_directions = [
            Position(current_x + 1, current_y),
            Position(current_x - 1, current_y),
            Position(current_x, current_y + 1),
            Position(current_x, current_y - 1)
        ]

        def on_grid(pos):
            return (0 <= pos.x < self.width) and (0 <= pos.y < self.height)

        def can_move(pos):
            return self.grid[pos.y][pos.x] in [STATE_EMPTY, STATE_ACTOR]

        possible_moves = list(filter(lambda pos: on_grid(pos) and can_move(pos), compass_directions))

        possible_moves.sort(key=lambda pos: (pos.x - self.actor_x) ** 2 + (pos.y - self.actor_y) ** 2)

        return possible_moves

    def __move_monsters(self):
        for monster_position in self.monsters:
            current_x = monster_position.x
            current_y = monster_position.y

            valid_moves = self.__get_valid_monster_moves(current_x, current_y)

            if len(valid_moves):
                move_randomly = random.random() < MONSTER_RANDOMNESS
                if move_randomly:
                    new_pos = random.choice(valid_moves)
                else:
                    new_pos = valid_moves[0]

                self.grid[current_y][current_x] = STATE_EMPTY
                self.grid[new_pos.y][new_pos.x] = STATE_MONSTER

                monster_position.x = new_pos.x
                monster_position.y = new_pos.y

                if new_pos.x == self.actor_x and new_pos.y == self.actor_y:
                    self.actor_in_terminal_state = True

    def __update_environment(self):
        self.__move_monsters()

    def perform_action(self, action):
        reward = 0

        actor_requested_x = None
        actor_requested_y = None

        if action == ACTION_UP:
            actor_requested_x = self.actor_x
            actor_requested_y = self.actor_y + 1

        elif action == ACTION_RIGHT:
            actor_requested_x = self.actor_x + 1
            actor_requested_y = self.actor_y

        elif action == ACTION_DOWN:
            actor_requested_x = self.actor_x
            actor_requested_y = self.actor_y - 1

        elif action == ACTION_LEFT:
            actor_requested_x = self.actor_x - 1
            actor_requested_y = self.actor_y

        else:
            assert False, 'action=' + str(action)

        if actor_requested_x < 0 or actor_requested_x >= self.width or actor_requested_y < 0 or actor_requested_y >= self.height:
            requested_location_contents = STATE_BLOCK
        else:
            requested_location_contents = self.grid[actor_requested_y][actor_requested_x]

        def move_actor_to_requested_location():
            self.grid[self.actor_y][self.actor_x] = STATE_EMPTY
            self.actor_x = actor_requested_x
            self.actor_y = actor_requested_y
            self.grid[self.actor_y][self.actor_x] = STATE_ACTOR

        if requested_location_contents == STATE_BLOCK:
            reward += REWARD_BAD_MOVE

        elif requested_location_contents == STATE_EMPTY:
            reward += REWARD_MOVEMENT
            move_actor_to_requested_location()

        elif requested_location_contents == STATE_EXIT:
            reward += REWARD_MOVEMENT + REWARD_EXIT
            move_actor_to_requested_location()
            self.actor_in_terminal_state = True

        elif requested_location_contents == STATE_MONSTER:
            reward += REWARD_MOVEMENT + REWARD_MONSTER
            move_actor_to_requested_location()
            self.actor_in_terminal_state = True

        else:
            assert False, 'requested_location_contents=' + str(requested_location_contents)

        self.__update_environment()

        return reward


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y