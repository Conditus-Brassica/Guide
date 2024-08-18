# Author: Vodohleb04
from typing import List
import torch
from torch import nn
from torch.nn import functional as F


class ActorModel(nn.Module):
    """
    Model to generate actions. Model works using Wolpertinger policy
    (check https://arxiv.org/pdf/1512.07679 for more details)

    The base for the Wolpertinger actor model is DDPG actor model from https://arxiv.org/pdf/1509.02971
    """

    def _init_hidden_layers(self, input_layer: int, hidden_layers: List[int], device: torch.device, dtype: torch.dtype):
        self.hidden_layers.append(
            nn.Linear(input_layer, hidden_layers[0], bias=False, device=device, dtype=dtype)
        )  # ReLU activation
        self.hidden_layers.append(
            nn.BatchNorm1d(hidden_layers[0], device=device, dtype=dtype)
        )
        i = 1
        while i < len(hidden_layers):
            self.hidden_layers.append(
                nn.Linear(hidden_layers[i - 1], hidden_layers[i], bias=False, device=device, dtype=dtype)  # ReLU activation
            )
            self.hidden_layers.append(
                nn.BatchNorm1d(hidden_layers[i], device=device, dtype=dtype)
            )
            i += 1

    def __init__(
            self,
            state_size: int, input_layer: int, hidden_layers: List[int], action_size: int, dropout_keep_prob: int,
            device: torch.device, dtype: torch.dtype
    ):
        if dropout_keep_prob < 0 or dropout_keep_prob > 1:
            raise ValueError("Keep probability is rational number defined on [0, 1]")
        super().__init__()
        self.hidden_layers = nn.ModuleList()
        # layer -> batch_norm -> activation -> dropout
        self.input_layer = nn.Linear(state_size, input_layer, bias=False, device=device, dtype=dtype)  # ReLU activation
        self.input_batch_norm = nn.BatchNorm1d(input_layer, device=device, dtype=dtype)

        if hidden_layers:
            self._init_hidden_layers(input_layer, hidden_layers, device, dtype)
            self.output_layer = nn.Linear(hidden_layers[-1], action_size, bias=False, device=device, dtype=dtype)  # tanh activation
        else:
            self.output_layer = nn.Linear(input_layer, action_size, bias=False, device=device, dtype=dtype)  # tanh activation
        self.output_batch_norm = nn.BatchNorm1d(action_size, device=device, dtype=dtype)

    def init_weights(self):
        # Init weights with asymmetric activation function
        nn.init.kaiming_normal_(self.input_layer.weight)
        for hidden_layer in self.hidden_layers:
            if isinstance(hidden_layer, nn.Linear):
                nn.init.kaiming_normal_(hidden_layer.weight)

        # Init weights with symmetric activation function
        nn.init.uniform_(self.output_layer.weight, a=-0.003, b=0.003)

    def _network(self, x: torch.Tensor):
        x = F.linear(x, self.input_layer.weight.clone(), bias=None)
        x = self.input_batch_norm(x)
        x =


    def forward(self, state: torch.Tensor, actions_tensor: torch.Tensor) -> torch.Tensor:
        """
        Takes the state and the set of actions that can be applied to the environment. Actor defines the proto-action
        using state and defines the distance between proto-action and the given actions. Tensor of the corresponding
        distance is returned. L2 distance is used to count distance.
        """
        proto_action = self.input_layer()
        # proto_action = self.network(state)
        pass

    def turn_off_gradient(self):
        for param in self.parameters():
            param.requires_grad_(False)

