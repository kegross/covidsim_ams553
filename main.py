import numpy as np
import math


"""
Generates a random variate to represent how long until a person would catch covid given
- num_infected: the number of people infected
- office_density: the people per area in the office
- ismasked: if the office is masked or not
- isvent: if the office is well ventilated (hepa filters/good mechanical system)
ismasked, and isvent default to false (no mitigation measures taken)
"""
def rv_time_until_covid(num_infected, office_density, ismasked=False, isvent=False):
    if num_infected == 0:
        return math.inf
    if ismasked and isvent:
        return rv_covid_masks_vent(num_infected, office_density)
    elif ismasked:
        return rv_covid_only_masks(num_infected, office_density)
    elif isvent:
        return rv_covid_only_vent(num_infected, office_density)
    else:
        return rv_covid_normal(num_infected, office_density)


"""
Generates a random variate to represent how long until a person would catch covid given
- num_infected: the number of people infected
- office_density: the people per area in the office
- masks and good ventilation are in use
"""
def rv_covid_masks_vent(num_infected, office_density):
    # TODO: rv if all are masked & ventilation good
    return math.inf


"""
Generates a random variate to represent how long until a person would catch covid given
- num_infected: the number of people infected
- office_density: the people per area in the office
- masks are in use
"""
def rv_covid_only_masks(num_infected, office_density):
    # TODO: rv if all are masked
    return math.inf


"""
Generates a random variate to represent how long until a person would catch covid given
- num_infected: the number of people infected
- office_density: the people per area in the office
- good ventilation is in use
"""
def rv_covid_only_vent(num_infected, office_density):
    # TODO: rv if ventilation good
    return math.inf


"""
Generates a random variate to represent how long until a person would catch covid given
- num_infected: the number of people infected
- office_density: the people per area in the office
"""
def rv_covid_normal(num_infected, office_density):
    # TODO: rv if no measures taken
    return math.inf


"""
Generates a random variate to represent how long a person spends in the office given
- average_shift: the average shift length in minutes
- standard_dev: the standard deviation in amount of time spend in the office
This is assumed to be a standard normal distribution
If no values are given, default values of 8 hours per day and a 15 minute standard deviation are used
"""
def rv_time_in_office(average_shift=480, standard_dev=15):
    return np.random.normal(average_shift, standard_dev)


"""
Runs a simulation to generate the number of employees who would be infected after one workday given
- num_in_office: the number of people in the office
- office_density: the people per area in the office
- outside_infection_rate: the rate at which people come into the office with covid
- ismasked: if the office is masked or not
- isvent: if the office is well ventilated (hepa filters/good mechanical system)
- run_as_one: if true, run as if exactly one person in the office has covid
outside_infection_rate has a default of 0.0015, which is the current rate of covid in adults in the united states
ismasked, and isvent default to false (no mitigation measures taken)
run_as_one defaults to false (run with current infection rates)
"""
def run_simulation(num_in_office, office_density, outside_infection_rate=0.0015, ismasked=False, isvent=False, run_as_one=False, ave_shift=480, standard_dev=15):
    if run_as_one:
        number_infected_in_office = 0
        for i in range(num_in_office):
            if rv_time_in_office(ave_shift,standard_dev) > rv_time_until_covid(1,office_density,ismasked,isvent):
                number_infected_in_office += 1
        return number_infected_in_office
    else:
        expected_number_infected = 0
        for i in range(num_in_office):
            k = i+1
            n = num_in_office
            p = outside_infection_rate
            probability = math.comb(n,k)*(p**k)*((1-p)**k)  # binomial distribution
            number_infected_in_office = 0
            for j in range(num_in_office):
                if rv_time_in_office(ave_shift, standard_dev) > rv_time_until_covid(k, office_density, ismasked, isvent):
                    number_infected_in_office += 1
            expected_number_infected += probability*number_infected_in_office
        return expected_number_infected


