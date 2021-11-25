from modules.spaceobject import SpaceObject
from modules.constants import ASTRONOMICAL_UNIT_METERS, MU_SUN

import math
import numpy as np

class Spaceship(SpaceObject):
    '''
    Spaceship will have additional functions to help it do burns
    '''
    def __init__(self, semimajor_axis_au, eccentricity, inclination, grav_param):
        '''
        semimajor_axis_au - semi major axis of asteroid (AU)
        eccentricity - eccentricity of asteroids orbit
        inclination - inclination
        grav_param - gravitational parameter that the spaceship respects (meters^2/sec^2)
        '''
        
        SpaceObject.__init__(self, semimajor_axis_au, eccentricity, inclination)  # Call parent class constructor.
        self.mu = grav_param
        self.set_current_orbital_energy()
        self.list_of_dv_maneuvers = np.array([]) # this list will contain all deltaV needs of maneuvers done (m/s)
        self.list_of_TOF_seconds = np.array([]) # this list will be filled with all TOFs of maneuvers (seconds)
        self.list_of_burn_descriptions = []

    
    def add_dv_requirement(self, dv_req):
        '''
        this will add a deltaV to the current deltaV
        '''
        self.dv_requirement += np.abs(dv_req)

    def get_half_period(self):
        '''
        half of the period of an orbit is the TOF of a maneuver with the new parameters
        returns the half the period of the current orbit spaceship is on
        '''
        return math.pi * math.sqrt(self.sma_m ** 3 / MU_SUN)

    def get_total_dv(self):
        '''
        will return the total amount of deltaV required to do the mission (m/s)
        '''
        dv_mag = [np.abs(dv) for dv in self.list_of_dv_maneuvers]
        return np.sum(dv_mag)

    def set_current_orbital_energy(self):
        '''
        this function will set the orbital energy attribute from the
        current semi major axis
        '''
        self.orbital_energy = -1 * self.mu / ( self.periapsis_m + self.apoapsis_m)
    
    def update_orbital_characteristics(self):
        '''
        this function will set the semi major axis attributes, eccentricity,
        and orbital energy to the current apoapsis and periapsis. Either one of these
        will be updated in a different function
        '''
        self.sma_m = (self.apoapsis_m + self.periapsis_m) / 2
        self.sma_au = self.sma_m / ASTRONOMICAL_UNIT_METERS
        self.eccentricity = 1 - self.periapsis_m / self.sma_m
        self.set_current_orbital_energy()

    def reset_spaceship(self):
        '''
        will reset the spaceship to orbiting earth with 0 dv and tof
        '''
        self.apoapsis_m = ASTRONOMICAL_UNIT_METERS
        self.periapsis_m = ASTRONOMICAL_UNIT_METERS
        self.list_of_dv_maneuvers = np.array([]) # this list will contain all deltaV needs of maneuvers done (m/s)
        self.list_of_TOF_seconds = np.array([]) # this list will be filled with all TOFs of maneuvers (seconds)


    def solve_for_speed_using_energy(self, current_r):
        '''
        current r is semi major
        '''
        return math.sqrt((self.orbital_energy + self.mu / current_r) * 2)

    def dv_change_periapsis_from_apoapsis(self, new_periapsis):
        '''
        your new desired periapsis in meters

        returns:
         - value of dv required (can be positive or negative, not just magnitude)
        '''
        # updating orbital chacteristics incase they werent before. 
        self.update_orbital_characteristics()
        cur_speed = self.solve_for_speed_using_energy(self.apoapsis_m)

        # updating apoapsis and re-updating orbit
        self.periapsis_m = new_periapsis
        self.update_orbital_characteristics()
        new_speed = self.solve_for_speed_using_energy(self.apoapsis_m)

        # taking difference in velocities
        dv_req = new_speed - cur_speed
        self.list_of_dv_maneuvers = np.append(self.list_of_dv_maneuvers, dv_req)
        return dv_req

    def dv_change_apoapsis_from_periapsis(self, new_apoapsis):
        '''
        your new desired apoapsis in meters

        returns:
         - value of dv required (can be positive or negative, not just magnitude)
        '''
        # updating orbital chacteristics incase they werent before. 
        self.update_orbital_characteristics()
        cur_speed = self.solve_for_speed_using_energy(self.periapsis_m)

        # updating apoapsis and re-updating orbit
        self.apoapsis_m = new_apoapsis
        self.update_orbital_characteristics()
        new_speed = self.solve_for_speed_using_energy(self.periapsis_m)

        # taking difference in velocities
        dv_req = new_speed - cur_speed
        self.list_of_dv_maneuvers = np.append(self.list_of_dv_maneuvers, dv_req)
        return dv_req

    def match_periapsis_then_apoapsis(self, new_periapsis_m, new_apoapsis_m):
        '''
        this will first burn at apoapsis of the current orbit to match periapsis
        and will then burn at its new apoapsis to change periapsis and completely 
        match orbit.
        This function will also append the TOF of the maneuver to the TOF list
        '''
        # first burning to match periapsis to target
        self.dv_change_periapsis_from_apoapsis(new_periapsis_m)

        # adding the TOF from apoapsis to periapsis of new orbit
        self.list_of_TOF_seconds = np.append(self.list_of_TOF_seconds, self.get_half_period())

        # burning to fully match target orbit
        self.dv_change_apoapsis_from_periapsis(new_apoapsis_m)

    def match_apoapsis_then_periapsis(self, new_periapsis_m, new_apoapsis_m):
        '''
        this will first burn at periapsis of the current orbit to match apoapsis
        and will then burn at its new periapsis to change apoapsis and completely 
        match orbit.
        This function will also append the TOF of the maneuver to the TOF list
        '''
        # first burning to match periapsis to target
        self.dv_change_apoapsis_from_periapsis(new_apoapsis_m)

        # adding the TOF from periapsis to apoapsis of new orbit
        self.list_of_TOF_seconds = np.append(self.list_of_TOF_seconds, self.get_half_period())

        # burning to fully match target orbit
        self.dv_change_periapsis_from_apoapsis(new_periapsis_m)
