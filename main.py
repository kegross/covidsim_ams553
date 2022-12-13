import numpy as np
import math
import random


"""
Generates the probability a person would catch covid given
- num_infected: the number of people infected
- office_volume: the area in the office
- time_in_office: the amount of time a person spends in the office
- ismasked: if the office is masked or not
- isvent: if the office is well ventilated (hepa filters/good mechanical system)
ismasked, and isvent default to false (no mitigation measures taken)
"""
def probability_catch_covid(num_infected, office_volume, time_in_office, ismasked=False, isvent=False):
    if num_infected == 0:
        return 0
    a = num_infected/office_volume
    b = 1.61
    if ismasked and isvent:
        a *= 0.004936
        b = 10.87
    elif ismasked:
        a *= 0.033230
        b = 1.61
    elif isvent:
        a *= 0.034039
        b = 10.87
    else:
        a *= 0.229814
        b = 1.61
    d_q = 0.49 * (a*time_in_office - a/b + (a/b)*math.exp(-b*time_in_office))
    return 1 - math.exp(-d_q)


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
- office_volume: the area in the office
- outside_infection_rate: the rate at which people come into the office with covid
- ismasked: if the office is masked or not
- isvent: if the office is well ventilated (hepa filters/good mechanical system)
- run_as_one: if true, run as if exactly one person in the office has covid
outside_infection_rate has a default of 0.0015, which is the current rate of covid in adults in the united states
ismasked, and isvent default to false (no mitigation measures taken)
run_as_one defaults to false (run with current infection rates)
"""
def run_simulation(num_in_office, office_volume, outside_infection_rate=0.0015, ismasked=False, isvent=False, run_as_one=False, ave_shift=480, standard_dev=15):
    if run_as_one:
        number_infected_in_office = 0
        for i in range(num_in_office):
            time_in_office = rv_time_in_office(ave_shift, standard_dev)
            if random.random() <= probability_catch_covid(1, office_volume, time_in_office, ismasked, isvent):
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
            for j in range(num_in_office-k):
                time_in_office = rv_time_in_office(ave_shift, standard_dev)
                if random.random() <= probability_catch_covid(k, office_volume, time_in_office, ismasked, isvent):
                    number_infected_in_office += 1
            expected_number_infected += probability*number_infected_in_office
        return expected_number_infected


"""
Main function, starts simulation according to preferences
"""
def main_allnumbers(num_in_office, office_volume, outside_infection_rate=0.0015, average_shift=480, standard_dev=15):
    print("Given that: ")
    print("The number of people in the office is " + str(num_in_office))
    print("The area of the office is " + str(office_volume))
    print("The outside infection rate is " + str(outside_infection_rate))
    print("The standard length of shift is " + str(average_shift))
    print("The standard deviation of length of shift is " + str(standard_dev))

    number_of_runs = 1000000

    without_measures = []
    for i in range(number_of_runs):
        without_measures += [run_simulation(num_in_office, office_volume, outside_infection_rate, ave_shift=average_shift, standard_dev=standard_dev)]
    without_measures_mean = np.mean(without_measures)
    without_measures_std = np.std(without_measures)
    print("The expected number of people with covid after one day in office is " + str(without_measures_mean) + " when no mitigation strategies are used.")

    masking = []
    for i in range(number_of_runs):
        masking += [run_simulation(num_in_office, office_volume, outside_infection_rate, ismasked=True, ave_shift=average_shift, standard_dev=standard_dev)]
    masking_mean = np.mean(masking)
    masking_std = np.std(masking)
    print("The expected number of people with covid after one day in office is " + str(masking_mean) + " when masks are used in the office.")

    ventilation = []
    for i in range(number_of_runs):
        ventilation += [run_simulation(num_in_office, office_volume, outside_infection_rate, isvent=True, ave_shift=average_shift, standard_dev=standard_dev)]
    ventilation_mean = np.mean(ventilation)
    ventilation_std = np.std(ventilation)
    print("The expected number of people with covid after one day in office is " + str(ventilation_mean) + " when the office uses good ventilation systems.")

    chance = 0.4 # chance a person does not know they have covid (goes into office)
    quarantine = []
    for i in range(number_of_runs):
        quarantine += [run_simulation(num_in_office, office_volume, outside_infection_rate * chance, ave_shift=average_shift, standard_dev=standard_dev)]
    quarantine_mean = np.mean(quarantine)
    quarantine_std = np.std(quarantine)
    print("The expected number of people with covid after one day in office is " + str(quarantine_mean) + " when the office encourages quarantining when an employee is feeling symptoms.")

    all_measures = []
    for i in range(number_of_runs):
        all_measures += [run_simulation(num_in_office, office_volume, outside_infection_rate * chance, True, True, False, average_shift, standard_dev)]
    all_measures_mean = np.mean(all_measures)
    all_measures_std = np.std(all_measures)
    print("The expected number of people with covid after one day in office is " + str(all_measures_mean) + " when the office uses all mentioned mitigation strategies.")


    print("LaTeX Table Form")
    print("\hline")
    print(" & No Measures & Masking Only & Ventilation Only & Quarantine & All Measures")
    print("\hline\hline")
    print("Mean & " + str(without_measures_mean) + " & " + str(masking_mean) + " & " + str(ventilation_mean) + " & " + str(quarantine_mean) + " & " + str(all_measures_mean))
    print("\hline")
    print("Standard Deviation & " + str(without_measures_std) + " & " + str(masking_std) + " & " + str(
        ventilation_std) + " & " + str(quarantine_std) + " & " + str(all_measures_std))
    print("\hline")

def main_runasone(num_in_office, office_volume, outside_infection_rate=0.0015, average_shift=480, standard_dev=15):
    print("Given that: ")
    print("The number of people in the office is " + str(num_in_office))
    print("The area of the office is " + str(office_volume))
    print("The outside infection rate is " + str(outside_infection_rate))
    print("The standard length of shift is " + str(average_shift))
    print("The standard deviation of length of shift is " + str(standard_dev))

    number_of_runs = 1000000

    print("Here are the numbers when the simulation is run with exactly one person coming into the office with covid: ")

    without_measures = []
    for i in range(number_of_runs):
        without_measures += [run_simulation(num_in_office, office_volume, outside_infection_rate, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)]
    without_measures_mean = np.mean(without_measures)
    without_measures_std = np.std(without_measures)
    print("The expected number of people with covid after one day in office is " + str(
        without_measures_mean) + " when no mitigation strategies are used.")

    masking = []
    for i in range(number_of_runs):
        masking += [run_simulation(num_in_office, office_volume, outside_infection_rate, ismasked=True, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)]
    masking_mean = np.mean(masking)
    masking_std = np.std(masking)
    print("The expected number of people with covid after one day in office is " + str(
        masking_mean) + " when masks are used in the office.")

    ventilation = []
    for i in range(number_of_runs):
        ventilation += [run_simulation(num_in_office, office_volume, outside_infection_rate, isvent=True, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)]
    ventilation_mean = np.mean(ventilation)
    ventilation_std = np.std(ventilation)
    print("The expected number of people with covid after one day in office is " + str(
        ventilation_mean) + " when the office uses good ventilation systems.")

    chance = 0.4  # chance a person does not know they have covid (goes into office)
    quarantine = []
    for i in range(number_of_runs):
        quarantine += [run_simulation(num_in_office, office_volume, outside_infection_rate * chance, run_as_one=True, ave_shift=average_shift, standard_dev=standard_dev)]
    quarantine_mean = np.mean(quarantine)
    quarantine_std = np.std(quarantine)
    print("The expected number of people with covid after one day in office is " + str(
        quarantine_mean) + " when the office encourages quarantining when an employee is feeling symptoms.")

    all_measures = []
    for i in range(number_of_runs):
        all_measures += [run_simulation(num_in_office, office_volume, outside_infection_rate * chance, True, True, True, average_shift, standard_dev)]
    all_measures_mean = np.mean(all_measures)
    all_measures_std = np.std(all_measures)
    print("The expected number of people with covid after one day in office is " + str(
        all_measures_mean) + " when the office uses all mentioned mitigation strategies.")

    print("LaTeX Table Form")
    print("\hline")
    print(" & No Measures & Masking Only & Ventilation Only & Quarantine & All Measures")
    print("\hline\hline")
    print("Mean & " + str(without_measures_mean) + " & " + str(masking_mean) + " & " + str(
        ventilation_mean) + " & " + str(quarantine_mean) + " & " + str(all_measures_mean))
    print("\hline")
    print("Standard Deviation & " + str(without_measures_std) + " & " + str(masking_std) + " & " + str(
        ventilation_std) + " & " + str(quarantine_std) + " & " + str(all_measures_std))
    print("\hline")

# TODO: Test 80sqft per person, 125, 150
# TODO: Test 20, 50, 100, 500 people

def main():
    num_in_office = 20
    office_volume = 360
    outside_infection_rate = 0.0015
    average_shift = 433.578
    standard_dev = 20.32
    main_allnumbers(num_in_office, office_volume, outside_infection_rate, average_shift, standard_dev)
    main_runasone(num_in_office, office_volume, outside_infection_rate, average_shift, standard_dev)



def test():
    print(probability_catch_covid(1,100,480))
    print(probability_catch_covid(1,100,480,True))
    print(probability_catch_covid(1,100,480,False,True))
    print(probability_catch_covid(1,100,400,True,True))


if __name__ == '__main__':
    main()
