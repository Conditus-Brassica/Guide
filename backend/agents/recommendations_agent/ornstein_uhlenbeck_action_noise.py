#Author: Vodohleb04
import numpy as np


class OrnsteinUhlenbeckNoise:
    def __init__(self, dtype, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None):
        super().__init__()
        self.dtype = dtype
        self.theta = theta
        self.mean = mean
        self.std_dev = std_deviation
        self.dt = dt
        if x_initial is not None:
            self.x_prev = x_initial
        else:
            self.x_prev = np.zeros_like(self.mean, dtype=dtype)


    def __call__(self):
        x = (
            self.x_prev +
            self.theta * (self.mean - self.x_prev) * self.dt +
            self.std_dev * np.sqrt(self.dt) * 
            np.random.normal(size=self.mean.shape, loc=0.0, scale=1.0).astype(self.dtype)
        )
        self.x_prev = x
        return x
