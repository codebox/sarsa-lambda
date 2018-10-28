# -*- coding: utf-8 -*-

import signal, sys, json

from environment import Environment
from strategy import Strategy

EPISODE_COUNT=1000 * 1000
SAVE_INTERVAL=1000
MAX_EPISODE_STEPS=10000
ENVIRONMENT_HEIGHT=10
ENVIRONMENT_WIDTH=10
SAVE_FILE='sarsa.json'

INIT_ENVIRONMENT="""
    . . . . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    . . M . . . . . . .
    . X M . 웃 . . M . .
    . M M . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
"""

def build_environment():
    return Environment(INIT_ENVIRONMENT)

def build_strategy():
    γ = 0.99
    α = 0.1
    λ = 0.1
    ε = 0.1
    return Strategy(γ, α, λ, ε, Environment.actions)


def load_from_file(strategy):
    try:
        with open(SAVE_FILE) as f:
            strategy.load(json.load(f))

        print('Loaded', SAVE_FILE)

    except:
        pass

def save_to_file(strategy):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(strategy.dump(), f)

        # print('Saved', SAVE_FILE)

    except:
        pass


def run_episode(strategy):
    environment = build_environment()
    steps = 0
    total_reward = 0

    strategy.new_episode()

    while not environment.actor_in_terminal_state and steps < MAX_EPISODE_STEPS:
        state_before = environment.get_actor_state()
        action = strategy.next_action(state_before)
        reward = environment.perform_action(action)
        state_after = environment.get_actor_state()
        strategy.update(state_before, action, reward, state_after)
        total_reward += reward
        steps += 1

    return steps, total_reward


def save_and_exit(_1,_2):
    save_to_file(strategy)
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, save_and_exit) # handle ctrl-c

    strategy = build_strategy()
    load_from_file(strategy)

    for episode_index in range(EPISODE_COUNT):
        run_episode(strategy)
        if episode_index > 0 and episode_index % SAVE_INTERVAL == 0:
            save_to_file(strategy)
            print(episode_index)

    save_to_file(strategy)