"""
Main function, starts simulation according to preferences
"""
def main_allnumbers(num_in_office, office_density, outside_infection_rate=0.0015, average_shift=480, standard_dev=15):
    print("Given that: ")
    print("The number of people in the office is " + str(num_in_office))
    print("The density of people in the office (people per space) is " + str(office_density))
    print("The outside infection rate is " + str(outside_infection_rate))
    print("The standard length of shift is " + str(average_shift))
    print("The standard deviation of length of shift is " + str(standard_dev))

    number_of_runs = 50

    without_measures = 0
    for i in range(number_of_runs):
        without_measures += run_simulation(num_in_office, office_density, outside_infection_rate, ave_shift=average_shift, standard_dev=standard_dev)
    without_measures = without_measures/number_of_runs
    print("The expected number of people with covid after one day in office is " + str(without_measures) + " when no mitigation strategies are used.")

    masking = 0
    for i in range(number_of_runs):
        masking += run_simulation(num_in_office, office_density, outside_infection_rate, ismasked=True, ave_shift=average_shift, standard_dev=standard_dev)
    masking = masking/number_of_runs
    print("The expected number of people with covid after one day in office is " + str(masking) + " when masks are used in the office.")

    ventilation = 0
    for i in range(number_of_runs):
        ventilation += run_simulation(num_in_office, office_density, outside_infection_rate, isvent=True, ave_shift=average_shift, standard_dev=standard_dev)
    ventilation = ventilation/number_of_runs
    print("The expected number of people with covid after one day in office is " + str(ventilation) + " when the office uses good ventilation systems.")

    chance = 1 # chance a person does not know they have covid (goes into office)
    quarantine = 0
    for i in range(number_of_runs):
        quarantine += run_simulation(num_in_office, office_density, outside_infection_rate*chance, ave_shift=average_shift, standard_dev=standard_dev)
    quarantine = quarantine/number_of_runs
    print("The expected number of people with covid after one day in office is " + str(quarantine) + " when the office encourages quarantining when an employee is feeling symptoms.")

    all_measures = 0
    for i in range(number_of_runs):
        all_measures += run_simulation(num_in_office, office_density, outside_infection_rate*chance, True, True, False, average_shift, standard_dev)
    all_measures = all_measures/number_of_runs
    print("The expected number of people with covid after one day in office is " + str(all_measures) + " when the office uses all mentioned mitigation strategies.")


def main_runasone(num_in_office, office_density, outside_infection_rate=0.0015, average_shift=480, standard_dev=15):
    print("Given that: ")
    print("The number of people in the office is " + str(num_in_office))
    print("The density of people in the office (people per space) is " + str(office_density))
    print("The outside infection rate is " + str(outside_infection_rate))
    print("The standard length of shift is " + str(average_shift))
    print("The standard deviation of length of shift is " + str(standard_dev))

    number_of_runs = 50

    print("Here are the numbers when the simulation is run with exactly one person coming into the office with covid: ")

    without_measures = 0
    for i in range(number_of_runs):
        without_measures += run_simulation(num_in_office, office_density, outside_infection_rate, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)
    without_measures = without_measures / number_of_runs
    print("The expected number of people with covid after one day in office is " + str(
        without_measures) + " when no mitigation strategies are used.")

    masking = 0
    for i in range(number_of_runs):
        masking += run_simulation(num_in_office, office_density, outside_infection_rate, ismasked=True, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)
    masking = masking / number_of_runs
    print("The expected number of people with covid after one day in office is " + str(
        masking) + " when masks are used in the office.")

    ventilation = 0
    for i in range(number_of_runs):
        ventilation += run_simulation(num_in_office, office_density, outside_infection_rate, isvent=True, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)
    ventilation = ventilation / number_of_runs
    print("The expected number of people with covid after one day in office is " + str(
        ventilation) + " when the office uses good ventilation systems.")

    chance = 1  # chance a person does not know they have covid (goes into office)
    quarantine = 0
    for i in range(number_of_runs):
        quarantine += run_simulation(num_in_office, office_density, outside_infection_rate * chance, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)
    quarantine = quarantine / number_of_runs
    print("The expected number of people with covid after one day in office is " + str(
        quarantine) + " when the office encourages quarantining when an employee is feeling symptoms.")

    all_measures = 0
    for i in range(number_of_runs):
        all_measures += run_simulation(num_in_office, office_density, outside_infection_rate * chance, True, True, True, average_shift, standard_dev)
    all_measures = all_measures / number_of_runs
    print("The expected number of people with covid after one day in office is " + str(
        all_measures) + " when the office uses all mentioned mitigation strategies.")

# TODO: stats on output?

def main():
    num_in_office = 0
    office_density = 0
    outside_infection_rate = 0.0015
    average_shift = 480
    standard_dev = 15
    main_allnumbers(num_in_office, office_density, outside_infection_rate, average_shift, standard_dev)
    main_runasone(num_in_office, office_density, outside_infection_rate, average_shift, standard_dev)


if __name__ == '__main__':
    main()