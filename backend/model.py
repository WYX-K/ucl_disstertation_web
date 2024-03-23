import torch
import torch.nn as nn


class LSTM(nn.Module):
    def __init__(self, vocab_size=15, region_embedding_dim=16, time_embedding_dim=32, hidden_size=64, output_size=1):
        super(LSTM, self).__init__()
        self.region_embedding = nn.Embedding(
            vocab_size, region_embedding_dim, padding_idx=0)
        self.time_embedding = nn.Embedding(
            vocab_size, time_embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(region_embedding_dim +
                            time_embedding_dim, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, region_sequences, time_sequences):
        region_embed = self.region_embedding(region_sequences)
        time_embed = self.time_embedding(
            region_sequences) * time_sequences.unsqueeze(-1)
        combined_embed = torch.cat([region_embed, time_embed], dim=-1)
        _, (hidden, _) = self.lstm(combined_embed)
        out = self.fc(hidden.squeeze(0))
        out = self.sigmoid(out)
        return out