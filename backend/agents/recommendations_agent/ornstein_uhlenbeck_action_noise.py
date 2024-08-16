#Author: Vodohleb04
import torch
from torch import nn
import numpy as np


class OrnsteinUhlenbeckActionNoise(nn.Module):
    """
    Noise process to find the solution of the exploration-exploitation problem
    """
    def __init__(self, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None, device=None, dtype=None):
        super().__init__()
        if device is None:
            device = torch.device('cpu')
        if dtype is None:
            dtype = torch.float64
        self.theta = theta
        self.mean = mean
        self.std_deviation = std_deviation
        self.dt = dt
        self.x_initial = x_initial
        self.device = device
        self.dtype = dtype
        self.reset()

    def forward(self):
        x = (
            self.x_prev
            + self.theta * (self.mean - self.x_prev) * self.dt
            + self.std_deviation * np.sqrt(self.dt) * torch.normal(
                    mean=0.0, std=1.0, size=self.mean.shape, device=self.device, dtype=self.dtype
                )
        )
        self.x_prev = x
        return x

    def reset(self):
        if self.x_initial is not None:
            self.x_prev = self.x_initial
        else:
            self.x_prev = torch.zeros_like(self.mean, device=self.device, dtype=self.dtype)
