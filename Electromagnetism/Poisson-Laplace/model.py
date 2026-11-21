"""Static homogeneous slab in normalized units, 0 <= y <= H."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Slab:
    H: float = 3.0
    epsilon: float = 1.0
    Vg: float = 0.0

    def potential(self, y, Vc=-6.0, rho=0.0):
        return self.Vg + (Vc-self.Vg)*y/self.H + rho*y*(self.H-y)/(2*self.epsilon)

    def field(self, y, Vc=-6.0, rho=0.0):
        return -(Vc-self.Vg)/self.H-rho*(self.H-2*y)/(2*self.epsilon)
