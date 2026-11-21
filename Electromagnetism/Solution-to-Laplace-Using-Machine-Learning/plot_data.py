"""Evaluate saved parameters for plotting, without importing a training backend."""
import numpy as np

def evaluate(p, X, Y):
    n=(len(p)-1)//4
    z=X[...,None]*p[:n]+Y[...,None]*p[2*n:3*n]+p[n:2*n]
    return np.tanh(z)@p[3*n:4*n]+p[4*n]

# snippet:grid
def potential_grid(p, points=41):
    x = np.linspace(0, np.pi, points)
    X, Y = np.meshgrid(x, x, indexing='xy')
    V = evaluate(p, X, Y)
    return X, Y, V
# end:grid
