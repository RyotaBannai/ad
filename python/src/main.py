# %%
import random

import ipdb as pdb
import numpy as np
import pandas as pd
import plotly.express as px
import torch
import torchdiffeq
from scipy.integrate import odeint


# %%
def plot2d(var_list, t_label, y_label, columns):
    df = pd.DataFrame(var_list, columns=columns)
    fig = px.line(df, x=t_label, y=y_label)
    fig.show()


def plot3d(var_list, t_label, y_label, z_label, columns):
    df = pd.DataFrame(var_list, columns=columns)
    fig = px.line_3d(df, x=t_label, y=y_label, z=z_label)
    fig.show()


# T 半減期
def func_dydt(y, t, T):
    dydt = -y * 0.693 / T
    return dydt


def radioactive_decay():
    # 1階常微分方程式（放射性崩壊）
    t_list = np.linspace(0.0, 25.0, 1000)
    y_init = 1.0  # 初期値
    T = 5.0
    y_list = odeint(func_dydt, y_init, t_list, args=(T,))

    plot2d(zip(t_list, y_list[:, 0]), "t", "y", columns=["t", "y"], mode="lines+markers")


def func_lorenz(var, t, p, r, b):
    dxdt = -p * var[0] + p * var[1]
    dydt = -var[0] * var[2] + r * var[0] - var[1]
    dzdt = var[0] * var[1] - b * var[2]
    return [dxdt, dydt, dzdt]


def lorenz_equation():
    # 一階連立上微分方程式（Lorenz 方程式）- 気象における大気の対流現象を表した近似モデル
    t_list = np.linspace(0.0, 100.0, 10000)
    p = 10
    r = 28
    b = 8 / 3
    var_init = [0.1, 0.1, 0.1]  # 三次元座標上での初期値
    var_list = odeint(func_lorenz, var_init, t_list, args=(p, r, b))
    plot3d(var_list, t_label="x", y_label="y", z_label="z", columns=["x", "y", "z"])


def func_ast_move(var, t, m):
    # 天体の動き, m は天体の質量
    dxdt = var[2]  # u
    dydt = var[3]  # v
    r = var[0] * var[0] + var[1] * var[1]
    dudt = -m * var[0] / pow(r, 3 / 2)  # u`
    dvdt = -m * var[1] / pow(r, 3 / 2)  # v`
    return [dxdt, dydt, dudt, dvdt]


def astronomoical_object():
    t_list = np.linspace(0.0, 15.0, 100)
    m = 1.0
    var_init = [3.0, 0.0, 0.3, 0.2]  # 初期条件
    var_list = odeint(func_ast_move, var_init, t_list, args=(m,))
    # plot2d(var_list, t_label="x", y_label="y", columns=["x", "y", "u", "v"])
    return var_list


def ad_reg():
    random.seed(10)
    N = 200
    x = np.random.rand(N) * 30 - 15
    y = 2 * x + np.random.randn(N) * 5

    x = x.astype(np.float32)
    y = y.astype(np.float32)

    # fig = px.scatter(x=x, y=y)
    # fig.show()

    x = torch.from_numpy(x)
    y = torch.from_numpy(y)

    # 最適化する変数
    # 初期化
    w = torch.tensor(1.0, requires_grad=True)
    b = torch.tensor(0.0, requires_grad=True)

    # 線形回帰
    def model(x):
        return w * x + b

    # 平均二乗誤差（mean squared error）
    def mse(p, y):
        return ((p - y) ** 2).mean()

    lr = 1.0e-4

    losses = []
    for epoch in range(3000):
        p = model(x)

        loss = mse(p, y)
        loss.backward()

        with torch.no_grad():
            w -= w.grad * lr
            b -= b.grad * lr
            w.grad.zero_()
            b.grad.zero_()

        losses.append(loss.item())

    fig = px.scatter(losses)  # 誤差が減少しているのがわかる
    fig.show()


def ad_move():
    def model(t, var):
        # 天体の動き, m は天体の質量
        (x, y, u, v) = var
        r = x * x + y * y
        dudt = -1.0 * x / pow(r, 3 / 2)  # u`
        dvdt = -1.0 * y / pow(r, 3 / 2)  # v`
        ret = np.array([u, v, dudt, dvdt])
        ret = torch.from_numpy(ret)
        return ret

    def opt():
        true_y = np.array(astronomoical_object())
        true_y = torch.from_numpy(true_y)
        t_list = torch.linspace(0.0, 15.0, 100)
        var_init = np.array([3.0, 0.0, 0.3, 0.2])  # 初期条件
        var_init = torch.from_numpy(var_init)

        pred_y = torchdiffeq.odeint(model, var_init, t_list)
        loss = torch.mean(torch.abs(pred_y - true_y))

        pdb.set_trace()

    opt()


def main():
    # radioactive_decay()
    # lorenz_equation()
    # astronomoical_object()

    # ad_reg()
    ad_move()


main()

# %%
