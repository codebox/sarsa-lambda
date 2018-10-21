import signal, sys

from environment import Environment
from strategy import Strategy

EPISODE_COUNT=1000 * 1000
SAVE_INTERVAL=1000
MAX_EPISODE_STEPS=10000
ENVIRONMENT_HEIGHT=10
ENVIRONMENT_WIDTH=10
SAVE_FILE='sarsa.json'


def build_environment():
    environment = Environment(ENVIRONMENT_WIDTH, ENVIRONMENT_HEIGHT)
    environment.initialise()
    return environment


def build_strategy():
    return Strategy()


def load_from_file(strategy):
    pass # TODO


def save_to_file(strategy):
    pass # TODO


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
        next_action = strategy.next_action(state_after)

        strategy.update(state_before, action, reward, state_after, next_action)
        total_reward += reward
        steps += 1

    return steps, total_reward


def save_and_exit():
    save_to_file(strategy)
    sys.exit(0)

signal.signal(signal.SIGINT, save_and_exit) # handle ctrl-c

strategy = build_strategy()
load_from_file(strategy)

for episode_index in range(EPISODE_COUNT):
    run_episode(strategy)
    if episode_index % SAVE_INTERVAL == 0:
        save_to_file(strategy)

save_to_file(strategy)