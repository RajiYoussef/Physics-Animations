"""Deterministic physical geometry, independent of render frame rate."""
import numpy as np


def two_phase(t):
    """One car: 10 -> 24 -> 10 m/s, +1.75 then -1.75 m/s², over 16 seconds."""
    t=np.clip(np.asarray(t,float),0,16)
    first=t<=8
    q=t-8
    x=np.where(first,10*t+.875*t*t,136+24*q-.875*q*q)
    v=np.where(first,10+1.75*t,24-1.75*q)
    a=np.where(t<8,1.75,-1.75)
    return x,v,a


def tangent(theta):
    return np.array([-np.sin(theta),np.cos(theta),0.])


def radial(theta):
    return np.array([np.cos(theta),np.sin(theta),0.])


def bend_by_distance(distance,start=(-5,-1.3,0),straight=3,radius=2.2):
    """C1 straight-to-circle path parameterized by arc length, in scene units.

    Position and tangent are continuous at the join. Curvature jumps from zero
    to 1/r there, an idealized circular corner rather than a transition spiral.
    """
    start=np.asarray(start,float)
    if distance<=straight:
        return start+np.array([distance,0,0]),np.array([1.,0,0]),np.zeros(3)
    theta=(distance-straight)/radius-np.pi/2
    center=start+np.array([straight,radius,0])
    return center+radius*radial(theta),tangent(theta),-radial(theta)/radius


def circular_state(t,radius=1,speed=1,phase=0):
    if radius<=0 or speed<0:raise ValueError("Positive radius and nonnegative speed required")
    angle=phase+speed*t/radius
    return radius*radial(angle),speed*tangent(angle),-speed**2/radius*radial(angle)


def velocity_difference(angle1,angle2,speed=1):
    return speed*(tangent(angle2)-tangent(angle1))
