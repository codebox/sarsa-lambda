from states_actions import StatesAndActions


class EligibilityTraces:
    def __init__(self, decay_rate):
        self.decay_rate = decay_rate
        self.values = StatesAndActions()

    def decay(self, state, action):
        self.values.update(state, action, lambda v: v * self.decay_rate)

    def increment(self, state, action):
        self.values.update(state, action, lambda v: v + 1, 1)

    def get(self, state, action):
        return self.values.get(state, action)
