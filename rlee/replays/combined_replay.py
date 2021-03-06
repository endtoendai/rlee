"""
Combined Experience Replay.

A Deeper Look at Experience Replay
https://arxiv.org/abs/1712.01275
"""
import random
from collections import deque

import torch


class CombinedReplayBuffer:
    """
    Combined Experience Replay.

    A Deeper Look at Experience Replay
    https://arxiv.org/abs/1712.01275
    """

    def __init__(self, capacity: int) -> None:
        self.buffer: deque = deque(maxlen=capacity)  # noqa: E999

    def __len__(self) -> int:
        return len(self.buffer)

    def push(
        self,
        state: torch.Tensor,
        action: int,
        reward: torch.Tensor,
        next_state: torch.Tensor,
        done: torch.Tensor,
    ) -> None:
        """
        Add a new interaction / experience to the replay buffer.

        Parameters
        ----------
        state : torch.Tensor of torch.float32
            Has shape (1, L) (for feature-type states) or (1, C, H, W) (for
            image-type states).
        action : int
        reward : torch.Tensor of torch.float32
            Has shape (1, 1)
        next_state : torch.Tensor of torch.float32
            Has shape (1, L) (for feature-type states) or (1, C, H, W) (for
            image-type states).
        done : torch.Tensor of torch.float32
            Has shape (1, 1)

        """
        self.buffer.append(
            (state, torch.LongTensor([action]), reward, next_state, done)
        )

    def sample(self, batch_size: int) -> torch.Tensor:
        """
        Sample a batch from the replay buffer.

        This function does not check if the buffer is bigger than the
        `batch_size`.

        Parameters
        ----------
        batch_size : int
            Size of the output batch. Should be at most the current size of the
            buffer.

        Returns
        -------
        batch: tuple of torch.Tensor
            A tuple of batches: (state_batch, action_batch, reward_batch,
            next_state_batch, done_batch).

        """
        samples = random.sample(self.buffer, batch_size - 1)
        samples.append(self.buffer[-1])  # Add immediate experience
        state, action, reward, next_state, done = zip(*samples)

        return (
            torch.cat(state),
            torch.cat(action),
            torch.cat(reward),
            torch.cat(next_state),
            torch.cat(done),
        )
