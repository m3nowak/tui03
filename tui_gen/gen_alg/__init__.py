"""
Module containing genetic algorithm logic.
"""
from copy import copy
import math
from random import choice as rand_choice, randrange, random, choices as rand_choices, sample
from datetime import datetime
from enum import Enum

import numpy as np

from tui_gen.gen_alg.rating import rate_population
from tui_gen.gen_alg.genetic_algorithm_report import GeneticAlgorithmReport


class CrossoverMethodEnum(Enum):
    """
    Enum containing values for different methods of crossover
    """
    Uniform = 1
    Classy = 2
    Probability = 3


class MutationMethodEnum(Enum):
    """
    Enum containing values for different methods of mutation
    """
    Standard = 1
    DoubleStandard = 2
    Range = 3


def tournament_selection(population, population_rating, tour_size=3, elite_size=0, dropout_size=0):
    """
    Perform tournament selection.
    :param list population: population to perform selection on
    :param list population_rating: rating of population members
    :param int tour_size: tour size
    :param int elite_size: top chromosome retain count
    :param float dropout_size: worst of popultaion loss size
    """
    og_population_len = len(population)
    survived_population = []
    population_rating_np = np.array(population_rating)

    if dropout_size > 0 or elite_size > 0:
        sorted_rating = np.argsort(population_rating_np)

    if elite_size > 0:
        for preserved_position in sorted_rating[-elite_size:][::-1]:
            survived_population.append(population[preserved_position])

    if dropout_size > 0:
        population_np = np.array(population)
        population_np = np.delete(population_np, sorted_rating[:dropout_size])
        population = population_np.tolist()

    while len(survived_population) < og_population_len:
        chosen_indicies = sample(range(len(population)), k=tour_size)
        index_of_chosen_indicies = np.argmax(population_rating_np[chosen_indicies])
        pop_index_chosen = chosen_indicies[index_of_chosen_indicies]
        survived_population.append(population[pop_index_chosen])
    return survived_population


def logistic(population_rating):
    """
    Calculate sigmoid for population ratings.
    :param list population_rating: rating of population members
    :returns list: rayings with sigmoid applied
    """
    np_population_rating = np.array(population_rating)
    np_population_rating_softplus = np.log(1/(1 + np.exp(np_population_rating*-1)))
    scores_softplus = np_population_rating_softplus.tolist()
    return scores_softplus


def softplus(population_rating):
    """
    Calculate softplus for population ratings.
    :param list population_rating: rating of population members
    :returns list: rayings with softlus applied
    """
    np_population_rating = np.array(population_rating)
    np_population_rating_softplus = np.log(1 + np.exp(np_population_rating))
    scores_softplus = np_population_rating_softplus.tolist()
    return scores_softplus


def roulette_selection(population, population_rating, activation_func=softplus):
    """
    Perform roulette selection.
    :param list population: population to perform selection on
    :param list population_rating: rating of population members
    :param function activation_func: activation function
    :returns list: selected chromosomes
    """
    return rand_choices(population, weights=activation_func(population_rating), k=len(population))


def chromosome_mutation(chromo, problem_dict, method=MutationMethodEnum.Standard):
    """
    Perform mutation on chromosome.
    :param dict chromo: chromosome to perform mutation on
    :param dict problem_dict: problem dictionary
    :param MutationMethodEnum method: mutation method
    :return dict: mutated chromosome
    """
    key_list = list(problem_dict.keys())
    mutated_chromo = copy(chromo)
    mutation_keys = []
    if method == MutationMethodEnum.Standard:
        mutation_keys.append(rand_choice(key_list))
    elif method == MutationMethodEnum.DoubleStandard:
        mutation_keys.extend(sample(key_list, 2))
    elif method == MutationMethodEnum.Range:
        for key in key_list:
            if random() > 0.5:
                mutation_keys.append(key)

    for selected_key in mutation_keys:
        mutated_chromo[selected_key] = rand_choice(problem_dict[selected_key])
    return mutated_chromo


def population_mutation(population, problem_dict, probability, method=MutationMethodEnum.Standard):
    """
    Perform mutation on population.
    :param list population: population to perform mutation on
    :param dict problem_dict: problem dictionary
    :param int probability: mutation probability
    :param MutationMethodEnum method: mutation method
    :return list: population after mutation
    """
    mutated_population = []
    for chromo in population:
        if random() <= probability:
            chromo = chromosome_mutation(chromo, problem_dict, method)
        mutated_population.append(chromo)
    return mutated_population


def chromosomes_crossover(chromo_0, chromo_1):
    """
    Perform uniform crossover on two chromosomes.
    :param dict chromo_0: first chromosome to perform crossover on
    :param dict chromo_1: second chromosome to perform crossover on
    :return tuple: crossed chromosome pair
    """
    crossd_chromo_0 = {}
    crossd_chromo_1 = {}

    for key in chromo_0.keys():
        if randrange(2):
            crossd_chromo_0[key] = chromo_0[key]
            crossd_chromo_1[key] = chromo_1[key]
        else:
            crossd_chromo_0[key] = chromo_1[key]
            crossd_chromo_1[key] = chromo_0[key]
    return crossd_chromo_0, crossd_chromo_1


