"""
Module containing models used by genetic algorithm/
"""
from tui_gen.models.group import Group

def parse_raw_course_dict(raw_course_dict):
    """
    Parse raw dictionary into dictionary of course name - list of group objects.
    """
    prepared_course_dict = {}
    for course_name, groups_dict in raw_course_dict['courses'].items():
        prepared_groups_list = []
        for group_name, group_period_list in groups_dict.items():
            prepared_groups_list.append(Group.list_factory(group_name, group_period_list))
        prepared_course_dict[course_name] = prepared_groups_list
    return prepared_course_dict
