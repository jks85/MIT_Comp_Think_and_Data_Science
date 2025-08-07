# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random

random.seed(0)

##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """

        return random.random() <= self.death_prob

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        reproduce_prob = self.birth_prob*(1-pop_density)
        bact_reproduces = random.random() <= reproduce_prob

        if bact_reproduces:
            return SimpleBacteria(self.birth_prob, self.death_prob)
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        # determine whether each bacteria die and create list of survivors
        # if code below fails iterate over indices and use them to remove bacteria

        surviving_bacteria = []

        for bact in self.bacteria:

            if not bact.is_killed():
                surviving_bacteria.append(bact)

        # recalculate population density. use this value until update is called again
        new_pop_density = len(surviving_bacteria)/self.max_pop

        # determine whether each surviving cell reproduces. new bacteria do not reproduce
        bacteria_children = []

        for bact in surviving_bacteria:
            try:
                new_bacteria = bact.reproduce(new_pop_density)
                bacteria_children.append(new_bacteria)

            except NoChildException:
                print("bacteria did not reproduce")

        # create new bacteria list for patient
        surviving_bacteria.extend(bacteria_children)
        self.bacteria = surviving_bacteria

        # self.bacteria = surviving_bacteria + bacteria_children    # single line expression for combining the lists

        return len(self.bacteria)


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """

    pop_sum = 0     # initialize tracker for population sum

    for trial_pops in populations:
        pop_sum += trial_pops[n]

    return pop_sum/len(populations)


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    populations = [[]]*num_trials    # create list of empty lists with population data for each trial
    for trial in range(num_trials):
        bacteria_list = []
        for index in range(num_bacteria):
            bacteria_list.append(SimpleBacteria(birth_prob, death_prob))
        patient = Patient(bacteria_list, max_pop)
        trial_pops = [num_bacteria]  # track trial populations
        for time_step in range(1,300):
            trial_pops.append(patient.update())
        populations[trial] = trial_pops

    # create plotting parameters
    time_steps = list(range(300))

    # # get average population at each time step (y coordinates)
    average_bact_pop = []
    for i in range(300):
        average_bact_pop.append(calc_pop_avg(populations, i))

    make_one_curve_plot(time_steps,average_bact_pop,"time_steps",
                        "avg population", "Bacteria Population vs Time")

    return populations


# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)



##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    avg_pop_step_t = calc_pop_avg(populations,t)

    sum_sq_devs = 0    # variable to track sum of squared deviations

    for trial in range(len(populations)):
        sum_sq_devs += (populations[trial][t] - avg_pop_step_t)**2

    return math.sqrt(sum_sq_devs/len(populations))



def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """

    mean = calc_pop_avg(populations,t)
    std_err = calc_pop_std(populations,t)/math.sqrt(len(populations))
    width = 1.96*std_err

    return mean,width

##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        # SimpleBacteria.__init__(self, birth_prob, death_prob)
        super().__init__(birth_prob, death_prob)      # testing superclass constructor using super()
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""

        # commented out code below is wrong. i think method checks current state not whether resistance is *developed*
        # if random.random() <= self.mut_prob:
        #     self.resistant = True
        # else:
        #     self.resistant = False

        # # testing ternary operator
        # gained_resistance = random.random() <= self.mut_prob
        # self.resistant = True if gained_resistance else False

        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """

        if self.resistant:
            # randomize death results
            return random.random() < self.death_prob
        else:
            return random.random() < self.death_prob/4

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """



        # return NoChildException otherwise

        # compute probabilities and filters
        reproduce_prob = self.birth_prob * (1 - pop_density)
        mutation_prob = self.mut_prob * (1 - pop_density)

        bact_reproduces = random.random() <= reproduce_prob
        bact_mutates = random.random() <= mutation_prob

        # check whether bacteria reproduces
        if bact_reproduces:
            bact_child = ResistantBacteria(self.birth_prob, self.death_prob, self.resistant, self.mut_prob)
            if bact_mutates:        # don't need to check parent resistance. child is already resistant or may mutate
                bact_child.resistant = True
            return bact_child
        else:
            raise NoChildException




