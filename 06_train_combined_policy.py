from rl_toolbox import Runner
from rl_toolbox.agent import PPOAgent
from rl_toolbox.policy import VisualMemoryPolicy


def main():
    runner = Runner(
        'CarRacing-v0',
        PPOAgent,
        VisualMemoryPolicy,
        save=True,
        load=True,
        weight_path='./weights/')

    runner.run(num_episode=1000)


if __name__ == '__main__':
    main()
