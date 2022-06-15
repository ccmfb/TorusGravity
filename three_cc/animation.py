from three_cc.util import VideoTools
from three_cc.objects import *
import three_cc.util as util

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
            

class Animation:
    def __init__(self, axes_bounds, fps=30, time_multiplier=1):
        # TIME, FPS, ...
        self.time_multiplier = time_multiplier
        self.fps = fps
        
        # FIGURE, AXES, ...
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.axes_bounds = axes_bounds
        self.blackout = False
        self.dpi = 500

        self.view_angle = 50 
        self.view_angle_end = 70 
        self.view_angle_i = 0

        self.view_elev = 30
        self.view_elev_end = 50
        self.view_elev_i = 0

        self.camera_radius = -10 * np.sqrt(3 * (self.axes_bounds)**2)

        # VIDEO TOOLS
        self.vid_tools = VideoTools()
        self.vid_tools.remove_folder('images')
        self.vid_tools.create_folder('images')

        print('Initialised Animation...')

    def animate(self, objects):
        total_frames = len(objects[0].position_data)
        self.view_angle_i = (self.view_angle_end - self.view_angle) / total_frames
        self.view_elev_i = (self.view_elev_end - self.view_elev) / total_frames

        for frame in util.progressbar(range(total_frames), 'Animating: ', 40):
            self.clear_figure()
            
            to_plot = self.get_plot_order(objects, frame)

            for item in to_plot:
                obj = item[0]
                dist = item[1]

                if isinstance(obj, Torus):
                    rel_index = item[2] 
                    obj.plot(self.ax, rel_index, view_angle=self.view_angle, frame=frame)
                else:
                    obj.plot(self.ax, frame)

            plt.savefig(f'images/{frame}.png', dpi=self.dpi)
            plt.cla()
            plt.close('all')

        self.vid_tools.create_folder('videos')
        self.vid_tools.create_mp4('images', self.fps)

    def clear_figure(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # TEST --------------------------
        if self.blackout:
            self.fig.set_facecolor('black')
            self.ax.set_facecolor('black')
            self.ax.grid(False)
            self.ax.w_xaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
            self.ax.w_yaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
            self.ax.w_zaxis.set_pane_color((0.0,0.0,0.0,0.0)) 
        # --------------------------

        self.ax.set_xlim3d([self.axes_bounds, -self.axes_bounds])
        self.ax.set_xlabel('x')

        self.ax.set_ylim3d([self.axes_bounds, -self.axes_bounds])
        self.ax.set_ylabel('y')

        self.ax.set_zlim3d([self.axes_bounds, -self.axes_bounds])
        self.ax.set_zlabel('z')

        self.ax.view_init(elev = self.view_elev, azim = self.view_angle)
        self.view_angle += self.view_angle_i
        self.view_elev += self.view_elev_i

    def get_plot_order(self, objects, frame):
        to_plot = []
        
        sat = objects[0] if isinstance(objects[0], Sphere) else objects[1]
        torus = objects[0] if isinstance(objects[0], Torus) else objects[1]
        
        vec_s = np.array(sat.position_data[frame]) # Vector from origin to satellite
        vec_t = np.array(torus.position_data[frame]) # Vector from origin to torus
        vec_c = self.get_camera_pos() # Vector from origin to camera

        vec_r1 = vec_t - vec_c
        vec_r1[2] = 0
        vec_r1 = -torus.r1 * vec_r1 / np.linalg.norm(vec_r1) # Vector from centre of torus to centre of tube in opposite direction as camera

        for i in range(torus.parts):
            vec_to_part = np.dot(vec_r1, self.rot_mat((2*i+1) * np.pi / torus.parts))
            vec_pos = vec_t + vec_to_part

            #self.ax.scatter(vec_pos[0], vec_pos[1], vec_pos[2])

            dist = np.linalg.norm(vec_pos - vec_c)
            to_plot.append((torus, dist, i))


        to_plot.append((sat, np.linalg.norm(vec_s - vec_c)))

        to_plot.sort(key=lambda x:x[1], reverse=True)

        #for item in to_plot:
        #    print(item)

        return to_plot

    def rot_mat(self, angle):
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
            ])

    def get_plot_order_old(self, objects, frame):
        sat = objects[0] if isinstance(objects[0], Sphere) else objects[1]
        torus = objects[0] if isinstance(objects[0], Torus) else objects[1]

        vec_s = np.array(sat.position_data[frame]) # Vector from origin to satellite
        vec_t = np.array(torus.position_data[frame]) # Vector from origin to torus
        vec_c = self.get_camera_pos() # Vector from origin to camera

        vec_r1 = vec_t - vec_c
        vec_r1[2] = 0
        vec_r1 = torus.r1 * vec_r1 / np.linalg.norm(vec_r1) # Vector from centre of torus to centre of tube in same direction as camera

        dist_t_to_s = np.linalg.norm(vec_s - vec_t) # Distance from torus to satellite
        if 0.1 * torus.r1 <= dist_t_to_s <= 1.9 * torus.r1:
            dist_s_to_back = np.linalg.norm(vec_s - (vec_t + vec_r1))
            dist_s_to_front = np.linalg.norm(vec_s - (vec_t - vec_r1))

            if dist_s_to_back <= dist_s_to_back: # i.e. closer to back side of torus

                vec_t_to_s = vec_s - vec_t
                vec_t_to_s[2] = 0 # Projects in xy-plane

                vec_t_to_tube = torus.r1 * vec_t_to_s / np.linalg.norm(vec_t_to_s)

                vec_front = vec_t - vec_r1
                vec_back = vec_t + vec_t_to_tube

                self.ax.scatter(vec_front[0], vec_front[1], vec_front[2])
                self.ax.scatter(vec_back[0], vec_back[1], vec_back[2])

                torus_dist_to_front = np.linalg.norm( vec_front  - vec_c )
                torus_dist_to_back = np.linalg.norm( vec_back - vec_c )
            else:

                vec_t_to_s = vec_s - vec_t
                vec_t_to_s[2] = 0 # Projects in xy-plane

                vec_t_to_tube = torus.r1 * vec_t_to_s / np.linalg.norm(vec_t_to_s)

                vec_front = vec_t + vec_t_to_tube
                vec_back = vec_t + vec_r1

                self.ax.scatter(vec_front[0], vec_front[1], vec_front[2])
                self.ax.scatter(vec_back[0], vec_back[1], vec_back[2])

                torus_dist_to_front = np.linalg.norm( vec_front - vec_c )
                torus_dist_to_back = np.linalg.norm( vec_back - vec_c )


        else:
            vec_front = vec_t - vec_r1
            vec_back = vec_t + vec_r1

            self.ax.scatter(vec_front[0], vec_front[1], vec_front[2])
            self.ax.scatter(vec_back[0], vec_back[1], vec_back[2])
            
            torus_dist_to_front = np.linalg.norm( vec_front - vec_c )
            torus_dist_to_back = np.linalg.norm( vec_back - vec_c )

        to_plot = []
        to_plot.append((sat, np.linalg.norm(vec_s - vec_c)))
        to_plot.append((torus, torus_dist_to_front))
        to_plot.append((torus, torus_dist_to_back))

        to_plot.sort(key=lambda x:x[1], reverse=True)

        #for item in to_plot:
        #    print(item)

        return to_plot


    def get_camera_pos(self):
        phi = 2*np.pi * (self.view_angle - self.view_angle_i) / 360
        theta = (np.pi / 2) - ((self.view_elev/360) * 2*np.pi)
        r = self.camera_radius
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        return np.array([x,y,z])

    def set_ambient_rot(self, start, end):
        self.view_angle = start
        self.view_angle_end = end

    def set_elev_rot(self, start, end):
        self.view_elev = start
        self.view_elev_end = end

    def set_blackout(self, blackout):
        self.blackout = blackout


