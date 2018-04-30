import torch
from torch.distributions import Normal, Categorical, Distribution


class MixtureNormal(Distribution):
    def __init__(self, pi, loc, scale):
        self.pi, self.loc, self.scale = pi, loc, scale

        super(MixtureNormal, self).__init__()

        self.normal_pd = Normal(self.loc, self.scale)
        self.pi_pd = Categorical(self.pi)

    def sample(self, sample_shape=torch.Size()):
        with torch.no_grad():
            raw_sample = self.normal_pd.sample()
            index = self.pi_pd.sample().unsqueeze(-1)
            return torch.gather(raw_sample, -1, index).squeeze(-1)

    def log_prob(self, value):
        if self._validate_args:
            self._validate_sample(value)

        value = value.unsqueeze(-1).expand_as(self.loc)
        log_probs = self.normal_pd.log_prob(value)
        probs = torch.exp(log_probs)
        weighted_probs = self.pi * probs
        sum_prob = torch.sum(weighted_probs, -1)
        return torch.log(sum_prob)
