"""
Chromosome rating utility.
"""
from copy import copy
from datetime import datetime, timedelta

from tui_gen.models.parity import Parity

_DEFAULT_CONFLICT_PENALTY = -250
_DEFAULT_BEFORE_9_PENALTY = -10
_DEFAULT_AFTER_17_PENALTY = -10
_DEFAULT_OVER_2H_WINDOW_PENALTY = -10

_DEFAULT_FREE_DAY_BONUS = 50
_DEFAULT_NOT_BEFORE_11_BONUS = 10
_DEFAULT_NOT_AFTER_15_BONUS = 10

_HOUR_9 = datetime(1900, 1, 1, 9, 0)
_HOUR_11 = datetime(1900, 1, 1, 11, 0)
_HOUR_15 = datetime(1900, 1, 1, 15, 0)
_HOUR_17 = datetime(1900, 1, 1, 17, 0)
_SPAN_2H = timedelta(hours=2)


def create_fenotype(chromosome):
    """
    Create fenotype for rating.
    :param dict chromosome: source chromosome
    :returns list: fenotype (list of list of tuples of (time, time))
    """
    fenotype = [[] for _ in range(10)]
    for group in chromosome.values():
        for period in group.period_list:
            dow_zero_based = period.dow - 1
            if period.parity != Parity.EVEN:
                fenotype[dow_zero_based].append((period.time_start, period.time_end, group.name))
            if period.parity != Parity.ODD:
                fenotype[dow_zero_based+5].append((period.time_start, period.time_end, group.name))
    for day_list in fenotype:
        day_list.sort()

    return fenotype


def _count_conflicts(fenotype):
    """
    Count conflicts in fenotype.

    :param list fenotype: scored fenotype
    :return int: conflict occurances
    """
    count = 0
    for day_list in fenotype:
        day_list_copy = copy(day_list)
        while len(day_list_copy) > 1:
            time_start_0, time_end_0, _0 = day_list_copy.pop(0)
            for time_start_1, time_end_1, _1 in day_list_copy:
                if (time_start_1 <= time_start_0 <= time_end_1)\
                        or (time_start_1 <= time_end_0 <= time_end_1):
                    count += 1
    return count


def _count_before_9(fenotype):
    """
    Count days with first activities before 9.

    :param list fenotype: scored fenotype
    :return int: "before 9" occurances
    """
    count = 0
    for day_list in fenotype:
        if day_list and day_list[0][0] < _HOUR_9:
            count += 1
    return count


def _count_after_17(fenotype):
    """
    Count days with last activities after 17.

    :param list fenotype: scored fenotype
    :return int: "after 17" occurances
    """
    count = 0
    for day_list in fenotype:
        if day_list and day_list[-1][0] > _HOUR_17:
            count += 1
    return count


def _count_not_before_11(fenotype):
    """
    Count days with first activities not before 11.

    :param list fenotype: scored fenotype
    :return int: "not before 11" occurances
    """
    count = 0
    for day_list in fenotype:
        if day_list and day_list[0][0] >= _HOUR_11:
            count += 1
    return count


def _count_not_after_15(fenotype):
    """
    Count days with last activities not after 15.

    :param list fenotype: scored fenotype
    :return int: "not after 15" occurances
    """
    count = 0
    for day_list in fenotype:
        if day_list and day_list[-1][0] <= _HOUR_15:
            count += 1
    return count


def _count_2h_windows(fenotype):
    """
    Count 2h+ windows.

    :param list fenotype: scored fenotype
    :return int: 2h+ windows count
    """
    count = 0
    for day_list in fenotype:
        if len(day_list) > 2:
            for index in range(len(day_list) - 1):
                if day_list[index+1][0] - day_list[index][1] >= _SPAN_2H:
                    count += 1
    return count


def _count_free_days(fenotype):
    """
    Count free days.

    :param list fenotype: scored fenotype
    :return int: free day count
    """
    count = 0
    for day_list in fenotype:
        if not day_list:
            count += 1
    return count


def rate_chromosome(chromosome, scoring_values):
    """
    Calculate rating for chomosome.

    :param dict chromosome: chromosome to score
    :param dict scoring_values: dictionary of scoring values
    :returns int: score of chromosome
    """
    conflict_penalty = scoring_values.get("conflictPenalty", _DEFAULT_CONFLICT_PENALTY)
    before_9_penalty = scoring_values.get("before9Penalty", _DEFAULT_BEFORE_9_PENALTY)
    after_17_penalty = scoring_values.get("after17Penalty", _DEFAULT_AFTER_17_PENALTY)
    over_2h_window_penalty = scoring_values.get(
        "over2hWindowPenalty", _DEFAULT_OVER_2H_WINDOW_PENALTY)

    free_day_bonus = scoring_values.get("freeDayBonus", _DEFAULT_FREE_DAY_BONUS)
    not_before_11_bonus = scoring_values.get("notBefore11Bonus", _DEFAULT_NOT_BEFORE_11_BONUS)
    not_after_15_bonus = scoring_values.get("notAfter15Bonus", _DEFAULT_NOT_AFTER_15_BONUS)

    fenotype = create_fenotype(chromosome)

    score_conflict_penalty = conflict_penalty * _count_conflicts(fenotype)
    score_before_9_penalty = before_9_penalty * _count_before_9(fenotype)
    score_after_17_penalty = after_17_penalty * _count_after_17(fenotype)
    score_over_2h_window_penalty = over_2h_window_penalty * _count_2h_windows(fenotype)

    score_free_day_bonus = free_day_bonus * _count_free_days(fenotype)
    score_not_before_11_bonus = not_before_11_bonus * _count_not_before_11(fenotype)
    score_not_after_15_bonus = not_after_15_bonus * _count_not_after_15(fenotype)

    score = score_conflict_penalty + score_before_9_penalty + score_after_17_penalty + \
        score_over_2h_window_penalty + score_free_day_bonus + \
        score_not_before_11_bonus + score_not_after_15_bonus

    return score


def rate_population(population, scoring_values):
    """
    Calculate rating for population.

    :param list population: population to score
    :return list: list of scores
    """
    return [rate_chromosome(chromo, scoring_values) for chromo in population]
