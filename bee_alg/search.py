"""
Module containing search part of bee algorithm solver
"""
from random import choice as rand_choice, choices as rand_choices
from copy import copy


def spawn_global_seeker(problem_dict):
    """
    Create random global seeker
    :param dict problem_dict: problem dictionary
    :returns dict: randomly created seeker
    """
    return {
        course_name: rand_choice(group_list) for course_name, group_list in problem_dict.items()
    }


def spawn_global_seekers(problem, n):
    """
    Spawn n global seekers
        :param dict problem: problem dictionary
        :param int n: seeker count
        :return list: global seekers, list of dict
    """
    return [spawn_global_seeker(problem) for _ in range(n)]


def spawn_local_seeker(problem, location, ngh):
    """
    Create random global seeker
    :param dict problem: problem dictionary
    :param dict location: location to spawn seeker at
    :param int ngh: neighbourhood size
    :returns dict: randomly created seeker
    """
    key_list = list(problem.keys())
    changed_dimensions_count = rand_choice(list(range(1, ngh+1)))
    changed_dimensions = rand_choices(key_list, k=changed_dimensions_count)
    new_location = copy(location)
    for changed_dimension in changed_dimensions:
        new_location[changed_dimension] = rand_choice(
            problem[changed_dimension])
    return new_location


def spawn_local_seekers(problem, location, ngh, n):
    """
    Create random global seeker
    :param dict problem: problem dictionary
    :param dict location: location to spawn seeker at
    :param int ngh: neighbourhood size
    :returns list: list of randomly created seekers
    """
    return [spawn_local_seeker(problem, location, ngh) for _ in range(n)]
