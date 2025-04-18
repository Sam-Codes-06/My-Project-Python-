import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
import time

torch.set_default_dtype(torch.float)
torch.manual_seed(1234)
np.random.seed(1234)

Range = 1000
diffusion_rate, flux, L_range, T_range = 3000., 6., 10., 10.
x = np.linspace(0, L_range, Range)
t = np.linspace(0, T_range, Range)
X, T = np.meshgrid(x, t)

X_u_test = np.hstack((X.flatten()[:, None], T.flatten()[:, None]))

lb = np.array([0., 0.])
ub = np.array([L_range, T_range])


def trainingdata(N_b, N_p):
    boundary_1_xt = np.hstack((np.zeros((X.shape[0], 1)), T[:, 0][:, None]))
    boundary_1_u = np.ones((X.shape[0], 1)) * flux

    boundary_2_xt = np.hstack((X[:, -1][:, None], T[:, 0][:, None]))
    boundary_2_u = np.zeros(boundary_2_xt.shape[0])[:, None]

    boundary_3_xt = np.hstack((X[:][0].reshape(-1, 1), np.zeros((T.shape[0], 1))))
    boundary_3_u = flux * np.exp(1000 - (1000 / (1 - ((boundary_3_xt - lb) / (ub - lb)).T[0].reshape(-1, 1) ** 2)))
    # boundary_3_u = flux * (1. - ((boundary_3_xt - lb) / (ub - lb)).T[0].reshape(-1, 1)) ** 4

    train_xt = np.vstack([boundary_1_xt, boundary_2_xt, boundary_3_xt])
    train_u = np.vstack([boundary_1_u, boundary_2_u, boundary_3_u])

    random_indices = np.random.choice(train_xt.shape[0], N_b, replace=False)
    xt_boundary = train_xt[random_indices, :]
    u_boundary = train_u[random_indices, :]
    xt_collocation = lb + (ub - lb) * np.random.rand(N_p, 2)

    return xt_collocation, xt_boundary, u_boundary


N_b = 3000
N_p = 4000
xt_collocation, xt_boundary, u_boundary = trainingdata(N_b, N_p)
xt_collocation = torch.from_numpy(xt_collocation).float()
xt_boundary = torch.from_numpy(xt_boundary).float()
u_boundary = torch.from_numpy(u_boundary).float()
xt_space = torch.from_numpy(X_u_test).float()


class Sequentialmodel(nn.Module):
    def __init__(self):
        super().__init__()
        self.activation = nn.Tanh()
        self.loss_function = nn.MSELoss(reduction='mean')
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 1)

    def forward(self, x):
        u_b = torch.from_numpy(ub).float()
        l_b = torch.from_numpy(lb).float()
        x = (x - l_b) / (u_b - l_b)
        x = x.float()
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.activation(self.fc3(x))
        x = self.fc4(x)
        return x

    def loss_boundary(self, x, y):
        loss_u = self.loss_function(self.forward(x), y)
        return loss_u

    def loss_physics(self, x_to_train_f):
        temp_xt_collocation = x_to_train_f.clone()
        temp_xt_collocation.requires_grad = True
        u = self.forward(temp_xt_collocation)
        u_xt = autograd.grad(u.sum(), temp_xt_collocation, retain_graph=True, create_graph=True)[0]
        u_x_xt = autograd.grad(u_xt[:, [0]].sum(), temp_xt_collocation, create_graph=True)[0]
        u_t = u_xt[:, [1]]
        u_xx = u_x_xt[:, [0]]
        f = u_t - diffusion_rate * u_xx + 5 * (u ** 3 - u)
        residual = torch.zeros(f.shape[0], 1)
        loss_p = self.loss_function(f, residual)
        return loss_p

    def loss(self, x, y, xt_coll):
        loss_b = self.loss_boundary(x, y)
        loss_p = self.loss_physics(xt_coll)
        loss_v = .015 * loss_b + .001 * loss_p
        return [loss_v, loss_p, loss_b]

    def test(self):
        u_pred = self.forward(xt_space)
        u_pred = u_pred.cpu().detach().numpy()
        u_pred = np.reshape(u_pred, (Range, Range), order='F')
        return u_pred


PINN = Sequentialmodel()
optimizer = optim.Adam(PINN.parameters(), lr=0.0006, weight_decay=0, amsgrad=False)

start_time = time.time()
max_iter = 1000
Epoch, loss_val, loss_physics, loss_boundary = [], [], [], []
for i in range(max_iter):
    loss = PINN.loss(xt_boundary, u_boundary, xt_collocation)
    optimizer.zero_grad()
    loss[0].backward()
    optimizer.step()
    if i % 200 == 0:
        print(loss[0])
        Epoch.append(i)
        loss_val.append(loss[0].data)
        loss_physics.append(loss[1].data)
        loss_boundary.append(loss[2].data)

elapsed = time.time() - start_time
print('Training time: %.2f' % (elapsed))

u_pred = PINN.test()

sol = u_pred.T
plt.imshow(sol, interpolation='nearest', cmap='jet',
           extent=[X.min(), X.max(), T.min(), T.max()],
           origin='lower')
plt.title('Allen-Cahn Equation Graph')
plt.xlabel('X')
plt.ylabel('T')
plt.colorbar()
plt.tight_layout()
plt.show()

plt.grid()
plt.plot(Epoch, loss_val, label='Total Loss')
plt.plot(Epoch, loss_physics, label='Physics Loss')
plt.plot(Epoch, loss_boundary, label='Boundary Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()
