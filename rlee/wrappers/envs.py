"""OpenAI Gym Environment wrappers."""
from typing import Any

import gym

from .atari_wrappers import make_atari, wrap_deepmind
from .torch_wrappers import wrap_pytorch


def make_env(env_id: str) -> Any:
    """
    Return an OpenAI Gym environment wrapped with appropriately.

    Throws error if unrecognized env_id is given.

    Parameters
    ----------
    env_id : str
        OpenAI Gym ID for environment.

    Returns
    -------
    env
        Wrapped OpenAI Gym environment.

    """
    if env_id in ["Acrobot", "CartPole", "MountainCar", "LunarLander"]:
        # Create environment
        if env_id in ["LunarLander"]:
            env_id = env_id + "-v2"
        elif env_id in ["Acrobot", "CartPole"]:
            env_id = env_id + "-v1"
        else:
            env_id = env_id + "-v0"
        env = gym.make(env_id)  # Don't use Frameskip, NoopReset

        # NOTE The 3 lines below make classic control environments into
        # a DeepMind-style environment with visual inputs
        # env = ClassicControlWrapper(env)
        # env = WarpFrame(env)
        # env = FrameStack(env, 4)

        # Wrap environment for PyTorch agents
        env = wrap_pytorch(env, visual=False)

    elif env_id in ["Pong"]:
        # Create environment
        env_id = env_id + "NoFrameskip-v4"
        env = make_atari(env_id)

        # Wrap environment to fit DeepMind-style environment
        env = wrap_deepmind(env, frame_stack=True)

        # Wrap environment for PyTorch agents
        env = wrap_pytorch(env)
    else:
        raise ValueError("{} is not a supported environment.".format(env_id))

    return env
