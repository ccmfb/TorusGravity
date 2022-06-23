'''
Example code for a simulation of an object orbiting a torus.

'''
from three_cc.simulation import Simulation
from three_cc.objects import *
from three_cc.animation import Animation


all_objects = []

planet = Torus(
        position=(0,0,0),
        mass=500,
        r1=10,
        r2=3
        )
planet.set_color_map('terrain')

sat1 = Sphere(
        position=(20,0,0),
        mass=1,
        radius=1,
        velocity=(0,0,-2.313),
        attracted_to=planet
        )
sat1.set_color('lightgray')

'''
sat2 = Sphere(
        position=(15,0,0),
        mass=1,
        radius=1,
        velocity=(0,0,-6.5),
        attracted_to=planet
        )
sat2.set_color('lightgray')

sat3 = Sphere(
        position=(0,-20,0),
        mass=1,
        radius=1,
        velocity=(0,0,-8.5),
        attracted_to=planet
        )
sat3.set_color('lightgray')

'''

all_objects.append(planet)
all_objects.append(sat1)
#all_objects.append(sat2)
#all_objects.append(sat3)

# Simulating all positions
simulation = Simulation(duration=30)
simulation.start(all_objects)

# Making the animations
anim = Animation(axes_bounds=20)

anim.set_ambient_rot(55,55)
anim.set_elev_rot(30, 30)
anim.set_blackout(False)

anim.animate(all_objects)