class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        super().__init__(bacteria,max_pop)
        # self.bacteria = bacteria
        # self.max_pop = max_pop
        self.on_antibiotic = False


    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """

        # res_list = []   # list to contain bools indicating whether a bacteria is resistant
        # for bact in self.bacteria:
        #     if isinstance(bact,ResistantBacteria):  # this instance check is unnecessary. may refactor later
        #         res_list.append(True) if bact.get_resistant() else res_list.append(False)
        #     else:
        #         res_list.append(False)
        #
        #
        # return sum(res_list)

        return sum([bact.get_resistant() for bact in self.bacteria])

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """

        bact_survivors = []

        # check if bacteria cells die and create survival list

        for bact in self.bacteria:
            if not bact.is_killed():
                bact_survivors.append(bact)

        # if patient on antibiotics. for treated patients only resistant bacteria survive further.
        # for untreated patients all bacteria survive

        if self.on_antibiotic:
            bact_survivors_copy = bact_survivors[:]     # mutating list so copy is needed here
            for bact in bact_survivors_copy:
                if not bact.get_resistant():
                    bact_survivors.remove(bact)


        # recalculate population density and reassign
        new_pop_density = len(bact_survivors)/self.max_pop

        # check whether bacteria reproduce and add offspring

        bact_children = []
        for bact in bact_survivors:
            try:
                bact_child = bact.reproduce(new_pop_density)
                bact_children.append(bact_child)
            except NoChildException:
                print("bacteria did not reproduce")

        # update lists and return population
        self.bacteria = bact_survivors + bact_children
        return self.get_total_pop()



##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    This function plots the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot using the helper
    function make_two_curve_plot().

    Additionally, it computes 95% confidence intervals for each population at t = 299.
    Note that the plotting significantly increases the run-time.

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    populations = [[]]*num_trials   # list of lists with bacteria population for each trial and time step
    resistant_pop = [[]]*num_trials # list of lists with resistant bacteria population for each trial and time step

    for trial in range(num_trials):

        bacteria_list_trial = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob) for i in range(num_bacteria)]
        patient_trial = TreatedPatient(bacteria_list_trial, max_pop)


        # lists containing bacteria and resistant bacteria populations for each trial
        bact_pops = []
        resistant_bact_pops = []

        # set step 0 to initial populations
        bact_pops.append(num_bacteria)
        resistant_bact_pops.append(0)

        # simulate 149 additional steps (150 total)
        for i in range(1,150):
            bact_pops.append(patient_trial.update())
            resistant_bact_pops.append(patient_trial.get_resist_pop())

        # add antibiotic and simulate 250 more steps (400 total)
        patient_trial.set_on_antibiotic()
        for i in range(150,400):
            bact_pops.append(patient_trial.update())
            resistant_bact_pops.append(patient_trial.get_resist_pop())

        populations[trial] = bact_pops
        resistant_pop[trial] = resistant_bact_pops

    # plot population vs time graphs
    time_steps_antibiotic = list(range(400))
    average_bact_pop = []
    average_resistant_pop = []
    for i in range(400):
        average_bact_pop.append(calc_pop_avg(populations, i))
        average_resistant_pop.append(calc_pop_avg(resistant_pop, i))

    make_two_curve_plot(time_steps_antibiotic, average_bact_pop, average_resistant_pop, "Average Total Bacteria",
                        "Average Resistant Bacteria", "time steps", "Population",
                        "Bacteria Population vs Time in Treated Patients")


    # compute confidence intervals of total and resistant populations at time 299
    total_mean, total_width = calc_95_ci(populations, 299)
    resistant_mean, resistant_width = calc_95_ci(resistant_pop, 299)

    print(f"95% CI for total population at t = 299: ({round(total_mean - total_width,2)},"
          f"{round(total_mean + total_width,2)})")
    print(f"95% CI for resistant population at t = 299: ({round(resistant_mean - resistant_width,2)},"
          f"{round(resistant_mean + resistant_width,2)})")

    return populations,resistant_pop



# When you are ready to run the simulations, uncomment the next lines one
# at a time

# # Sim A
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                       max_pop=1000,
#                                                       birth_prob=0.3,
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=50)


# Sim B
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                       max_pop=1000,
#                                                       birth_prob=0.17, # changed from 0.17
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=50)


# smaller simulation for debugging

# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=5,
#                                                       max_pop=1000,
#                                                       birth_prob=0.3, # changed from 0.17
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=5)


##########################
# PROBLEM 6
##########################

# Calculate 95% confidence intervals for the total population and resistant population at time step 299. Note that this
# this results in 4 confidence intervals. The method simulation_with_antibiotic() prints the desired 95%
# confidence intervals.

# Simulation A
# 95% CI for total population at t = 299: (183.53,204.11)
# 95% CI for resistant population at t = 299: (183.53,204.11)


# Simulation B
# 95% CI for total population at t = 299: (0.0,0.0)
# 95% CI for resistant population at t = 299: (0.0,0.0)

# Within the simulation the confidence intervals for the total and resistant populations match. This is expected since
# the interval was calculated at t = 299, which beyond the time at which the graphs converge (i.e. after the antibiotic
# is administered.



