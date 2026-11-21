"""The executable source is also used for the on-screen code excerpts."""
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp
from jax import grad, jit, vmap, random
import settings
n = settings.HIDDEN_UNITS

# snippet:model
def potential(p, x, y):
    wx, b = p[:n], p[n:2*n]
    wy, wo = p[2*n:3*n], p[3*n:4*n]
    hidden = jnp.tanh(x*wx + y*wy + b)
    return jnp.sum(hidden*wo) + p[4*n]
# end:model

# snippet:derivatives
Vx = grad(potential, argnums=1)
Vy = grad(potential, argnums=2)
Vxx = grad(Vx, argnums=1)
Vyy = grad(Vy, argnums=2)
V_batch = vmap(potential, (None, 0, 0))
Vxx_batch = vmap(Vxx, (None, 0, 0))
Vyy_batch = vmap(Vyy, (None, 0, 0))
# end:derivatives

# snippet:initialize
key = random.PRNGKey(settings.SEED)
key_init, key_points, key_check = random.split(key, 3)
params_initial = random.normal(key_init, (4*n+1,))
# end:initialize

# snippet:points
points = jnp.pi * random.uniform(
    key_points, (settings.INTERIOR_POINTS, 2))
def interior_loss(p, samples):
    x, y = samples[:, 0], samples[:, 1]
    residual = Vxx_batch(p, x, y) + Vyy_batch(p, x, y)
    return jnp.mean(residual**2)
# end:points

# snippet:boundary
x_edge = jnp.linspace(0, jnp.pi, settings.BOUNDARY_POINTS)
y_edge = jnp.linspace(0, jnp.pi, settings.BOUNDARY_POINTS)
target_bottom = jnp.sin(x_edge)
zero = jnp.zeros_like(x_edge)
far = jnp.full_like(x_edge, jnp.pi)
# end:boundary

# snippet:boundary_loss
def boundary_losses(p):
    bottom = V_batch(p, x_edge, zero) - target_bottom
    left = V_batch(p, zero, y_edge)
    right = V_batch(p, far, y_edge)
    top = V_batch(p, x_edge, far)
    return jnp.array([jnp.mean(e**2)
                     for e in (bottom, left, right, top)])
# end:boundary_loss

@jit
def components(p, samples):
    return jnp.concatenate((jnp.array([interior_loss(p, samples)]), boundary_losses(p)))

# snippet:loss
@jit
def loss(p, samples):
    return interior_loss(p, samples) + jnp.sum(boundary_losses(p))
grad_loss = jit(grad(loss, argnums=0))
# end:loss

# snippet:update
@jit
def update(p, velocity):
    lookahead = p + settings.MOMENTUM * velocity
    gradient = grad_loss(lookahead, points)
    velocity = (settings.MOMENTUM * velocity
                - settings.LEARNING_RATE * gradient)
    return p + velocity, velocity
# end:update

predict = jit(V_batch)
residual_batch = jit(lambda p,x,y: Vxx_batch(p,x,y)+Vyy_batch(p,x,y))
