import numpy as np
import math
import matplotlib.pyplot as plt

from constants import MU_SUN

mu_sun = 1.32712440018 * 10 ** 20
au = 1.496 * 10 ** 11

def get_perigee_apogee_from_semimajor(semimajor_axis_m, eccentricity):
    '''
    this function returns perigee, apogee from sma and e
    '''
    return semimajor_axis_m * (1 - eccentricity), semimajor_axis_m * (1 + eccentricity)

earth_semimajor = 1 * au
earth_perigee, earth_apogee = get_perigee_apogee_from_semimajor(earth_semimajor, .0167)

def solve_for_speed_using_energy(orbit_energy, current_r):
    '''
    current r is semi major
    '''
    return math.sqrt((orbit_energy + mu_sun / current_r) * 2)

def change_perigee_from_apogee_solar_system(cur_perigee, cur_apogee, new_perigee):
    '''
    all altitude in m
    '''
    cur_perigee_total = cur_perigee
    cur_apogee_total = cur_apogee
    new_perigee_total = new_perigee
    current_orbital_energy = -1 * mu_sun / ( cur_apogee_total + cur_perigee_total)
    new_orbital_energy = -1 * mu_sun / ( cur_apogee_total + new_perigee_total)
    cur_speed = solve_for_speed_using_energy(current_orbital_energy, cur_apogee_total)
    print(cur_speed)
    new_speed = solve_for_speed_using_energy(new_orbital_energy, cur_apogee_total)
    print(new_speed)
    return new_speed - cur_speed

def change_apogee_from_perigee_solar_system(cur_perigee, cur_apogee, new_apogee):
    '''
    all altitude in m
    '''
    cur_perigee_total = cur_perigee
    cur_apogee_total = cur_apogee
    new_apogee_total = new_apogee
    current_orbital_energy = -1 * mu_sun / ( cur_apogee_total + cur_perigee_total)
    print(current_orbital_energy)
    new_orbital_energy = -1 * mu_sun / ( cur_perigee_total + new_apogee_total)
    cur_speed = solve_for_speed_using_energy(current_orbital_energy, cur_perigee_total)
    print(cur_speed)
    new_speed = solve_for_speed_using_energy(new_orbital_energy, cur_perigee_total)
    print(new_speed)
    return new_speed - cur_speed


###### TESTING ######

ML1989_perigee, ML1989_apogee = get_perigee_apogee_from_semimajor(1 * au, .5) 


first_burn = change_apogee_from_perigee_solar_system(.95* au * (1-.137), .95 * au * (1.137), 1.5 * au)
second_burn = change_perigee_from_apogee_solar_system(earth_semimajor, ML1989_apogee, ML1989_perigee)
print(first_burn, second_burn)
print(first_burn + second_burn)
'''
first_burn = change_perigee_from_apogee_solar_system(earth_semimajor, earth_semimajor, ML1989_perigee)
second_burn = change_apogee_from_perigee_solar_system(earth_semimajor, ML1989_perigee, ML1989_apogee)
print(first_burn, second_burn)
print(first_burn + second_burn)
'''
dv_burn = math.sqrt(2 * MU_SUN * (1/(2 * 1.137)))