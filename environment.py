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

class Environment:
    actions = ACTIONS

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.actor_in_terminal_state = False

    def initialise(self):
        self._grid = []

        for y in range(self.height):
            row = []
            self._grid.append(row)
            for x in range(self.width):
                content = self._get_initial_content(x, y)

                if content == STATE_ACTOR:
                    self.actor_x = x
                    self.actor_y = y

                row.append(content)


    def get_actor_state(self):
        return '{},{}'.format(self.actor_x, self.actor_y)


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
            requested_location_contents = self._grid[actor_requested_x][actor_requested_y]

        def move_actor_to_requested_location():
            self._grid[self.actor_x][self.actor_y] = STATE_EMPTY
            self.actor_x = actor_requested_x
            self.actor_y = actor_requested_y
            self._grid[self.actor_x][self.actor_y] = STATE_ACTOR

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

        return reward

    def _get_initial_content(self, x, y):
        return [
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. X . . 웃 . . M . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .',
            '. . . . . . . . . .'
        ][y].split(' ')[x]
