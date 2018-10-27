# -*- coding: utf-8 -*-

from random import random, choice
from states_actions import StatesAndActions


class QValues:
    def __init__(self, all_actions):
        self.all_actions = all_actions
        self.values = StatesAndActions()

    def get_expected_reward(self, state, action):
        return self.values.get(state, action)

    def set_expected_reward(self, state, action, reward):
        self.values.set(state, action, reward)

    def ensure_exists(self, state, action):
        if not self.values.has(state, action):
            self.values.set(state, action)

    def get_greedy_action(self, state, ε=0):
        if random() < ε:
            actions = self.all_actions

        else:
            actions_for_state = self.values.get_all_for_state(state, self.all_actions)
            max_val = max(actions_for_state.values())
            actions = [action for action, value in actions_for_state.items() if value == max_val]

        return choice(actions)

    def set_all_values(self, values):
        self.values.set_all(values)

    def get_all_values(self):
        return self.values.get_all()

    def for_each(self, fn):
        self.values.for_each(fn)