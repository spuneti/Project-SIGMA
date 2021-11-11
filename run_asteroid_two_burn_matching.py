from modules.asteroid import Asteroid
from modules.constants import MU_SUN, ASTRONOMICAL_UNIT_METERS
from modules.spaceship import Spaceship
from modules.simulationmanager import SimulationManager

import numpy as np
import math 
import pandas as pd

def populate_asteroid_objects(simulation_manager, asteroid_csv_path):
    '''
    this function will take in a simulation manager
    and call the simulation managers function
    to read asteroids in from a csv
    '''
    simulation_manager.get_asteroids_from_csv(asteroid_csv_path)

def create_spaceship_for_each_asteroid_at_earth(simulation_manager):
    '''
    this function will create a spaceship for each asteroid
    '''
    asteroids = simulation_manager.asteroids
    for asteroid in asteroids.keys():
        new_spaceship = Spaceship(ASTRONOMICAL_UNIT_METERS, 0, 0, MU_SUN)
        simulation_manager.add_spaceship_for_asteroid(new_spaceship, asteroid)

def populate_spaceships_and_asteroids(simulation_manager, asteroid_csv_path):
    '''
    will populate the sim manager with relevant asteroids and spaceships
    '''
    populate_asteroid_objects(simulation_manager, asteroid_csv_path)
    create_spaceship_for_each_asteroid_at_earth(simulation_manager)

def do_all_missions_apo_peri(simulation_manager):
    '''
    do all missions for the spacecraft apo peri method
    '''
    target_names = []
    target_f_b = []
    target_s_b = []
    target_t_dv = []
    target_tof = []
    method = []

    for asteroid_name in simulation_manager.asteroids.keys():
        simulation_manager.do_mission_to_asteroid_apoperi(asteroid_name)

    for iter1, target_name in enumerate(simulation_manager.spaceships.keys()):
        spacecraft = simulation_manager.spaceships[target_name]
        print(target_name)
        print(spacecraft.list_of_dv_maneuvers)
        target_names.append(target_name)
        target_f_b.append(spacecraft.list_of_dv_maneuvers[0])
        target_s_b.append(spacecraft.list_of_dv_maneuvers[1])
        target_t_dv.append(spacecraft.get_total_dv())
        target_tof.append(spacecraft.list_of_TOF_seconds[0]/(60*60*24))
        method.append('Apoapsis_Match_First')

    df = pd.DataFrame({'Asteroid Name': target_names, 'First Burn (m/s)': target_f_b, 'Second Burn (m/s)': target_s_b, 'Total Burn (m/s)': target_t_dv,
                        'Total TOF (days)':target_tof, 'Burn Method': method})

    df.to_csv('outputs/apoperi.csv')

def do_all_missions_peri_apo(simulation_manager):
    '''
    do all missions for the spacecraft peri apo method
    '''
    target_names = []
    target_f_b = []
    target_s_b = []
    target_t_dv = []
    target_tof = []
    method = []

    for asteroid_name in simulation_manager.asteroids.keys():
        simulation_manager.do_mission_to_asteroid_periapo(asteroid_name)

    for iter1, target_name in enumerate(simulation_manager.spaceships.keys()):
        spacecraft = simulation_manager.spaceships[target_name]
        print(target_name)
        print(spacecraft.list_of_dv_maneuvers)
        target_names.append(target_name)
        target_f_b.append(spacecraft.list_of_dv_maneuvers[0])
        target_s_b.append(spacecraft.list_of_dv_maneuvers[1])
        target_t_dv.append(spacecraft.get_total_dv())
        target_tof.append(spacecraft.list_of_TOF_seconds[0]/(60*60*24))
        method.append('Periapsis_Match_First')

    df = pd.DataFrame({'Asteroid Name': target_names, 'First Burn (m/s)': target_f_b, 'Second Burn (m/s)': target_s_b, 'Total Burn (m/s)': target_t_dv,
                        'Total TOF (days)':target_tof, 'Burn Method': method})

    df.to_csv('outputs/periapo.csv')

if __name__ == '__main__':
    '''
    going to run all main functions and produce outputs.
    '''

    ############### INPUTS ################
    asteroid_file_path = 'inputs/wider_limits_asteroids.csv'

    # Creating sim manager
    simulation_manager = SimulationManager()

    # Adding Spaceships and Asteroids
    populate_spaceships_and_asteroids(simulation_manager, asteroid_file_path)

    # Reseting all spaceships
    simulation_manager.reset_all_spaceships()

    # Doing the apo peri method first
    do_all_missions_apo_peri(simulation_manager)

    # Reseting Spaceships
    simulation_manager.reset_all_spaceships()

    # doing per apo method next
    do_all_missions_peri_apo(simulation_manager)











'''
ryugu = Asteroid(1, .5, 20)

takeoff = Spaceship(.95, .137, 2, MU_SUN)


print(takeoff.dv_change_apoapsis_from_periapsis(ryugu.apoapsis_m))


print(takeoff.dv_change_periapsis_from_apoapsis(ryugu.periapsis_m))
print ( '--------')
takeoff2 = Spaceship(.6, 1/6, 2, MU_SUN)
print(takeoff2.dv_change_periapsis_from_apoapsis(ryugu.periapsis_m))
print(takeoff2.dv_change_apoapsis_from_periapsis(ryugu.apoapsis_m))
print(takeoff2.list_of_dv_maneuvers)
print(takeoff2.list_of_TOF_seconds)
#print(f'Sup dwag. My dv is {} and rob is {}', tale)
print ( '--------')
takeoff3 = Spaceship(.95, .137, 2, MU_SUN)
takeoff3.match_apoapsis_then_periapsis(ryugu.periapsis_m, ryugu.apoapsis_m)
print(takeoff3.list_of_dv_maneuvers)
print(takeoff3.list_of_TOF_seconds)
print(takeoff3.get_total_dv())
'''