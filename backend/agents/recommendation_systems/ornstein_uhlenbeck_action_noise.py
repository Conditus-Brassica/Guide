#Author: Vodohleb04
import numpy as np


class OrnsteinUhlenbeckNoise:
    def __init__(self, dtype, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None, reinit_x_prev_period=1000):
        super().__init__()
        self.dtype = dtype
        self.theta = theta
        self.mean = mean
        self.std_dev = std_deviation
        self.dt = dt
        if x_initial is not None:
            self._x_initial = x_initial
        else:
            self._x_initial = np.zeros_like(self.mean, dtype=dtype)
        
        self.x_prev = self._x_initial

        self._reinit_x_prev_period = reinit_x_prev_period
        self._after_last_reinit = 0


    def __call__(self):
        x = (
            self.x_prev +
            self.theta * (self.mean - self.x_prev) * self.dt +
            self.std_dev * np.sqrt(self.dt) * 
            np.random.normal(size=self.mean.shape, loc=0.0, scale=1.0).astype(self.dtype)
        )
        self._after_last_reinit += 1
        if self._after_last_reinit == self._reinit_x_prev_period:
            self.x_prev = self._x_initial
            self._after_last_reinit = 0
        else:
            self.x_prev = x
        return x
