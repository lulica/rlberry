import pytest
from rlberry.agents.kernel_based import RSKernelUCBVIAgent
from rlberry.agents.kernel_based import RSUCBVIAgent
from rlberry.envs.benchmarks.ball_exploration.ball2d import get_benchmark_env


@pytest.mark.parametrize("kernel_type", [
                "uniform",
                "triangular",
                "gaussian",
                "epanechnikov",
                "quartic",
                "triweight",
                "tricube",
                "cosine"
])
def test_rs_kernel_ucbvi(kernel_type):
    for horizon in [None, 30]:
        env = get_benchmark_env(level=1)
        agent = RSKernelUCBVIAgent(
                                env,
                                n_episodes=5,
                                gamma=0.95,
                                horizon=horizon,
                                bonus_scale_factor=0.01,
                                min_dist=0.2,
                                bandwidth=0.05,
                                beta=1.0,
                                kernel_type=kernel_type)
        agent._log_interval = 0
        agent.fit()
        agent.policy(env.observation_space.sample())


def test_rs_ucbvi():
    env = get_benchmark_env(level=1)
    agent = RSUCBVIAgent(env,
                         n_episodes=5,
                         gamma=0.99,
                         horizon=30,
                         bonus_scale_factor=0.1)
    agent._log_interval = 0
    agent.fit()
    agent.policy(env.observation_space.sample())
