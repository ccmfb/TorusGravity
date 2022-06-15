'''
Example code for a simulation of an object orbiting a torus.

'''

from three_cc.simulation import Simulation
from three_cc.objects import *
from three_cc.animation import Animation


simulation = Simulation(duration=20)

all_objects = []

planet = Torus(
        position=(0,0,0),
        mass=500,
        r1=10,
        r2=3
        )
planet.set_color_map('terrain')

sat = Sphere(
        position=(20,0,0),
        mass=1,
        radius=1.5,
        velocity=(0,0,2.313),
        attracted_to=planet
        )
sat.set_color('lightgray')

all_objects.append(planet)
all_objects.append(sat)

simulation.start(all_objects)

anim1 = Animation(axes_bounds=20)
anim1.set_ambient_rot(55,85)
anim1.set_elev_rot(20, 50)
anim1.set_blackout(True)
anim1.animate(all_objects)



