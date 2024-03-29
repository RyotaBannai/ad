# %%
import time

import ipdb as pdb
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# if args.adjoint:
#     from torchdiffeq import odeint_adjoint as odeint
# else:
from torchdiffeq import odeint

device = torch.device("cpu")

data_size = 100
batch_size = 10
batch_time = 10
niters = 10
true_y0 = torch.tensor([[2.0, 0.0]])
t = torch.linspace(0.0, 25.0, data_size)
true_A = torch.tensor([[-0.1, 2.0], [-2.0, -0.1]])


class Lambda(nn.Module):
    def forward(self, t, y):
        return torch.mm(y**3, true_A)


with torch.no_grad():
    true_y = odeint(Lambda(), true_y0, t, method="dopri5")


def get_batch():
    s = torch.from_numpy(
        np.random.choice(
            np.arange(data_size - batch_time, dtype=np.int64),
            batch_size,
            replace=False,
        )
    )
    batch_y0 = true_y[s]  # (M, D)
    batch_t = t[:batch_time]  # (T)
    batch_y = torch.stack([true_y[s + i] for i in range(batch_time)], dim=0)  # (T, M, D)
    return batch_y0, batch_t, batch_y


class ODEFunc(nn.Module):
    def __init__(self):
        super(ODEFunc, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(2, 50),
            nn.Tanh(),
            nn.Linear(50, 2),
        )

        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, mean=0, std=0.1)
                nn.init.constant_(m.bias, val=0)

    def forward(self, t, y):
        return self.net(y**3)


class RunningAverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, momentum=0.99):
        self.momentum = momentum
        self.reset()

    def reset(self):
        self.val = None
        self.avg = 0

    def update(self, val):
        if self.val is None:
            self.avg = val
        else:
            self.avg = self.avg * self.momentum + val * (1 - self.momentum)
        self.val = val


def main():

    func = ODEFunc()

    optimizer = optim.RMSprop(func.parameters(), lr=1e-3)
    end = time.time()

    time_meter = RunningAverageMeter(0.97)

    loss_meter = RunningAverageMeter(0.97)

    for itr in range(1, niters + 1):
        optimizer.zero_grad()
        batch_y0, batch_t, batch_y = get_batch()
        pred_y = odeint(func, batch_y0, batch_t)
        loss = torch.mean(torch.abs(pred_y - batch_y))
        loss.backward()
        optimizer.step()

        pdb.set_trace()

        time_meter.update(time.time() - end)
        loss_meter.update(loss.item())

        # if itr % args.test_freq == 0:
        #     with torch.no_grad():
        #         pred_y = odeint(func, true_y0, t)
        #         loss = torch.mean(torch.abs(pred_y - true_y))
        #         print("Iter {:04d} | Total Loss {:.6f}".format(itr, loss.item()))
        #         ii += 1

        end = time.time()


if __name__ == "__main__":
    main()

# %%

# %%
