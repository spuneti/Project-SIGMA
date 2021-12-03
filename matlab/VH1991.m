%% This is my attempt to design one of THOSE trajectories. Screw this project

clear all

%% Getting the speed based off the drop off orbit
mu_earth = 3.986 * 10 ^14;
earth_r = 6371 * 1000;
perigee = earth_r + 300*1000;
apogee = earth_r + 35600 *1000;
a = perigee/2 + apogee /2;
orbit_energy = - mu_earth / 2 / a;

current_r = perigee;

speed_at_perigee_in_earths_orbit = sqrt(2 * (mu_earth/current_r + orbit_energy));


%% Sphere of Influence at apogee and perigee of asteroid

mass_sun = 1.989 * 10 ^ 30;
mass_asteroid_tons = (27) * 85 * 10 ^ 6; % 27 comes from 3 times the size and r^3 is in volume equation
mass_asteroid = mass_asteroid_tons * 907.18;
ASTRONOMICAL_UNIT_METERS = 149597870700;
asteroid_apogee = 1.3 * ASTRONOMICAL_UNIT_METERS;
asteroid_perigee = .97 * ASTRONOMICAL_UNIT_METERS;

asteroid_SOI_at_perigee = asteroid_perigee * (mass_asteroid / mass_sun) ^ (2/5);
asteroid_SOI_at_apogee = asteroid_apogee * (mass_asteroid / mass_sun) ^ (2/5);

%% Getting speeds relative

earth_speed_around_sun = 29780; % km/s
mu_sun = 1.32712440018 * 10 ^ 20;
a_asteroid = asteroid_perigee/2 + asteroid_apogee /2;
eccentricity_asteroid = 1 - asteroid_perigee/a_asteroid;
orbit_energy = - mu_sun / 2 / a_asteroid;
current_r = .98 * ASTRONOMICAL_UNIT_METERS;
V = sqrt(2 * (mu_sun/current_r + orbit_energy));

speed_necessary_when_leaving_earth_SOI = V - earth_speed_around_sun;




R_SOI_METERS = 924811699;
a_hyperbolic = -1 * mu_earth / (2 * (speed_necessary_when_leaving_earth_SOI ^ 2 / 2 - mu_earth / R_SOI_METERS));
orbit_energy = - mu_earth / 2 / a_hyperbolic;

%current_r = R_SOI_METERS / 5;
first_burn_to_leave_earth_SOI_and_start_trajectory = sqrt(2 * (mu_earth/(perigee) + orbit_energy)) - speed_at_perigee_in_earths_orbit;

%% Now we will need to do some semi major axis phasing in order to reach it. 

% we are now roughly 5 days behind, so we must phase our orbit so that we
% can catch up we can do this in as much as 2 rotations probably 

orbital_period_asteroid = 2 * pi * sqrt( a_asteroid^3 / mu_sun);
desired_phase_days = 5;
desired_phase_seconds = desired_phase_days * (24*60*60);
orbital_period_necessary = orbital_period_asteroid - desired_phase_seconds;

% this burn is going to happen at perigee of the orbit, so we know that is
% constant, must find necessary semi major axis and then apogee and find dv
% change

necessary_semi_major_axis = (mu_sun * ((orbital_period_necessary / (2 * pi)) ^ 2 )) ^ (1/3);

necessary_speed_at_perigee_for_phasing = sqrt(2 * mu_sun * (-1/2/necessary_semi_major_axis + 1 / asteroid_perigee));
current_speed_at_perigee_before_phasing = sqrt(2 * mu_sun * (-1/2/a_asteroid + 1 / asteroid_perigee));

% now we can find the second burn
second_burn_to_phase_orbit = necessary_speed_at_perigee_for_phasing - current_speed_at_perigee_before_phasing;

% third burn for docking with asteroid we have now phased and should
% docking with the asteroid exactly on our go around, will need to burn to
% rematch the asteroids orbit
third_burn_to_dock_with_asteroid = -1 * second_burn_to_phase_orbit;

%% We have now arrived at the asteroid, doing some sphere of influence calcs just cause

