import matplotlib.pyplot as plt
from more_itertools import last
import numpy as np

from pyworld3 import World3, world3
from pyworld3.utils import plot_world_variables

params = {"lines.linewidth": "3"}
plt.rcParams.update(params)

def run_world3_simulation(year_min, year_max, dt=1, prev_run_data={}, k_index=1):

    if bool(prev_run_data):
        world3 = World3(
            year_max=year_max,
            year_min=year_min, 
            dt=dt,
            prev_world_prop= prev_run_data["world_props"],
            ordinary_run= False
        )
        world3.set_world3_control()
        world3.init_world3_constants()
        world3.init_world3_variables(prev_run_data["init_vars"])
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions(prev_delay=prev_run_data["delay_funcs"])
    else:
        world3 = World3(
            year_max=year_max,
            year_min=year_min, 
            dt=dt,
            ordinary_run= True
        )
        world3.set_world3_control()
        world3.init_world3_constants()
        world3.init_world3_variables()
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions()

    world3.run_world3(fast=False, k_index=k_index)
    return world3.get_state(), world3


def main():
    # Run the first simulation
    dict_for_run_2, world3 = run_world3_simulation(year_min=1900, year_max=2000)

    # Run the second simulation with initial conditions derived from the first simulation
    world3_second, world3_second = run_world3_simulation(year_min=2000, year_max=2100, prev_run_data=dict_for_run_2, k_index=dict_for_run_2["world_props"]["k"])
    

    # Plot the combined results
    plot_world_variables(
        world3_second.time,
        [world3_second.fpc, world3_second.fr, world3_second.pop, world3_second.ppolx],
        ["FPC", "FR", "POP", "PPOLX"],
        [[0, 2e3], [0, 5], [0, 10e9], [0, 20]],
        figsize=(10, 7),
        title="World3 Simulation from 1900 to 2200, paused at 2000"
    )
    plt.show()

if __name__ == "__main__":
    main()

