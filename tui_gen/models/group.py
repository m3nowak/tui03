"""
Module containing class representing activity group.
"""
from tui_gen.models.period import Period

class Group(object):
    """
    Class representing activity group.
    """
    def __init__(self, name, period_list):
        self.name = name
        self.period_list = period_list

    @staticmethod
    def list_factory(name, list_raw):
        """
        Object factory. Consumes lists,
        :param list list_raw: raw, json-loaded list
        :returns Group: group object
        """
        return Group(name, [Period.dict_factory(period_dict) for period_dict in list_raw])
