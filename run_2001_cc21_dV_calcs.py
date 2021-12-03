from modules.constants import MU_EARTH,  MU_SUN, ASTRONOMICAL_UNIT_METERS, MASS_EARTH, MASS_SUN, RADIUS_EARTH_METERS
from modules.spaceship import Spaceship
from modules.asteroid import Asteroid

import copy as c

import numpy as np
import math

# Creating asteroid object with its basic characteristics
cc21 = Asteroid(1.032286365, 0.219154082, 4.808353727)

# Creating asteroid spaceship in earth SOI
cc21_ship = Spaceship(1, 0, 0, MU_EARTH)

# Calculating Earth SOI
R_SOI_METERS = ASTRONOMICAL_UNIT_METERS * ((MASS_EARTH / MASS_SUN) ** .4)

# 2nd_stage_drop_off_orbit_calcs putting into GTO orbit
second_stage_dropoff_perigee_m = 300 * 1000 + RADIUS_EARTH_METERS
second_stage_dropoff_apogee_m = 35600 * 1000 + RADIUS_EARTH_METERS

# Updating our craft to have these characteristics
cc21_ship.periapsis_m = second_stage_dropoff_perigee_m
cc21_ship.apoapsis_m = second_stage_dropoff_apogee_m
cc21_ship.update_orbital_characteristics()

################################ CALCS FOR LEAVING EARTH SOI #####################################

# From previous calcs we know the first burn and second burn, still need to do inclination burn
first_burn_leaving_earth = 1658.447782
second_burn_arriving_asteroid = -1523.303012

# Getting interplanetary semi major axis for transfer from our resting orbit
interplanetary_semimajor_m = -1 * MU_EARTH / (2 * (first_burn_leaving_earth ** 2 / 2 - MU_EARTH / R_SOI_METERS))

# Getting its current velocity at perigee of its drop off orbit
current_velocity_at_earth_2nd_stage_dropoff_perigee = cc21_ship.solve_for_speed_using_energy(cc21_ship.periapsis_m)

# Getting the needed interplanetary velocity
needed_velocity_at_earth_2nd_stage_dropoff_perigee = math.sqrt((-1 * MU_EARTH / 2 / interplanetary_semimajor_m + MU_EARTH / cc21_ship.periapsis_m) * 2)

# Getting first burn
first_burn_to_leave_earth_SOI_and_to_asteroid = needed_velocity_at_earth_2nd_stage_dropoff_perigee - current_velocity_at_earth_2nd_stage_dropoff_perigee
TOF_leaving_earth_SOI = 425542 # Correct got from interpolating velocities in time intervals

############################ CALCS FOR HELIOCENTRIC TOWARDS ASTEROID ############################

# Creating dummy Spaceship just to find earth velocity around sun
earth = Spaceship(1, 0, 0, MU_SUN)
earth_speed_around_sun = earth.solve_for_speed_using_energy(ASTRONOMICAL_UNIT_METERS)

# We are now outside Earths SOI
cc21_ship.mu = MU_SUN
spaceship_velocity_relative_to_sun = earth_speed_around_sun + first_burn_leaving_earth
heliocentric_semimajor_m = -1 * MU_SUN / (2 * (spaceship_velocity_relative_to_sun ** 2 / 2 - MU_SUN / ASTRONOMICAL_UNIT_METERS))

# Getting apogee of orbit around the sun
apogee_of_heliocentric_orbit_towards_asteroid = heliocentric_semimajor_m * 2 - ASTRONOMICAL_UNIT_METERS

# Setting ship apogee and perigee and updating characteristics
cc21_ship.periapsis_m = ASTRONOMICAL_UNIT_METERS
cc21_ship.apoapsis_m = apogee_of_heliocentric_orbit_towards_asteroid
cc21_ship.update_orbital_characteristics()

# Now on transfer orbit from earth to the asteroids apogee
TOF_flying_to_asteroid_apogee = 219.1584571 * (24 * 60 * 60) # Seconds

############################ CALCS FOR ARRIVING AT ASTEROID ############################

# Now calculating second burn which will match perigee and inclincation of asteroid for a complete rendevouz
cc21_inclination = math.radians(cc21.inclination) # asteroid inc in radians

# Getting the velocity of the ship when it reaches the asteroids apogee
speed_when_arriving_at_cc21 = cc21_ship.solve_for_speed_using_energy(cc21_ship.apoapsis_m)
 
# We already know that burn necessary from previous calculations
speed_after_burn_when_arriving_at_cc21 = speed_when_arriving_at_cc21 + second_burn_arriving_asteroid

# Total burn necessary including inclination
second_burn_for_rendevouzing_cc21_combined = math.sqrt(speed_when_arriving_at_cc21 ** 2 + speed_after_burn_when_arriving_at_cc21 ** 2 - 2 * speed_when_arriving_at_cc21 * speed_after_burn_when_arriving_at_cc21 * math.cos(cc21_inclination))
second_burn_for_rendevouzing_cc21_just_perigee_match = np.abs(second_burn_arriving_asteroid)
second_burn_for_rendevouzing_cc21_just_inclination_match = second_burn_for_rendevouzing_cc21_combined - second_burn_for_rendevouzing_cc21_just_perigee_match

# Here we will mine the asteroid until the asteroid reaches 

TOF_mining_asteroid = 191 * (24 * 60 * 60) # This comes from the fact we will arrive on 1/12/2026 and leave 7/20/2026