def chromosomes_crossover_swap_prob(chromo_0, chromo_1, swap_pob):
    """
    Perform uniform crossover on two chromosomes with swap probability.
    :param dict chromo_0: first chromosome to perform crossover on
    :param dict chromo_1: second chromosome to perform crossover on
    :param float swap_pob: swap_probability
    :return tuple: crossed chromosome pair
    """
    crossd_chromo_0 = {}
    crossd_chromo_1 = {}

    for key in chromo_0.keys():
        if random() < swap_pob:
            crossd_chromo_0[key] = chromo_0[key]
            crossd_chromo_1[key] = chromo_1[key]
        else:
            crossd_chromo_0[key] = chromo_1[key]
            crossd_chromo_1[key] = chromo_0[key]
    return crossd_chromo_0, crossd_chromo_1


def chromosomes_crossover_classy(chromo_0, chromo_1, cross_point_count=1):
    """
    Perform classy crossover on two chromosomes.
    :param dict chromo_0: first chromosome to perform crossover on
    :param dict chromo_1: second chromosome to perform crossover on
    :param int cross_point_count: cross point count
    :return tuple: crossed chromosome pair
    """
    keys_sorted = sorted(list(chromo_0.keys()))
    keys_sorted_len = len(keys_sorted)
    cross_points = sample(range(keys_sorted_len), min(cross_point_count, keys_sorted_len))
    keys_counter = 0
    use_snd = False
    crossd_chromo_0 = {}
    crossd_chromo_1 = {}

    for key in keys_sorted:
        if keys_counter in cross_points:
            use_snd = not use_snd
        keys_counter += 1
        if use_snd:
            crossd_chromo_0[key] = chromo_0[key]
            crossd_chromo_1[key] = chromo_1[key]
        else:
            crossd_chromo_0[key] = chromo_1[key]
            crossd_chromo_1[key] = chromo_0[key]
    return crossd_chromo_0, crossd_chromo_1


def population_crossover(population,
                         probability,
                         method=CrossoverMethodEnum.Uniform,
                         classy_cross_count=1,
                         swap_prob=0.5):
    """
    Perform crossover on population.
    :param list population: population to perform crossover on
    :param int probability: crosspover probability
    :param bool use_classy: whether to use classic crossover
    :param int classy_cross_count: number of crossings when classy method is used
    :param float swap_prob: swap probability when Probability method is used
    :return list: population after crossover
    """
    og_population = copy(population)
    crossoverd_population = []
    while len(og_population) >= 2:
        chromo_0 = og_population.pop(randrange(len(og_population)))
        chromo_1 = og_population.pop(randrange(len(og_population)))
        if random() <= probability:
            if method == CrossoverMethodEnum.Classy:
                chromo_0, chromo_1 = chromosomes_crossover_classy(
                    chromo_0, chromo_1, classy_cross_count)
            elif method == CrossoverMethodEnum.Probability:
                chromo_0, chromo_1 = chromosomes_crossover_swap_prob(
                    chromo_0, chromo_1, swap_prob)
            else:
                chromo_0, chromo_1 = chromosomes_crossover(chromo_0, chromo_1)
        crossoverd_population.append(chromo_0)
        crossoverd_population.append(chromo_1)
    if og_population:
        crossoverd_population.append(og_population[0])
    return crossoverd_population


def create_random_chromosome(problem_dict):
    """
    Create random chomosome.
    :param dict problem_dict: problem dictionary
    :returns dict: randomly created chomosome
    """
    return {
        course_name: rand_choice(group_list) for course_name, group_list in problem_dict.items()
    }


def create_population(problem_dict, size):
    """
    Create random population.
    :param dict problem_dict: problem dictionary
    :param int size: population size
    :returns list: randomly created chomosomes
    """
    return [create_random_chromosome(problem_dict) for _ in range(size)]


def genetic_algorithm(problem_dict, pop_size, crossover_prob,
                      mutation_prob, stale_limit, scoring_values, verbose=True):
    """
    Run genetic algorithm.
    :param dict problem_dict: problem dictionary
    :param int pop_size: population size
    :param float crossover_prob: crossover probability
    :param float mutation_prob: mutation probability
    :param int stale_limit: max number of stale generations (termination condition)
    :param dict scoring_values: dictionary of scoring values
    :param bool verbose: whether print info during execution
    :returns GeneticAlgorithmReport: final report
    """
    population = create_population(problem_dict, pop_size)
    best_score = - math.inf
    best_score_stale_for = 0  # for how many gens. best score is the same
    best_chromo = population[0]
    generation_count = 0
    time_start = datetime.now()
    while best_score_stale_for < stale_limit:
        generation_count += 1

        population = population_crossover(
            population, crossover_prob)
        population = population_mutation(population, problem_dict, mutation_prob, MutationMethodEnum.Range)
        population_rating = rate_population(population, scoring_values)
        gen_best_index = np.argmax(population_rating)
        gen_best_score = population_rating[gen_best_index]

        if gen_best_score > best_score:
            best_score_stale_for = 0
            best_score = gen_best_score
            best_chromo = population[gen_best_index]
        else:
            best_score_stale_for += 1
        if verbose:
            print("Best score for generation {}: {}".format(generation_count, gen_best_score))
        #population = roulette_selection(population, population_rating, logistic)
        population = tournament_selection(population, population_rating)
    time_end = datetime.now()
    return GeneticAlgorithmReport(best_chromo, best_score, generation_count, time_end-time_start)
