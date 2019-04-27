"""
Module containing bee algorithm solver
"""

import math
from datetime import datetime

import numpy as np

from bee_alg import rating, search, bee_algorithm_report


def _sort_rated_locations(locations, locations_ratings):
    """
    Sort rated locations
        :param list locations: list of locations
        :param list locations_ratings: list of location ratings
        :return list: sorted locations by rating
    """
    locations_ratings_np = np.array(locations_ratings)
    locations_np = np.array(locations)
    locations_sorted_np = locations_np[np.argsort(locations_ratings_np)]
    return locations_sorted_np.tolist()


def _best_rated_location(locations, locations_ratings):
    """
    Get best rated location
        :param list locations: list of locations
        :param list locations_ratings: list of location ratings
        :return dict: best location
    """
    locations_ratings_np = np.array(locations_ratings)
    locations_np = np.array(locations)
    locations_sorted_np = locations_np[np.argmax(locations_ratings_np)]
    return locations_sorted_np


def _location_search(problem, scoring_values, location, ngh, nsp, keep_og_locs):
    """
    Perform location search
        :param dict problem: problem dictionary
        :param dict scoring_values: dictionary of scoring values
        :param dict location: search starting point
        :param int ngh: neighbourhood size
        :param int nsp: neighbourhood search team size
        :param bool keep_og_locs: whether original locations should be kept in local searches
        :return dict: best location found
    """
    locations_local = search.spawn_local_seekers(problem, location, ngh, nsp)
    locations_local_rating = rating.rate_locations(
        locations_local, scoring_values)

    locations_local_best = _best_rated_location(
        locations_local, locations_local_rating)

    return locations_local_best


def initialize(problem, scoring_values, stale_rounds, n, m, ngh, nsp, e=0,
               nep=None, keep_og_locs=False):
    """
    Launch bee algorithm
        :param dict problem: problem dictionary
        :param dict scoring_values: dictionary of scoring values
        :param int stale_rounds: how much stale rounds has to pass
        :param int n: seeker swarm size
        :param int m: neighbourhood search place count
        :param int ngh: neighbourhood size
        :param int nsp: neighbourhood search team size
        :param int e: elite neighbourhood search place count
        :param int nep: elite neighbourhood search team size
        :param bool keep_og_locs: whether original locations should be kept in local searches
    """

    # value assertions
    if m >= n:
        raise ValueError("m must be less than n")
    if ngh <= 0:
        raise ValueError("ngh must be grater than 0")

    time_start = datetime.now()

    # end condition set up
    best_score_so_far = -math.inf
    best_location_so_far = None
    rounds_wo_best_score_change = 0
    rounds_count = 0

    # spawn n global seekers
    locations_global = search.spawn_global_seekers(problem, n)

    # rate all found locations
    locations_global_rating = rating.rate_locations(
        locations_global, scoring_values)

    # main loop
    while rounds_wo_best_score_change < stale_rounds:
        rounds_count += 1

        locations_global_sorted = _sort_rated_locations(
            locations_global, locations_global_rating)

        elite_search_locations = locations_global_sorted[-e:]
        standard_search_locations = locations_global_sorted[:-e][-(m-e)]

        elite_search_results = [_location_search(
            problem, scoring_values, location, ngh, nep, keep_og_locs)
            for location in elite_search_locations]
        standard_search_results = [_location_search(
            problem, scoring_values, location, ngh, nsp, keep_og_locs)
            for location in standard_search_locations]

        cummulative_search_results = elite_search_results+standard_search_results
        cummulative_search_ratings = rating.rate_locations(
            cummulative_search_results, scoring_values)
        round_best_location = _best_rated_location(
            cummulative_search_results, cummulative_search_ratings)
        round_best_rating = rating.rate_location(
            round_best_location, scoring_values)

        if best_score_so_far < round_best_rating:
            best_score_so_far = round_best_rating
            best_location_so_far = round_best_location
            rounds_wo_best_score_change = 0
        else:
            rounds_wo_best_score_change += 1
        locations_global = cummulative_search_results + \
            search.spawn_global_seekers(problem, n-m)

    time_end = datetime.now()

    return bee_algorithm_report.BeeAlgorithmReport(
        best_location_so_far, best_score_so_far, rounds_count, time_end-time_start)
