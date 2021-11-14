import pandas as pd
from modules.asteroid import Asteroid
from modules.asterankapi import get_filtered_dictionaries

class SimulationManager:
    '''
    the goal of this class is to hold all relevant objects and data so they can interact with eachother
    '''
    def __init__(self):
        '''
        both these will be name: object
        '''
        self.asteroids = {}
        self.spaceships = {}

    def get_asteroids_from_csv(self, csv_file_path):
        '''
        this function will take in a csv file path string
        and populate the asteroids
        '''
        asteriod_df = pd.read_csv(csv_file_path)
        for row in asteriod_df.itertuples(index=False):
            self.asteroids[row._0] = Asteroid(row._5, row.Eccentricity, row._4)

    def get_asteroids_from_api(self, list_of_constraints):
        '''
        function will create asteroid objects inside the sim manager from the constraints given
        and then directly from the api
        '''
        print(list_of_constraints[1])
        list_of_asteroids = get_filtered_dictionaries(list_of_constraints[0], list_of_constraints[1], 
                                                      list_of_constraints[2], list_of_constraints[3], 
                                                      list_of_constraints[4])
        for asteroid_dict in list_of_asteroids:
            self.asteroids[asteroid_dict['Object Name']] = Asteroid(asteroid_dict['Semi-major Axis (AU)'], asteroid_dict['Eccentricity'], asteroid_dict['Inclination (degrees)'])

    def add_spaceship_for_asteroid(self, spaceship_object, asteroid_name):
        '''
        this will create a spaceship designated for a specific asteroid
        '''
        self.spaceships[asteroid_name] = spaceship_object

    def do_mission_to_asteroid_apoperi(self, asteroid_name):
        '''
        do a mission for a singular asteroid for apoapsis then periapsis
        '''
        asteroid_obj = self.asteroids[asteroid_name]
        spaceship_obj = self.spaceships[asteroid_name]
        spaceship_obj.match_apoapsis_then_periapsis(asteroid_obj.periapsis_m, asteroid_obj.apoapsis_m)

    def do_mission_to_asteroid_periapo(self, asteroid_name):
        '''
        do a mission for a singular asteroid for periapsis then apoapsis
        '''
        asteroid_obj = self.asteroids[asteroid_name]
        spaceship_obj = self.spaceships[asteroid_name]
        spaceship_obj.match_periapsis_then_apoapsis(asteroid_obj.periapsis_m, asteroid_obj.apoapsis_m)

    def reset_all_spaceships(self):
        '''
        reset all spaceships to earth orbit
        '''
        for spaceship in self.spaceships.values():
            spaceship.reset_spaceship()
