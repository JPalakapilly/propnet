import numpy as np

from typing import *
from propnet import logger, ureg
from pybtex.database.input.bibtex import Parser

class PropertyMetadata :
#Class storing the complete description of a property.

    expected_props = ['id', 'units', 'display_names', 'display_symbols', 'dimension', 'test_value', 'comment']

    def __init__ (self, id : str, units : ureg.Quantity, display_names : List[str], display_symbols : List[str],
                  dimension : List[int], test_value : np.ndarray, comment : str) :
        """
            Parses and validates a series of inputs into a PropertyMetadata tuple, a format that PropNet expects.
            Parameters correspond exactly with those of a PropertyMetadata tuple.
            :param id: string ASCII identifying the property uniquely as an internal identifier.
            :param units: units of the property, supported by the Pint package.
            :param display_names: list of strings giving possible human-readable names for the property.
            :param display_symbols: list of strings giving possible human-readable symbols for the property.
            :param dimension: list giving the order of the tensor as the length, and number of dimensions as individual
                              integers in the list.
            :param test_value: a sample value of the property, reasonable over a wide variety of contexts.
            :param comment: any useful information on the property including its definitions and possible citations.
            :return: Properly-initialized PropertyMetadata instance.
        """
        if not id.isidentifier() or not id.islower():
            raise ValueError("The canonical name ({}) is not valid.".format(id))
        self.id = id
        self.units = ureg.Quantity.from_tuple(units)
        if display_names == None or len(display_names) == 0:
            raise ValueError("Insufficient display names for ({}).".format(id))
        self.display_names = display_names
        if display_symbols == None or len(display_symbols) == 0:
            raise ValueError("Insufficient display symbols for ({}).".format(id))
        self.display_symbols = display_symbols
        try :
            np.zeros(dimension)
        except :
            raise ValueError("Dimensions provided for ({}) are invalid.".format(id))
        self.dimension = dimension
        if not np.any(test_value) :
            logger.warn("Test value for {} is zero. Please change to a more appropriate test value.")
        self.test_value = test_value
        self.comment = comment

    @staticmethod
    def from_dict (d: dict) -> PropertyMetadata :
        """
        Convenience constructor. Creates a PropertyMetadata instance from a dictionary with appropriate
        key-value pairs.
        :param d: dict containing the information necessary to construct a PropertyMetadata object.
        :return: Properly-initialized PropertyMetadata instance.
        """
        for key in PropertyMetadata.expected_props :
            if key not in d.keys() :
                raise ValueError("Provided Dictionary is missing input argument: " + key)
        return PropertyMetadata(**d)


class Property :
#Class storing the value of a property in a given context.

    def __init__ (self, type : PropertyMetadata, value : Any, comment : str) :
        """
        Parses inputs for constructing a Property object.
        :param type: pointer to an existing PropertyMetadata object, identifies the type of data stored in the property.
        :param value: value of the property
        :param comment: important information relative to the property, including sourcing.
        """
        self.type = type
        self.value = value
        self.comment = comment
