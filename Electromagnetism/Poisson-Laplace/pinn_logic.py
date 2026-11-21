"""Numbers behind scene_05: a Laplace problem, its grid solution, and a small neural
network trained to satisfy the equation and the boundary values. Pure numpy/scipy.

Problem: unit square 0 <= x, y <= 1, Laplace's equation inside,
V = sin(pi x) on the top edge (y = 1) and V = 0 on the other three edges.
Exact solution: V = sin(pi x) sinh(pi y) / sinh(pi).

Network: inputs (x, y) -> two hidden layers of tanh units -> one output.
Training minimises  mean(laplacian(V)^2) inside  +  BOUNDARY_WEIGHT * mean((V - g)^2) on the edges.
The Laplacian is computed exactly by forward-mode propagation through the layers.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

LAYERS = (2, 6, 6, 1)
BOUNDARY_WEIGHT = 10.0


# ---- the problem ---------------------------------------------------------

def boundary_value(x, y):
    return np.where(np.isclose(y, 1.0), np.sin(np.pi * x), 0.0)


def exact(x, y):
    return np.sin(np.pi * x) * np.sinh(np.pi * y) / np.sinh(np.pi)


def grid_solution(n: int = 6):
    """Finite-difference values V_ij on an n x n node grid (rows = y), solved with raji_sci SOR."""
    from raji_sci.physics.electrostatics_logic import grid, poisson_sor

    X, Y, (h, _) = grid((0.0, 1.0), (0.0, 1.0), n, n)
    fixed = np.zeros_like(X, bool)
    fixed[0, :] = fixed[-1, :] = fixed[:, 0] = fixed[:, -1] = True
    values = np.where(fixed, boundary_value(X, Y), 0.0)
    V, _ = poisson_sor(np.zeros_like(X), h, fixed, values, tol=1e-12)
    return X, Y, V


def bilinear(X, Y, V, x, y):
    """Interpolated value at (x, y) from the four surrounding grid nodes, and their indices."""
    xs, ys = X[0], Y[:, 0]
    i = int(np.clip(np.searchsorted(xs, x) - 1, 0, len(xs) - 2))
    j = int(np.clip(np.searchsorted(ys, y) - 1, 0, len(ys) - 2))
    tx = (x - xs[i]) / (xs[i + 1] - xs[i])
    ty = (y - ys[j]) / (ys[j + 1] - ys[j])
    w = {(j, i): (1 - tx) * (1 - ty), (j, i + 1): tx * (1 - ty),
         (j + 1, i): (1 - tx) * ty, (j + 1, i + 1): tx * ty}
    return float(sum(V[k] * c for k, c in w.items())), w


# ---- the network ---------------------------------------------------------

def shapes():
    return [(LAYERS[k + 1], LAYERS[k]) for k in range(len(LAYERS) - 1)]


def n_params() -> int:
    return sum(o * i + o for o, i in shapes())


def unpack(theta):
    out, k = [], 0
    for o, i in shapes():
        W = theta[k:k + o * i].reshape(o, i); k += o * i
        b = theta[k:k + o]; k += o
        out.append((W, b))
    return out


def init_params(seed: int = 3) -> np.ndarray:
    rng = np.random.default_rng(seed)
    parts = []
    for o, i in shapes():
        parts.append(rng.normal(0, np.sqrt(1.0 / i), (o, i)).ravel())
        parts.append(np.zeros(o))
    return np.concatenate(parts)


def forward(theta, x, y, with_laplacian: bool = False):
    """Network output at points (x, y); optionally also its exact Laplacian.

    Returns (V, activations) or (V, laplacian, activations); activations lists each
    layer's values with shape (units, points), inputs first.
    """
    x = np.atleast_1d(np.asarray(x, float))
    y = np.atleast_1d(np.asarray(y, float))
    a = np.vstack([2 * x - 1, 2 * y - 1])  # inputs scaled to [-1, 1]
    # forward-mode: gradient wrt (x, y) and Laplacian, carried with the values
    g = np.zeros((2, 2, x.size)); g[0, 0] = 2.0; g[1, 1] = 2.0  # d(input_k)/d(x_m)
    lap = np.zeros((2, x.size))
    acts = [a]
    params = unpack(theta)
    for layer, (W, b) in enumerate(params):
        z = W @ a + b[:, None]
        gz = np.einsum("oi,imp->omp", W, g)
        lz = W @ lap
        if layer < len(params) - 1:
            t = np.tanh(z)
            d1 = 1 - t**2
            d2 = -2 * t * d1
            a = t
            g = d1[:, None, :] * gz
            lap = d2 * np.sum(gz**2, axis=1) + d1 * lz
        else:
            a, g, lap = z, gz, lz
        acts.append(a)
    V = a[0]
    return (V, lap[0], acts) if with_laplacian else (V, acts)


# ---- training ------------------------------------------------------------

def collocation(seed: int = 7, n_inside: int = 196, n_edge: int = 30):
    rng = np.random.default_rng(seed)
    inside = rng.uniform(0.02, 0.98, (n_inside, 2))
    t = np.linspace(0, 1, n_edge)
    edges = np.vstack([np.column_stack([t, 0 * t]), np.column_stack([t, 0 * t + 1]),
                       np.column_stack([0 * t, t]), np.column_stack([0 * t + 1, t])])
    return inside, edges


def mismatches(theta, inside, edges):
    _, lap, _ = forward(theta, inside[:, 0], inside[:, 1], with_laplacian=True)
    Vb, _ = forward(theta, edges[:, 0], edges[:, 1])
    gb = boundary_value(edges[:, 0], edges[:, 1])
    return float(np.mean(lap**2)), float(np.mean((Vb - gb) ** 2))


def train(max_iter: int = 600, seed: int = 3):
    """Fit the network. Returns (theta, history) with history = list of (theta, interior, boundary)."""
    inside, edges = collocation()
    theta0 = init_params(seed)
    history = [(theta0.copy(), *mismatches(theta0, inside, edges))]

    def loss(theta):
        r, b = mismatches(theta, inside, edges)
        return r + BOUNDARY_WEIGHT * b

    def record(theta):
        history.append((theta.copy(), *mismatches(theta, inside, edges)))

    result = minimize(loss, theta0, method="L-BFGS-B", callback=record,
                      options={"maxiter": max_iter, "maxfun": 200000})
    return result.x, history


def max_error(theta, n: int = 41) -> float:
    s = np.linspace(0, 1, n)
    X, Y = np.meshgrid(s, s)
    V, _ = forward(theta, X.ravel(), Y.ravel())
    return float(np.max(np.abs(V - exact(X.ravel(), Y.ravel()))))
