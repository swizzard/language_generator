from random import choice

class MorphemeGeneratorMixin:
    def map_syll_to_structure(self, syll):
        if len(syll) == 2:
            return 'CV'
        elif len(syll) == 4:
            return 'CVCV'
        else:
            if syll[-1] in self.inventory['V']:
                return 'CVV'
            else:
                return 'CVC'

    def get_more_complex_syllable(self, syll):
        if not syll:
            return 'CV'
        structure = self.map_syll_to_structure(syll)
        hierarchy = ['CV', 'CVC', 'CVV', 'CVCV']
        try:
            return hierarchy[hierarchy.index(structure) + 1]
        except IndexError:
            return hierarchy[0]

    def gen_morpheme(self, label, syll_structure='CV', noop=False):
        structure = syll_structure.capitalize()
        templates = {'CV': '{c1}{v1}', 'CVC': '{c1}{v1}{c2}', 'CVV': '{c1}{v1}{v2}', 'CVCV': '{c1}{v1}{c2}{v2}'}
        if noop:
            syll = ''
        else:
            syll = None
            template = templates[structure]
            while (not syll) or syll in self.syllables:
                if len(self.syllables) < self.inventory['max_{}'.format(structure)]:
                    syll = template.format(c1=choice(self.phonological_inventory['C']),
                                           v1=choice(self.phonological_inventory['V']),
                                           c2=choice(self.phonological_inventory['C']),
                                           v2=choice(self.phonological_inventory['V']))
                else:
                    template = self.get_more_complex_syllable(structure)
            self.syllables.add(syll)
        self.inventory[label] = syll