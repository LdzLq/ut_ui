import torch.nn as nn

class RNNimc(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=128, layer_dim=1):
        super(RNNimc, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.output_dim = output_dim

        self.rnn = nn.RNN(self.input_dim, self.hidden_dim, self.layer_dim, batch_first=True, nonlinearity='relu')
        self.fc = nn.Linear(self.hidden_dim, self.output_dim)

    def forward(self, x):
        out, h_n = self.rnn(x, None)
        out = self.fc1(out[:, -1, :])
        return out