mu_asteroid = 6.67 * 10 ^ -11 * mass_asteroid;
sample_orbitting_speed_around_asteroid_apogee = sqrt(2 * mu_asteroid * (-1/2/(1/10*asteroid_SOI_at_apogee) + 1 / (1/10*asteroid_SOI_at_apogee)));
sample_orbitting_speed_around_asteroid_perigee = sqrt(2 * mu_asteroid * (-1/2/(1/7*asteroid_SOI_at_perigee) + 1 / (1/7*asteroid_SOI_at_perigee)));

seconds_in_a_rev_on_asteroid = (2.24 * 60 * 60);
distance_on_surface = pi* .9 * 1000; % meters
surface_speed_on_asteroid = distance_on_surface / seconds_in_a_rev_on_asteroid;

%% After surveying asteroid, we will dock and and mine it 

% we are going to mine it for approximately one orbital period
% (orbital_period_asteroid)

%% We must now phase off the asteroid, we will do this in two seperate burns
% The first burn will be covering the majority of the period phasing
% The second burn will cover exactly matching up with earths trajectory for
% crash

total_phasing_needed_days = 58; % days

% this comes from the fact that we will intersect earth at about 280-300
% true anomaly on the second rotation. Calcs will be done as though they
% are meeting at perigee, so the TOF needed to phase would be actually
% slightly more. Adding a correction factor of .1 here to account for that
total_phasing_needed_with_correction_days = total_phasing_needed_days * 1.1; 

phasing_per_orbit_days = total_phasing_needed_with_correction_days / 2; % dividing by two here cause we will do it in two orbits

phasing_per_orbit_seconds = phasing_per_orbit_days * (24*60*60);

% adding additional time to the orbit cause need to phase higher
necessary_orbital_period_phase2 = orbital_period_asteroid + phasing_per_orbit_seconds;
necessary_semimajor_axis_2 = (mu_sun * ((necessary_orbital_period_phase2 / (2 * pi)) ^ 2 )) ^ (1/3);

necessary_speed_after_phasing_2 = sqrt(2 * mu_sun * (-1/2/necessary_semimajor_axis_2 + 1 / asteroid_perigee));

fourth_burn_to_phase_orbit_higher_and_hit_earth_in_2_years = necessary_speed_after_phasing_2 - current_speed_at_perigee_before_phasing;

% Here is a check to make sure that we will roughly hit earth with this new
% semi major axis, since it is slightly out of earths intersection
eccentricity_of_phasing_orbit_2 = 1 - asteroid_perigee/necessary_semimajor_axis_2; 
r_at_earth_intersection_AU = necessary_semimajor_axis_2 * (1 - eccentricity_of_phasing_orbit_2^2) / (1 + eccentricity_of_phasing_orbit_2 * cos(pi/4)) / ASTRONOMICAL_UNIT_METERS;

% orbit ends up being 1.0163 AU!!! Which is very close to earth at time of
% intersection

%% Doing some orbit insertion math 

ecliptic_angle = 23.4; % degrees

% the way the earth is rotated, leaving with a 23.4 inclination, would put
% you at 0 inclination, just basic angle math to find what inclination to
% leave earth SOI with.

asteroid_inclination_at_time_of_earth_arrival = -13.91; % degrees

necessary_exit_inclination = ecliptic_angle + asteroid_inclination_at_time_of_earth_arrival;



%% Getting total dv and printing outputs and other necessary things

total_dV_meters_per_second = abs(first_burn_to_leave_earth_SOI_and_start_trajectory) + abs(second_burn_to_phase_orbit) + abs(third_burn_to_dock_with_asteroid) + abs(fourth_burn_to_phase_orbit_higher_and_hit_earth_in_2_years);

disp('DISPLAYING NECESSARY INFORMATION')
disp('(All burns in m/s)')
disp('--------------------------------')





disp('First burn: ' + string(first_burn_to_leave_earth_SOI_and_start_trajectory))
disp('Second burn: ' + string(second_burn_to_phase_orbit))
disp('Third burn: ' + string(third_burn_to_dock_with_asteroid))
disp('Fourth burn: ' + string(fourth_burn_to_phase_orbit_higher_and_hit_earth_in_2_years))
disp('Total dV needed: ' + string(total_dV_meters_per_second))
disp('Total dV needed with 10% margin: ' + string(total_dV_meters_per_second*1.1))



