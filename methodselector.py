#!/bin/python3

from random import randint
import re


class MethodSelectorError(Exception):
    pass


class InvalidMethodSelector(MethodSelectorError):
    pass


class MethodSelector:
    def set_identifier(self, identifier):
        valid_id_starts = re.compile(r'[A-Za-z]')
        if not re.match(valid_id_starts, identifier):
            raise InvalidMethodSelector('Method selector must start with a letter')
        if identifier:
            self._identifier = identifier

    def get_identifier(self):
        return self._identifier

    identifier = property(get_identifier, set_identifier)

    def get_selectable_methods(self):
        return [method for method in dir(self) if method.startswith(self.identifier)]

    selectable_methods = property(get_selectable_methods)

    def set_likelihoods_map(self, likelihoods):
        for key in likelihoods.keys():
            if key not in self.selectable_methods:
                raise MethodSelectorError("{} not a valid selectable method for {}".format())
        if sum([val for val in likelihoods.values()]) != 100:
            raise MethodSelectorError("Likelihoods must sum to 100")
        self._likelihoods = likelihoods

    def get_likelihoods_map(self):
        return dict([(item[1], item[0]) for item in self._likelihoods.items()])

    likelihoods_map = property(get_likelihoods_map, set_likelihoods_map)

    def get_likelihoods(self):
        likelihoods = []
        for item in self.likelihoods_map:
            likelihoods += [item[1]] * item[0]
        return likelihoods

    def set_likelihoods(self, _):
        raise MethodSelectorError("Cannot set likelihoods directly--set likelihoods map instead")

    likelihoods = property(get_likelihoods, set_likelihoods)

