from methodselector import MethodSelector
from morphono import Phonology, Nominal, Verbal, Other, MorphemeGeneratorMixin
from random import randint

class Syntax(MethodSelector):
    def __init__(self, nominal_instance, verbal_instance, other_instance, likelihoods_dict=None, adjustments_dict=None):
        self.nominal_instance = nominal_instance
        self.verbal_instance = verbal_instance
        self.other_instance = other_instance
        self.adjustments = {
            'word_order_adjustment': 0,
            'adjunct_attachment_adjustment': 0
        }
        self.adjustments.update(adjustments)
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
        self.set_likelihoods_map(self.base_likelihoods.update(likelihoods))
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


class Master(MorphemeGeneratorMixin):
    def __init__(self, phonological_adjustments=None, syntax_adjustments=None, nominal_adjustments=None,
                 verbal_adjustments=None, other_adjustments=None, phonological_likelihoods=None,
                 syntax_likelihoods=None, nominal_likelihoods=None, verbal_likelihoods=None,
                 other_likelihoods=None):
        self.phonological_instance = Phonology(phonological_likelihoods, phonological_adjustments)
        self.nominal_instance = Nominal(self.phonological_instance.inventory, nominal_likelihoods, nominal_adjustments)
        self.verbal_instance = Verbal(self.phonological_instance.inventory, self.nominal_instance, verbal_likelihoods,
                                      verbal_adjustments)
        self.other_instance = Other(self.phonological_instance.inventory, self.nominal_instance, other_likelihoods,
                                    other_adjustments)
        self.syntax_instance = Syntax(self.nominal_instance, self.verbal_instance, self.other_instance,
                                      syntax_likelihoods, syntax_adjustments)
        self.inventory = {}
        self.lexicon = {}

    def gen_lexical_element(self, word, pos=None, syll='cv'):
        if word not in self.inventory:
            self.gen_morpheme(word, self.get_more_complex_syllable(syll))
        self.lexicon[pos][word] = self.inventory.get(word)

    def get_lexical_element(self, word, pos):
        elem = self.inventory.get(word)
        if not elem:
            self.gen_lexical_element(word, pos)
            elem = self.inventory.get(word)
        return elem

    def build_sentence(self, *words):
        nom_elems = ['obj', 'subj']
        elems = dict([(word[1], (self.get_lexical_element(word[0], word[1]) ,word[2])) for word in words])
        struct = self.syntax_instance.inventory.get('sentence')  # e.g {subj}{verb}{obj}
        parts = [info[0] for info in elems.values()]
        if 'prep_verbal' in parts:
            struct = struct.format(
                verb=self.syntax_instance.inventory.get('adjunct_verbal').format(adjunct=),
                                   object='{obj}', subj='{subj}')
        if 'prep_subj' in parts:
            struct = struct.format(verb='{verb}', obj='{obj}', subj=self.syntax_instance.inventory.get(
                'adjunct_nominal').format(nominal='{subj}', adjunct='{adjunct}'))
        if 'prep_obj' in parts:
            struct = struct.format(verb='{verb}', subj='{subj}', obj=self.syntax_instance.inventory.get(
                'adjunct_nominal').format(nominal='{obj}', adjunct='{adjunct}'))

        if 'neg_verbal' in parts:
            struct = struct.format(subj='{subj}', obj='{obj}', verb=self.other_instance.inventory.get('neg_vp').format(
                neg_verbal=self.inventory.get('neg_verbal'), verb='{verb}'))
        if 'neg_subj' in parts:
            struct = struct.format(obj='{obj}', verb='{verb}', subj=self.other_instance.inventory.get('neg_np').format(
                neg_nominal=self.other_instance.inventory.get('neg_nominal'), nominal='{subj}'))
        if 'neg_obj' in parts:
            struct = struct.format(subj='{subj}', verb='{verb}', obj=self.other_instance.inventory.get('neg_np').format(
                neg_nominal=self.other_instance.inventory.get('neg_nominal'), nominal='{obj}'))
        if 'poss_subj' in parts:
            poss_phrase = self.other_instance.inventory.get('poss_phrase')
            possessor = elems.pop('possessor')
            possessor = self.nominal_instance.get_nominal(root=possessor[0], gender=possessor[1].get('gender'),
                                                          number=possessor[1].get('number'),
                                                          case=poss_phrase[1:4])
            struct = struct.format(verb='{verb}', obj='{obj}',
                                   subj=self.other_instance.inventory.get('poss_phrase').format(nominal='{subj}',
                                                                                                acc_nominal=possessor,
                                                                                                dat_nominal=possessor,
                                                                                                gen_nominal=possessor))
        if 'poss_obj' in parts:
            poss_phrase = self.other_instance.inventory.get('poss_phrase')
            possessor = elems.pop('possessor')
            possessor = self.nominal_instance.get_nominal(root=possessor[0], gender=possessor[1].get('gender'),
                                                          number=possessor[1].get('number'),
                                                          case=poss_phrase[1:4])
            struct = struct.format(verb='{verb}', subj='{subj}',
                                   obj=self.other_instance.inventory.get('poss_phrase').format(nominal='{obj}',
                                                                                                acc_nominal=possessor,
                                                                                                dat_nominal=possessor,
                                                                                                gen_nominal=possessor))
        if 'indir_obj' in parts:
            io_phrase = self.other_instance.inventory.get('indir_obj')
            io = elems.pop('indir_obj')
            if 'acc' in io_phrase:
                case = 'acc'
            elif 'dat' in io_phrase:
                case = 'dat'
            elif 'gen' in io_phrase:
                case = 'gen'
            else:
                case = 'nom'
            io = self.nominal_instance.get_nominal(root=io[0], gender=io[1].get('gender'), number=io[1].get('number'),
                                                   case=case)
            io_phrase = io_phrase.format(
                prep1=self.other_instance.inventory.get('prep_io'),
                prep2=self.other_instance.inventory.get('prep_io2', ''),
                nominal=io)

            l = struct.split('}')
            l = [x + '}' for x in l if x]
            l.insert(randint(0,len(l)), 'io_phrase')
            struct = ' '.join(l)
        for elem in elems:
