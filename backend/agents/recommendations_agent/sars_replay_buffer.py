# Author: Vodohleb04
from typing import Tuple
import torch
from torch import nn
import numpy as np


class SARSReplayBuffer(nn.Module):
    """Buffer to save SARS records (check https://arxiv.org/pdf/1509.02971 to get more information)"""
    def __init__(self, state_size, action_size, device, dtype, buffer_capacity=1e6, batch_size=64):
        super().__init__()
        self.device = device
        self.dtype = dtype
        self.buffer_capacity = buffer_capacity
        self.batch_size = batch_size

        self.current_index = 0
        self.buffer_is_filled = False

        self.state_buffer = torch.zeros((self.buffer_capacity, state_size), device=device, dtype=dtype)
        self.action_buffer = torch.zeros((self.buffer_capacity, action_size), device=device, dtype=dtype)
        self.reward_buffer = torch.zeros((self.buffer_capacity, 1), device=device, dtype=dtype)
        self.next_state_buffer = torch.zeros((self.buffer_capacity, state_size), device=device, dtype=dtype)

    def record(self, sars_tuple: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]) -> None:
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        self.state_buffer[self.current_index] = sars_tuple[0]
        self.action_buffer[self.current_index] = sars_tuple[1]
        self.reward_buffer[self.current_index] = sars_tuple[2]
        self.next_state_buffer[self.current_index] = sars_tuple[3]

        self.current_index += 1
        if self.current_index == self.buffer_capacity:
            self.buffer_is_filled = True
            self.current_index = 0

    def sample_sars_batch(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Samples random batch of SARS from the replay buffer
        """
        if self.buffer_is_filled:
            buffer_range = self.buffer_capacity
        else:
            buffer_range = self.current_index
        batch_indices = np.random.choice(buffer_range, size=self.batch_size)

        state_batch = self.state_buffer[batch_indices]  # TODO check if .to(device) is needed
        action_batch = self.action_buffer[batch_indices]  # TODO check if .to(device) is needed
        reward_batch = self.reward_buffer[batch_indices]  # TODO check if .to(device) is needed
        next_state_batch = self.next_state_buffer[batch_indices]  # TODO check if .to(device) is needed
        return state_batch, action_batch, reward_batch, next_state_batch
