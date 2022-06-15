from three_cc.objects import Torus
import three_cc.util as util

import pandas as pd


class Simulation:
    def __init__(self, duration=10):
        self.duration = duration
        self.dt = 1/20
        self.total_steps = int(self.duration / self.dt)

        
    def start(self, objects):

        # --------------------- MAIN LOOP -----------------------
        # -------------------------------------------------------

        for step in util.progressbar(range(self.total_steps), 'Simulating: ', 40):

            for obj in objects:
                obj.update_pos(self.dt)
    
        # -------------------------------------------------------
        # -------------------------------------------------------

        self.create_csv(objects)

    def create_csv(self, objects):
        all_data = {}

        for obj in objects:
            if isinstance(obj, Torus):
                pass
            else:
                all_data.update({f'P_i{obj.initial_pos}, v_i={obj.initial_velocity}': obj.position_data})

        df = pd.DataFrame.from_dict(all_data, orient='index')
        df = df.transpose()
        df.to_csv('out.csv')

