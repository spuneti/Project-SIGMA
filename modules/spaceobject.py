from modules.constants import ASTRONOMICAL_UNIT_METERS

class SpaceObject:
    '''
    General class for an object floating in space with a defined as an 
    orbital plane around the sun
    '''
    def __init__(self, semimajor_axis_au, eccentricity, inclination):
        '''
        semimajor_axis_au - semi major axis of asteroid in AU 
        eccentricity - eccentricity of asteroids orbit
        inclination - incination of the orbit in degrees, relative to sun
        '''
        self.sma_au = semimajor_axis_au
        self.eccentricity = eccentricity
        self.sma_m = self.sma_au * ASTRONOMICAL_UNIT_METERS
        self.periapsis_m, self.apoapsis_m = self.get_perigee_apogee_from_semimajor_eccentricity(self.sma_m, eccentricity)
        self.inclination = inclination


    def get_perigee_apogee_from_semimajor_eccentricity(self, semimajor_axis_m, eccentricity):
        '''
        this function returns perigee, apogee from sma and e
        '''
        return semimajor_axis_m * (1 - eccentricity), semimajor_axis_m * (1 + eccentricity)