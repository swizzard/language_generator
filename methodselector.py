#!/bin/python3

from random import randint
import re


class MethodSelectorError(Exception):
    pass


class InvalidMethodSelector(MethodSelectorError):
    pass


class MethodSelector:

    def set_likelihoods_map(self, likelihoods_map):
        """
        Set all likelihoods, based on the provided mapping. likelihoods_map should be a dictionary whose keys are
        the labels for each group of methods, and whose values should be a dictionary whose keys are the method names in
        question, and whose values should be equal to the chance of that method being selected, as an integer. (Thus, if
        there's a 30% chance a given method should be selected, the value should be 30.)
        :param likelihoods_map: mapping from methods to likelihoods
        :type likelihoods_map: dict (see above)
        """
        if not self._likelihoods:
            self._likelihoods = {}
        for item in likelihoods_map.items():
            self._likelihoods[item[0]] = self.__likelihoods_map_to_list(self.__validate_likelihoods(item[0], item[1]))

    def __likelihoods_map_to_list(self, likelihoods_map_entry):
        """
        Translates an entry in a likelihoods mapping to a list consisting of references to each method in the mapping
        to its likelihood. For example, given a mapping {method1: 30, method2: 20, method3: 50}, the list would consist
        of 30 references to method1, 20 references to method2, and 50 references to method3.
        :param likelihoods_map_entry: the entry to process
        :type likelihoods_map_entry: dict
        """
        likelihoods = []
        for item in likelihoods_map_entry.items():
            likelihoods += [item[1]] * item[0]
        return likelihoods

    def __validate_likelihoods(self, label, likelihoods):
        """
        Validates provided likelihoods
        :param label: the label for the group of methods
        :type label: str
        :param likelihoods: the likelihoods dictionary for the group of methods
        :type likelihoods: dict
        """
        if not isinstance(likelihoods, dict):
            raise MethodSelectorError("Likelihoods must be a dictionary")
        likelihoods_sum = sum([val for val in likelihoods.values()])
        if likelihoods_sum != 100:
            raise MethodSelectorError(
                "Likelihoods must sum to 100 (likelihoods for {} sum to {})".format(label, likelihoods_sum))
        for val in likelihoods.values():
            if not hasattr(self, val):
                raise MethodSelectorError("{} is not a valid method".format(val))
        return likelihoods

    def get_likelihoods_map(self):
        """
        Converts the likelihoods map from a dictionary {methods_group: list_of_methods,...} to a dictionary
        {methods_group: {method: count,...},...} for better readability
        """
        output_d = {}
        for key in self._likelihoods.keys():
            label_d = {}
            for val in self._likelihoods[key]:
                label_d[val] = label_d.get(val, 0) + 1
            output_d[key] = label_d
        return output_d

    likelihoods_map = property(get_likelihoods_map, set_likelihoods_map)

    def set_likelihoods(self, _):
        """
        Nope.
        """
        raise MethodSelectorError("Cannot set likelihoods directly--set likelihoods map instead")

    likelihoods = property(get_likelihoods_map, set_likelihoods)

    def get_random_method(self, group_label, adjustment=0):
        """
        Retrieves a random method from the methods group identified by group_label.
        :param group_label: the label of the methods group to retrieve a method from
        :type group_label: str
        :param adjustment: an optional parameter to 'nudge' the random selection
        :type adjustment: int
        """
        return getattr(self, self._likelihoods[group_label][randint(0, 100) + adjustment])