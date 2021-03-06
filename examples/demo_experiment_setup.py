"""
Running this script will:
*  Execute the experiments
*  Save a config.json file in the folder dev/demo_experiment, with the parameters used
"""

import rlberry.seeding as seeding
from rlberry.agents import PPOAgent, A2CAgent
from rlberry.envs.benchmarks.ball_exploration.ball2d import get_benchmark_env
from rlberry.stats import AgentStats, compare_policies, plot_episode_rewards
from sacred import Experiment
from sacred.observers import FileStorageObserver

# Create experiment
ex = Experiment('demo_ppo_vs_a2c')

# Create output folder to store configs
fs_observer = FileStorageObserver.create("dev/demo_experiment")
ex.observers.append(fs_observer)


@ex.config
def cfg():
    """
    Defines experiment parameters, using the Sacred library.
    See Sacred documentation at https://sacred.readthedocs.io/en/stable/
    """
    params = {}
    params['ppo'] = {
                    "n_episodes": 100,
                    "gamma": 0.99,
                    "horizon": 50,
                    "learning_rate": 0.0003
                    }

    params['a2c'] = {
                    "n_episodes": 100,
                    "gamma": 0.99,
                    "horizon": 50,
                    "learning_rate": 0.0003
                    }

    optimize_hyperparams = True


@ex.automain
def run_experiment(params,
                   optimize_hyperparams):
    """
    Main experiment function
    """   
    # Choose environment
    env = get_benchmark_env(level=1)

    # Initialize AgentStats
    stats = {}
    stats['ppo'] = AgentStats(PPOAgent,
                              env,
                              init_kwargs=params['ppo'],
                              eval_horizon=params['ppo']['horizon'],
                              n_fit=2)

    stats['a2c'] = AgentStats(A2CAgent,
                              env,
                              init_kwargs=params['a2c'],
                              eval_horizon=params['a2c']['horizon'],
                              n_fit=2)

    agent_stats_list = stats.values()

    # Optimize hyperparams
    if optimize_hyperparams:
        for stats in agent_stats_list:
            # timeout after 20 seconds
            stats.optimize_hyperparams(n_trials=50, timeout=10)

    # learning curves
    plot_episode_rewards(agent_stats_list, cumulative=True, show=False)

    # compare final policies
    output = compare_policies(agent_stats_list, n_sim=10)
    print(output)
