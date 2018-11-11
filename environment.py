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
                    self.actor_pos = Position(x, y)

                elif content == STATE_MONSTER:
                    self.monsters.append(Position(x, y))

    def __parse_grid_text(self, grid_text):
        rows = re.split("\s*\n\s*", grid_text.strip())
        return list(map(lambda row:row.split(' '), rows))

    def get_actor_state(self):
        return str(self.actor_pos)

    def get(self):
        return self.grid

    def __position_on_grid(self, pos):
        return (0 <= pos.x < self.width) and (0 <= pos.y < self.height)

    def __get_valid_monster_moves(self, current_x, current_y):
        compass_directions = [
            Position(current_x + 1, current_y),
            Position(current_x - 1, current_y),
            Position(current_x, current_y + 1),
            Position(current_x, current_y - 1)
        ]

        def can_move(pos):
            return self.grid[pos.y][pos.x] in [STATE_EMPTY, STATE_ACTOR]

        possible_moves = list(filter(lambda pos: self.__position_on_grid(pos) and can_move(pos), compass_directions))

        possible_moves.sort(key=lambda pos: pos.dist_sq(self.actor_pos))

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

                if new_pos == self.actor_pos:
                    self.actor_in_terminal_state = True

    def __update_environment(self):
        self.__move_monsters()

    def perform_action(self, action):
        reward = 0

        actor_requested_pos = self.actor_pos.copy()

        if action == ACTION_UP:
            actor_requested_pos.up()

        elif action == ACTION_RIGHT:
            actor_requested_pos.right()

        elif action == ACTION_DOWN:
            actor_requested_pos.down()

        elif action == ACTION_LEFT:
            actor_requested_pos.left()

        else:
            assert False, 'action=' + str(action)

        if self.__position_on_grid(actor_requested_pos):
            requested_location_contents = self.grid[actor_requested_pos.y][actor_requested_pos.x]
        else:
            requested_location_contents = STATE_BLOCK

        def move_actor_to_requested_location():
            self.grid[self.actor_pos.y][self.actor_pos.x] = STATE_EMPTY
            self.actor_pos = actor_requested_pos
            self.grid[self.actor_pos.y][self.actor_pos.x] = STATE_ACTOR

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

    def dist_sq(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def copy(self):
        return Position(self.x, self.y)

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '{},{}'.format(self.x, self.y)