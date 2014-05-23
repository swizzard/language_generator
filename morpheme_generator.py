from random import choice

from methodselector import MethodSelector, StringRedis
from phono import Phonology


class MorphemeGeneratorMixin(MethodSelector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.syllables = set()

    def map_syll_to_structure(self, syll):
        vowels = self.connection.get(Phonology.construct_key('V'))
        if len(syll) == 2:
            return 'CV'
        elif len(syll) == 4:
            return 'CVCV'
        else:
            if syll[-1] in vowels:
                return 'CVV'
            else:
                return 'CVC'

    def get_more_complex_syllable(self, syll):
        if not syll:
            return 'CV'
        structure = self.map_syll_to_structure(syll)
        hierarchy = self.config['hierarchy']
        try:
            return hierarchy[hierarchy.index(structure) + 1]
        except IndexError:
            return hierarchy[0]

    def gen_morpheme(self, label, syll_structure='CV', noop=False):
        structure = syll_structure.capitalize()
        if noop:
            syll = ''
        else:
            syll = None
            template = self.config['templates'][structure]
            max_syll = self.connection.get('max_{}'.format(structure))
            vowels = self.connection.get(Phonology.construct_key('V'))
            consonants = self.connection.get(Phonology.construct_key('C'))
            while (not syll) or syll in self.syllables:
                if len(self.syllables) < max_syll:
                    syll = template.format(c1=choice(consonants),
                                           v1=choice(vowels),
                                           c2=choice(consonants),
                                           v2=choice(vowels))
                else:
                    template = self.get_more_complex_syllable(structure)
            self.syllables.add(syll)
        self.connection.hset(self.construct_key('inventory'), label, syll)
        self.inventory[label] = syll