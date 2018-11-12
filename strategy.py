# -*- coding: utf-8 -*-

from eligibility_traces import EligibilityTraces
from q_values import QValues


class Strategy:
    def __init__(self, γ, α, λ, ε, ε_decay, actions):
        self.γ = γ
        self.α = α
        self.λ = λ
        self.ε = ε
        self.ε_decay = ε_decay
        self.actions = actions
        self.eligibility_traces = None
        self.q_values = QValues(actions)
        self.scores = [] # TODO
        self.episode = 0
        self.episode_reward = 0
        self.episode_reward_total = 0 # TODO

    def new_episode(self):
        self.eligibility_traces = EligibilityTraces(1 - self.γ * self.λ)
        self.ε *= self.ε_decay
        self.episode += 1
        self.episode_reward = 0

    def next_action(self, state, ε=None):
        return self.q_values.get_greedy_action(state, self.ε if ε is None else ε)

    def update(self, state_before, action, reward, state_after):
        expected_reward = self.q_values.get_expected_reward(state_before, action)
        next_action = self.q_values.get_greedy_action(state_after, self.ε)
        next_expected_reward = self.q_values.get_expected_reward(state_after, next_action)

        td_error = reward - expected_reward + self.γ * next_expected_reward

        self.eligibility_traces.increment(state_before, action)
        self.q_values.ensure_exists(state_before, action)

        def update_q_values(state, action):
            old_expected_reward = self.q_values.get_expected_reward(state, action)
            new_expected_reward = old_expected_reward + self.α * td_error * self.eligibility_traces.get(state, action)
            self.q_values.set_expected_reward(state, action, new_expected_reward)
            self.eligibility_traces.decay(state, action)

        self.q_values.for_each(update_q_values)
        self.episode_reward += reward

    def load(self, values):
        self.q_values.set_all_values(values['q'])
        self.ε = values['ε']
        self.scores = values['scores']
        self.episode = values['episode']

    def dump(self):
        return {
            'q' : self.q_values.get_all_values(),
            'ε' : self.ε,
            'scores' : self.scores,
            'episode' : self.episode
        }