############################ CALCS FOR LEAVING ASTEROID ############################

# We are now on the asteroids orbit, so must have its exact orbit, setting here for future calcs
cc21_ship.periapsis_m = cc21.periapsis_m
cc21_ship.update_orbital_characteristics()

# Creating dummy object to find how much the dv calc would cost if it were purely coplanar
dummy_ship = c.deepcopy(cc21_ship)

# We are leaving the cc21 at perigee, so the first thing to do will be lower the current orbits apogee to earths and 0 out the inclination ( 1 AU )
speed_at_perigee_leaving_cc21_before_burn = cc21_ship.solve_for_speed_using_energy(cc21_ship.periapsis_m)

# Setting new apogee to get the speed needed
cc21_ship.apoapsis_m = ASTRONOMICAL_UNIT_METERS
cc21_ship.update_orbital_characteristics()

# Getting the desired speed on this orbit
speed_at_perigee_leaving_cc21_after_burn = cc21_ship.solve_for_speed_using_energy(cc21_ship.periapsis_m)

# Getting the total third burn now, just planar casue not doing inclination
third_burn_for_leaving_cc21_combined = np.abs(speed_at_perigee_leaving_cc21_after_burn - speed_at_perigee_leaving_cc21_before_burn)

# We are now on the way to rendevouz with Earth 

########################## CALCS FOR ARRIVING BACK AT EARTH ##########################

# Getting the ships speed when it arrives at Earth
speed_at_apogee_arriving_earth_before_burn = cc21_ship.solve_for_speed_using_energy(cc21_ship.apoapsis_m)

# Getting the speed of the craft relative to Earth once we entre Earths sphere of influence
speed_at_edge_of_earth_SOI_on_return_rel_earth = earth_speed_around_sun - speed_at_apogee_arriving_earth_before_burn

# The ship is now back inside the sphere of influence, setting it as such 
cc21_ship.mu = MU_EARTH

# Getting apogee and perigee of ISS for later calculations necessary
perigee_ISS = 413 * 1000 + RADIUS_EARTH_METERS
apogee_ISS = 423 * 1000 + RADIUS_EARTH_METERS

# Setting the desired hyperbolic perigee to that of the ISS to make phasing into its orbit easier later.
desired_hyperbolic_return_perigee = perigee_ISS

# Setting the desired apogee of the return orbit to 3x GEO orbit. This is because the burn to get caught is very minimal and will allow us greater phasing dV later
desired_hyperbolic_return_apogee = 3 * 35600 * 1000 + RADIUS_EARTH_METERS

# Getting the speed we will currently be going, based on our hyperbolic energy, at perigee
hyperbolic_orbit_energy_on_return = speed_at_edge_of_earth_SOI_on_return_rel_earth ** 2 / 2
speed_at_hyperbolic_perigee_before_burn = math.sqrt(2 * (cc21_ship.mu / desired_hyperbolic_return_perigee + hyperbolic_orbit_energy_on_return))

# Getting the 4th burn to be done at hyperbolic perigee on the crafts return to Earth in order to get fully caught in earth SOI and park in the orbit specified above
speed_for_desired_orbit_around_earth_on_return_at_perigee = math.sqrt(2 * (cc21_ship.mu / desired_hyperbolic_return_perigee - cc21_ship.mu / (desired_hyperbolic_return_perigee + desired_hyperbolic_return_apogee)))
fourth_burn_for_getting_caught_in_earth_gravity = speed_at_hyperbolic_perigee_before_burn - speed_for_desired_orbit_around_earth_on_return_at_perigee

# Now that we have done the fourth burn, we will update the ships characteristics
cc21_ship.periapsis_m = desired_hyperbolic_return_perigee
cc21_ship.apoapsis_m = desired_hyperbolic_return_apogee
cc21_ship.update_orbital_characteristics()

########################## CALCS FOR DOCKING WITH ISS ##########################

# We will now do a 5th burn to match semi major axis of ISS, inclination burn included. Will find the necessary speed difference, and find the minimum total dv needed for the speed and inclination change combined
# Creating Dummy ISS for easy speed calcs
ISS = Spaceship(1,.2,1, MU_EARTH)
ISS.periapsis_m = perigee_ISS
ISS.apoapsis_m = apogee_ISS
ISS.update_orbital_characteristics()
speed_at_perigee_of_ISS = ISS.solve_for_speed_using_energy(perigee_ISS)

# By entering earths SOI at the exact right location, we can make our inclination line up exactly with that of the ISS, so no inclination burn is needed. RAAN and w adjustments will be needed. Not calculating for those here

# Now getting the 5th total burn, assumng we have matched inclination by a well placed earth reentry
fifth_burn_for_docking_with_ISS = speed_for_desired_orbit_around_earth_on_return_at_perigee - speed_at_perigee_of_ISS

# We already have the speed of earth that the craft must 

print('All Burns in Order')
print('------')
print(first_burn_to_leave_earth_SOI_and_to_asteroid)
print(second_burn_for_rendevouzing_cc21_combined)
print(third_burn_for_leaving_cc21_combined)
print(fourth_burn_for_getting_caught_in_earth_gravity)
print(fifth_burn_for_docking_with_ISS)



### EXPLORE MATING INCLINATION WHEN YOU GET BACK FOR BETTER BURNS

####### Doing calculations for inclination burn

# Getting velocity at moment of inclination change

#math.sqrt(2* v ** 2 * (1-cos(i)))



