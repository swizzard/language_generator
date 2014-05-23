from random import randint

from methodselector import MethodSelector
from morphology import Nominal, Verbal, Other
from morpheme_generator import MorphemeGeneratorMixin
from phono import Phonology

class Syntax(MethodSelector):
    def __init__(self, nominal_instance, verbal_instance, other_instance, likelihoods_dict=None, adjustments_dict=None):
        self.nominal_instance = nominal_instance
        self.verbal_instance = verbal_instance
        self.other_instance = other_instance
        self.adjustments = {
            'word_order_adjustment': 0,
            'adjunct_attachment_adjustment': 0
        }
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.base_likelihoods = {
            'word_order': {
                'sov': 43,
                'svo': 38,
                'vso': 9,
                'vos': 4,
                'ovs': 3,
                'osv': 3
                },
            'adjunct_attachment': {
                'adjunct_left': 50,
                'adjunct_right': 50
            }
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.inventory = {}
        self.order = ['word_order', 'adjunct_attachment']
        for op in self.order:
            self.get_random_method(op)()

    def sov(self):
        self.inventory['sentence'] = '{subj} {obj} {verb}'

    def svo(self):
        self.inventory['sentence'] = '{subj} {verb} {obj}'

    def vso(self):
        self.inventory['sentence'] = '{verb} {subj} {obj}'

    def vos(self):
        self.inventory['sentence'] = '{verb} {obj} {subj}'

    def ovs(self):
        self.inventory['sentence'] = '{obj} {verb} {subj}'

    def osv(self):
        self.inventory['sentence'] = '{obj} {subj} {verb}'

    def adjunct_left(self):
        self.inventory['adjunct_nominal'] = '{adjunct} {nominal}'
        self.inventory['adjunct_verbal'] = '{adjunct} {verb}'

    def adjunct_right(self):
        self.inventory['adjunct_nominal'] = '{nominal} {adjunct}'
        self.inventory['adjunct_verbal'] = '{verb} {adjunct}'

