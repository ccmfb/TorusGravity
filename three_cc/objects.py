import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


G = 6.67 * 10**(-11)

class SObject:
    def __init__(self, position, mass, velocity, attracted_to):
        # BASIC PROPERTIES OF ALL OBJECTS
        self.initial_pos = position
        self.initial_velocity = velocity

        self.pos = np.array([position[0], position[1], position[2]])
        self.velocity = np.array([velocity[0], velocity[1], velocity[2]])
        self.mass = mass
        self.attracted_to = attracted_to

        # STYLE
        self.cmap = None
    
        # ANALYSIS PROPERTIES
        self.position_data = []
        self.position_data.append(list(self.pos))


    def update_pos(self, dt):
        if self.attracted_to is not None:
            F = self.attracted_to.get_force(self.pos, self.mass)
            dv = F * dt / self.mass

            self.velocity = self.velocity + dv
            self.pos = self.pos + self.velocity * dt

        self.position_data.append(list(self.pos))

    def set_color_map(self, cmap):
        self.cmap = cmap


class Sphere(SObject):
    def __init__(self, position, mass, radius, velocity=(0,0,0), attracted_to=None):
        super().__init__(position, mass, velocity, attracted_to)
        self.r = radius

        # STYLISTIC
        self.color = 'r'

        print('Initialised Sphere...')

    def get_force(self, pos, mass):
        r_vec = pos - self.pos
        r_mag = np.sqrt(r_vec.dot(r_vec))
        r_hat = - r_vec / r_mag

        return r_hat * G * mass * self.mass / r_mag**2

    def plot(self, ax, frame):
        pos = self.position_data[frame]

        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
        x = self.r * np.cos(u) * np.sin(v)
        y = self.r * np.sin(u) * np.sin(v)
        z = self.r * np.cos(v)
        ax.plot_surface(pos[0] - x, pos[1] - y, pos[2] - z, cmap=self.cmap, color=self.color, zorder=10)

    def set_color(self, color):
        self.color = color


class Torus(SObject):
    def __init__(self, position, mass, r1, r2, velocity=(0,0,0), attracted_to=None):
        super().__init__(position, mass, velocity, attracted_to)
        self.r1 = r1
        self.r2 = r2
        self.rho = mass / (2 * np.pi * r1)

        self.parts = 32

        # STYLISTIC
        self.lw = 0

        print('Initialised Torus...')

    def get_force(self, pos, mass):
        r = np.sqrt(pos[0]**2 + pos[1]**2)
        if pos[0] > 0:
            phi = np.arctan(pos[1]/pos[0])

        elif pos[0] < 0:
            phi = np.arctan(pos[1]/pos[0]) + np.pi

        else:
            phi = 0

        z = pos[2]

        F_r = self.r1 * self.rho * quad(self.__fr, 0, 2 * np.pi, args=(r,z))[0]
        F_z = self.r1 * self.rho * quad(self.__fz, 0, 2 * np.pi, args=(r,z))[0]

        F_x = F_r * np.cos(phi)
        F_y = F_r * np.sin(phi)

        return np.array([F_x, F_y, F_z])
    
    def __fr(self, phi, r, z):
        force_r = (self.r1*np.cos(phi) - r ) / (self.r1**2 - 2*self.r1*r*np.cos(phi) + r**2 + z**2)**(3/2)

        return force_r
        
    def __fz(self, phi, r, z):
        force_z = -z / ((self.r1**2 - 2*self.r1*r*np.cos(phi) + r**2 + z**2)**(3/2))

        return force_z

    def plot(self, ax, rel_index, view_angle, frame):
        pos = self.position_data[frame]

        current_phi = (np.pi * view_angle / 180) + (2 * rel_index + 1) * np.pi / self.parts

        n = 100

        theta = np.linspace(0, 2.*np.pi, n)
        phi = np.linspace(current_phi - np.pi/self.parts, current_phi + np.pi/self.parts, n)
        theta, phi = np.meshgrid(theta, phi)
        c, a = self.r1, self.r2
        x = (c + a*np.cos(theta)) * np.cos(phi)
        y = (c + a*np.cos(theta)) * np.sin(phi)
        z = a * np.sin(theta)

        ax.plot_surface(pos[0] - x, pos[1] - y, pos[2] - z, rstride=5, cstride=5, cmap=self.cmap, linewidth=self.lw)


















