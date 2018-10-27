import copy

DEFAULT_VALUE = 0


class StatesAndActions:
    def __init__(self):
        self.values = {}

    def get(self, state, action):
        if state in self.values:
            return self.values[state].get(action, DEFAULT_VALUE)

        return DEFAULT_VALUE

    def get_all_for_state(self, state, all_states):
        return {action: self.get(state, action) for action in all_states}

    def get_all(self):
        return copy.deepcopy(self.values)

    def set_all(self, values):
        self.values = copy.deepcopy(values)

    def set(self, state, action, value=DEFAULT_VALUE):
        if state not in self.values:
            self.values[state] = {}

        self.values[state][action] = value

    def has(self, state, action):
        return state in self.values and action in self.values[state]

    def update(self, state, action, update_fn, value_to_set=None):
        if self.has(state, action):
            old_value = self.get(state, action)
            new_value = update_fn(old_value)
            self.set(state, action, new_value)

        elif value_to_set is not None:
            self.set(state, action, value_to_set)

    def for_each(self, fn):
        for state, actions in self.values.items():
            for action in actions:
                fn(state, action)