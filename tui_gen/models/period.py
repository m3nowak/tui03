"""
Module containing class representing time period.
"""
from datetime import datetime
from tui_gen.models.parity import Parity

TIME_HRS_FORMAT = '%H%M'


class Period(object):
    """
    Class representing time period.
    """

    def __init__(self, dow, time_start, time_end, parity=Parity.BOTH):
        self.dow = dow
        self.time_start = time_start
        self.time_end = time_end
        self.parity = parity

    @staticmethod
    def dict_factory(dict_raw):
        """
        Object factory. Consumes dictionaries,
        :param dict dict_raw: raw, json-loaded dictionary
        :returns Period: period object
        """
        return Period(dict_raw['dow'],
                      datetime.strptime(dict_raw['start'], TIME_HRS_FORMAT),
                      datetime.strptime(dict_raw['end'], TIME_HRS_FORMAT),
                      Parity(dict_raw.get('par', 0)))
