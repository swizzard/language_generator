# morphology/phonology
from methodselector import MethodSelector
from random import choice, randint


class Phonology(MethodSelector):
    def __init__(self, likelihoods_dict=None, adjustments_dict=None, **likelihoods, **adjustments):
        self.base_vowels = ['a', 'i', 'u']
        self.extra_vowels = ['e', 'o']
        self.base_consonants = ['p', 't', 'k']
        self.extra_consonants = ['b', 'd', 'f', 'g', 'j', 'l', 'm', 'n', 'r', 's', 'z']
        self.base_likelihoods = {
            "v": {"v2": 25,
                  "v3": 25,
                  "v4": 25,
                  "v5": 25
                  },
            "c": {
                "c3": 10,
                "c4": 9,
                "c5": 9,
                "c6": 9,
                "c7": 9,
                "c8": 9,
                "c9": 9,
                "c10": 9,
                "c11": 9,
                "c12": 9,
                "c13": 9
            }
        }
        self.adjustments = {
            'v_adjustment': 0,
            'c_adjustment': 0
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.set_likelihoods_map(self.base_likelihoods.update(likelihoods))
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.adjustments.update(adjustments)

    def v2(self):
        i = randint(0, 2)
        return self.base_vowels.pop(i)

    def v3(self):
        return self.base_vowels

    def v4(self):
        return self.base_vowels.append(choice(self.extra_vowels))

    def v5(self):
        return self.base_vowels + self.extra_vowels

    def get_rand_cons(self, inventory):
        new = None
        while (not new) or (new in inventory):
            new = choice(self.extra_consonants)
        return inventory.append(new)

    def extend_inventory(self, inventory, num):
        while len(inventory) < num:
            inventory = self.get_rand_cons(inventory)
        return inventory

    def c3(self):
        return self.base_consonants

    def c4(self):
        return self.extend_inventory(self.base_consonants, 4)

    def c5(self):
        return self.extend_inventory(self.base_consonants, 5)

    def c6(self):
        return self.extend_inventory(self.base_consonants, 6)

    def c7(self):
        return self.extend_inventory(self.base_consonants, 7)

    def c8(self):
        return self.extend_inventory(self.base_consonants, 8)

    def c9(self):
        return self.extend_inventory(self.base_consonants, 9)

    def c10(self):
        return self.extend_inventory(self.base_consonants, 10)

    def c11(self):
        return self.extend_inventory(self.base_consonants, 11)

    def c12(self):
        return self.extend_inventory(self.base_consonants, 12)

    def c13(self):
        return self.base_consonants + self.extra_consonants

    def get_inventory(self):
        inventory = {
            'V': self.get_random_method('v')(),
            'C': self.get_random_method('c')()
        }
        maxes = {
            'max_CV': len(inventory['C']) * len(inventory['V']),
            'max_CVC': (len(inventory['C']) ** 2) * len(inventory['V']),
            'max_CVV': len(inventory['C']) * (len(inventory['V']) ** 2),
            'max_CVCV': (len(inventory['C']) ** 2) * (len(inventory['V']) ** 2)
        }
        inventory.update(maxes)


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
        templates = {
            'CV': '{c1}{v1}',
            'CVC': '{c1}{v1}{c2}',
            'CVV': '{c1}{v1}{v2}',
            'CVCV': '{c1}{v1}{c2}{v2}'
        }
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
                                           v2=choice(self.phonological_inventory['V'])
                                           )
                else:
                    template = self.get_more_complex_syllable(structure)
            self.syllables.add(syll)
        self.inventory[label] = syll


class Nominal(MethodSelector, MorphemeGeneratorMixin):
    def __init__(self, phonological_inventory, likelihoods_dict=None, adjustments_dict=None, **likelihoods,
                 **adjustments):
        self.phonological_inventory = phonological_inventory
        self.adjustments = {
            'case_adjustment': 0,
            'number_adjustment': 0,
            'gender_adjustment': 0,
            'nominal_agglutinativity_adjustment': 0,
            'pron_drop_adjustment': 0,
            'pron_agreement_adjustment': 0
        }
        self.adjustments.update(adjustments)
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.case = ['nom', 'acc', 'dat', 'gen']
        self.number = ['sg', 'pl', 'dual']
        self.gender = ['masc', 'fem', 'neut']
        self.person = ['1st', '2nd', '3rd']
        self.base_likelihoods = {
            'case': {  # set a flag
                'case_none': 40,
                'case_nom_acc': 35,
                'case_nom_acc_dat': 20,
                'case_nom_acc_dat_gen': 5
            },
            'number': {
                'num_none': 55,
                'num_sg_pl': 40,
                'num_sg_pl_dual': 5
            },
            'gender': {
                'gen_none': 35,
                'gen_pers_nonpers': 30,
                'gen_masc_fem': 25,
                'gen_masc_fem_neut': 10
            },
            'nominal_agglutinativity': {
                'nom_synthetic_before': 25,
                'nom_synthetic_after': 25,
                'nom_agglutinative_before': 25,
                'nom_agglutinative_after': 25
            },
            'pron_drop': {
                'pron_no_drop': 45,
                'pron_drop_subj': 35,
                'pron_drop_both': 20
            },
            'pron_agreement': {
                'pron_pers_num_synthetic_before': 10,
                'pron_pers_num_synthetic_after': 10,
                'pron_pers_num_agglutinative_before': 10,
                'pron_pers_num_agglutinative_after': 10,
                'pron_pers_num_gen_synthetic_before': 10,
                'pron_pers_num_gen_synthetic_after': 10,
                'pron_pers_num_gen_agglutinative_before': 10,
                'pron_pers_num_gen_agglutinative_after': 10,
                'pron_3ps_gen_only': 20  # i.e. he/she/it vs they
            }
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.set_likelihoods_map(self.base_likelihoods.update(likelihoods))
        self.flags = set()
        self.inventory = {}
        self.syllables = set()

    def synthesize(self):
        if self.inventory.get('masc'):
            syll = self.get_more_complex_syllable(self.inventory.get('masc'))
            for number in self.number:
                if self.inventory.get(number, '') != '':
                    for case in self.case:
                        if self.inventory.get(case, '') != '':
                            self.gen_morpheme('masc_{number}_{case}'.format(number=number, case=case), syll)
                    else:
                        if not any([self.inventory.get(case) for case in self.case]):
                            self.gen_morpheme('masc_{number}'.format(number=number), syll)
        if self.inventory.get('fem'):
            if self.inventory.get('fem') == self.inventory.get('masc'):
                for number in self.number:
                    if self.inventory.get(number, '') != '':
                        for case in self.case:
                            if self.inventory.get(case, '') != '':
                                self.inventory['fem_{number}_{case}'.format(number=number, case=case)] = self.inventory.get(
                                    'masc_{number}_{case}'.format(number=number, case=case))
                        else:
                            if not any([self.inventory.get(case) for case in self.case]):
                                self.inventory['fem_{number}'.format(number=number)] = self.inventory.get('masc_{number}'.format(number=number))
            else:
                syll = self.get_more_complex_syllable(self.inventory.get('fem'))
                for number in self.number:
                    if self.inventory.get(number, '') != '':
                        for case in self.case:
                            if self.inventory.get(case, '') != '':
                                self.gen_morpheme('fem_{number}_{case}'.format(number=number, case=case), syll)
                        else:
                            if not any([self.inventory.get(case) for case in self.case]):
                                self.gen_morpheme('fem_{number}'.format(number=number), syll)
        if self.inventory.get('neut'):
            if self.inventory.get('neut') == self.inventory.get('masc'):
                neut_gen = 'masc'
            elif self.inventory.get('neut') == self.inventory.get('fem'):
                neut_gen = 'fem'
            else:
                neut_gen = 'neut'
            if neut_gen != 'neut':
                for number in self.number:
                    if self.inventory.get(number, '') != '':
                        for case in self.case:
                            if self.inventory.get(case, '') != '':
                                self.inventory['neut_{number}_{case}'.format(
                                    number=number, case=case)] = self.inventory.get(
                                        '{neut_gen}_{number}_{case}'.format(neut_gen=neut_gen, number=number, case=case))
                        else:
                            if not any([self.inventory.get(case) for case in self.case]):
                                self.inventory['neut_{number}'.format(number=number)] = self.inventory.get(
                                    '{neut_gen}_{number}'.format(neut_gen=neut_gen, number=number))
            else:
                syll = self.get_more_complex_syllable(self.inventory.get('neut'))
                for number in self.number:
                    if self.inventory.get(number, '') != '':
                        for case in self.case:
                            if self.inventory.get(case, '') != '':
                                self.gen_morpheme('neut_{number}_{case}'.format(number=number, case=case), syll)
                    else:
                        if not any([self.inventory.get(case) for case in self.case]):
                            self.gen_morpheme('neut_{number}'.format(number=number), syll)

    def synthesize_pron(self, gen=False):
        for person in self.person:
            syll = self.get_more_complex_syllable(self.inventory.get(person))
            for number in self.number:
                if self.inventory.get(number, '') != '':
                    for case in self.case:
                        if self.inventory.get(case, ''):
                            if gen:
                                tpl = '{person}_{number}_{gender}_{case}'
                            else:
                                tpl = '{person}_{number}_{case}'
                            for gender in self.gender:
                                if self.inventory.get(gender, '') != '':
                                    self.gen_morpheme(tpl.format(person=person, number=number, case=case,
                                                                 gender=gender), syll)
                            else:
                                if not any([self.inventory.get(gender) for gender in self.gender]):
                                    self.gen_morpheme('{person}_{number}_{case}'.format(person=person,
                                                                                        number=number,
                                                                                        case=case), syll)
            else:
                if not any([self.inventory.get(number) for number in self.number]):
                    for case in self.case:
                        if self.inventory.get(case, '') != '':
                            if gen:
                                tpl = '{person}_{gender}_{case}'
                            else:
                                tpl = '{person}_{case}'
                            for gender in self.gender:
                                if self.inventory.get(gender, '') != '':
                                    self.gen_morpheme(tpl.format(person=person, gender=gender, case=case), syll)
                    else:
                        if gen:
                            for gender in self.gender:
                                if self.inventory.get(gender, '') != '':
                                    self.gen_morpheme('{person}_{gender}'.format(person=person, gender=gender), syll)

    def get_nominal(self, root, gender, number, case):
        nominal = self.inventory.get('nominal')
        features = [self.inventory.get(feature) for feature in [gender, number, case]]
        affix_tpl = ''
        for feature in features:
            if feature:
                affix_tpl += '{feature}_'
        if affix_tpl.endswith('_'):
            affix_tpl = affix_tpl[:-1]
        affix = self.inventory.get(affix_tpl.format(gender=gender, number=number, case=case))
        if not affix:
            affix = '{gender}{number}{case}'.format(gender=self.inventory.get(gender), number=self.inventory.get(number),
                                                    case=self.inventory.get(case))
        return nominal.format(root=root, affix=affix)

    def get_pronoun(self, root, person, gender, number, case):
        pron = self.inventory.get('pron')
        features = [self.inventory.get(feature) for feature in [person, gender, number, case]]
        affix_tpl = ''
        for feature in features:
            if feature:
                affix_tpl += '{feature}_'
        if affix_tpl.endswith('_'):
            affix_tpl = affix_tpl[:-1]
        affix = self.inventory.get(affix_tpl.format(person=person, gender=gender, number=number, case=case))
        if not affix:
            affix = '{person}{gender}{number}{case}'.format(person=self.inventory.get(person),
                                                            gender=self.inventory.get(gender),
                                                            number=self.inventory.get(number),
                                                            case=self.inventory.get(case))
        return pron.format(root=root, affix=affix)

    def person(self):
        for person in self.person:
            self.gen_morpheme(person)

    def case_none(self):
        for case in self.case:
            self.gen_morpheme(case, noop=True)

    def case_nom_acc(self):
        for case in self.case[2:]:
            self.gen_morpheme(case, noop=True)
        self.gen_morpheme('nom')
        self.gen_morpheme('acc')

    def case_nom_acc_dat(self):
        self.gen_morpheme('nom')
        self.gen_morpheme('acc')
        self.gen_morpheme('dat')
        self.gen_morpheme('gen', noop=True)

    def case_nom_acc_dat_gen(self):
        for case in self.case:
            self.gen_morpheme(case)

    def num_none(self):
        for num in self.number:
            self.gen_morpheme(num, noop=True)

    def num_sg_pl(self):
        self.gen_morpheme('sg')
        self.gen_morpheme('pl')
        self.gen_morpheme('dual', noop=True)

    def gen_none(self):
        for gender in self.gender:
            self.gen_morpheme(gender, noop=True)

    def gen_pers_nonpers(self):
        self.gen_morpheme('masc')
        self.inventory['fem'] = self.inventory['masc']
        self.gen_morpheme('neut')

    def gen_masc_fem(self):
        self.gen_morpheme('masc')
        self.gen_morpheme('fem')
        self.inventory['neut'] = choice([self.inventory['masc'], self.inventory['fem']])

    def gen_masc_fem_neut(self):
        for gender in self.gender:
            self.gen_morpheme(gender)

    def nom_synthetic_before(self):
        self.inventory['nominal'] = '{affix}{root}'
        self.synthesize()

    def nom_synthetic_after(self):
        self.inventory['nominal'] = '{root}{affix}'
        self.synthesize()

    def nom_agglutinative_before(self):
        if not self.inventory.get('nominal'):
            self.inventory['nominal'] = '{affix}{root}'

    def nom_agglutinative_after(self):
        if not self.inventory.get('nominal'):
            self.inventory['nominal'] = '{root}{affix}'

    def pron_no_drop(self):
        self.inventory['subj_pronoun'] = self.inventory['pron']
        self.inventory['obj_pronoun'] = self.inventory['pron']

    def pron_drop_subj(self):
        self.inventory['subj_pronoun'] = '({pron})'.format(self.inventory['pron'])
        self.inventory['obj_pronoun'] = self.inventory['pron']

    def pron_drop_both(self):
        self.inventory['subj_pronoun'] = '({pron})'.format(self.inventory['pron'])
        self.inventory['obj_pronoun'] = '({pron})'.format(self.inventory['pron'])

    def pron_pers_num_synthetic_before(self):
        self.inventory['pron'] = '{affix}{root}'
        self.synthesize_pron()

    def pron_pers_num_synthetic_after(self):
        self.inventory['pron'] = '{root}{affix}'
        self.synthesize_pron()

    def pron_pers_num_agglutinative_before(self):
        self.inventory['pron'] = '{case}{number}{person}'

    def pron_pers_num_agglutinative_after(self):
        self.inventory['pron'] = '{person}{number}{case}'

    def pron_pers_num_gen_synthetic_before(self):
        self.inventory['pron'] = '{affix}{root}'
        self.synthesize_pron(gen=True)

    def pron_pers_num_gen_synthetic_after(self):
        self.inventory['pron'] = '{root}{affix}'
        self.synthesize_pron(gen=True)

    def pron_pers_num_gen_agglutinative_before(self):
        self.inventory['pron'] = '{case}{number}{gender}{person}{root}'

    def pron_pers_num_gen_agglutinative_after(self):
        self.inventory['pron'] = '{root}{person}{gender}{number}{case}'

    def pron_3ps_gen_only(self):
        self.gen_morpheme('pron_3ppl_root')
        if not self.inventory.get('nominal'):
            self.get_random_method('nominal_agglutinativity')()
        self.inventory['pron_3ppl'] = self.inventory['nominal'].format(root=self.inventory['pron_3ppl_root'])
        new_pron_method = self.get_random_method('pron_agreement')
        while new_pron_method == self.pron_3ps_gen_only:
            new_pron_method = self.get_random_method('pron_agreement')
        new_pron_method()


class Verbal(MethodSelector, MorphemeGeneratorMixin):
    def __init__(self, phonological_inventory, nominal_instance, likelihoods_dict=None, adjustments_dict=None,
                 **likelihoods, **adjustments):
        self.phonological_inventory = phonological_inventory
        self.adjustments = {
            'tense_adjustment': 0,
            'indir_objs_adjustment': 0,
            'agreement_adjustment': 0,
            'verbal_agglutinativity_adjustment': 0
        }
        self.adjustments.update(adjustments)
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.nominal_instance = nominal_instance
        self.base_likelihoods = {
            'tense': {
                'tense_nonpst_pst': 50,
                'tense_pres_pst_fut': 30,
                'tense_none': 20
            },
            'indir_objs': {  # check if any([self.nominal_instance.inventory.get(case) for case in self.nominal_instance.case])
                'io_prepositional': 50,
                'io_case': 50
            },
            'agreement': {
                'vagr_none': 40,
                'vagr_3ps_non3ps': 30,
                'vagr_pers_only': 20,
                'vagr_pers_num': 10
            },
            'verbal_agglutinativity': {
                'verb_synthetic': 50,
                'verb_agglutinative': 50
            }
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.set_likelihoods_map(self.base_likelihoods.update(likelihoods))
        self.flags = set()
        self.inventory = {}
        self.syllables = set()


class Other(MethodSelector, MorphemeGeneratorMixin):
    def __init__(self, phonological_inventory, nominal_instance, likelihoods_dict=None, adjustments_dict=None,
                 **likelihoods, **adjustments):
        self.phonological_inventory = phonological_inventory
        self.adjustments = {
            'prep_position_adjustment': 0,
            'poss_prep.adjustment': 0,
            'neg_adjustment': 0,
            'neg_position_adjustment': 0,
            'art_kinds_adjustment': 0,
            'art_positions_adjustment': 0,
            'art_agreement_adjustment': 0,
            'art_proper_names_adjustment': 0
        }
        self.adjustments.update(adjustments)
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.nominal_instance = nominal_instance
        self.base_likelihoods = {
            'prep_position': {
                'prep_before_affixed': 23,
                'prep_after_affixed': 23,
                'prep_before_separate': 23,
                'prep_after_separate': 23,
                'prep_circum': 8  # always affixed
            },
            'poss_prep': {  # if no case, 100% present, treat as regular prep
                'poss_none_before_acc': 10,  # i.e. no poss prep, possessor in acc follows possessee
                'poss_none_before_dat': 10,  # if no dat, just use acc
                'poss_none_after_acc': 10,
                'poss_none_after_dat': 10,
                'poss_unless_gen_acc': 25,
                'poss_unless_gen_dat': 25,
                'poss_even_gen': 10
            },
            'neg': {
                'neg_nom_and_verb_same': 70,
                'neg_nom_and_verb_diff': 30
            },
            'neg_position': {
                'neg_before': 60,
                'neg_after': 40
            },
            'art_kinds': {  # do before other art stuff
                'art_none': 40,  # set a flag
                'art_def_only': 22,
                'art_indef_only_one': 11,  # i.e. indef art (root) same as word for 1
                'art_indef_only_not_one': 11,
                'art_both_indef_one': 8,
                'art_both_indef_not_one': 8
            },
            'art_position': {  # ignore if no arts (check flags)
                'art_before_affixed': 25,
                'art_after_affixed': 25,
                'art_before_separate': 25,
                'art_after_separate': 25
            },
            'art_agreement': {  # ignore if no arts (check flags)
                'art_no_agr': 40,
                'art_num_only': 25,
                'art_pers_num': 20,
                'art_pers_num_case': 15
            },
            'art_proper_names': {  # ignore if no arts (check flags)
                'art_with_names': 50,
                'art_not_with_names': 50
            }
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.set_likelihoods_map(self.base_likelihoods.update(likelihoods))
        self.inventory = {}
        self.syllables = set()




# V #this is the vowel set, between like 2 and 6
# C #this is the consonant set, between 2 and like 15
#
# pronouns = ['1st', '2nd', '3rd']  #these are all pulled from the Lipzig gloss https://en.wikipedia.org/wiki/List_of_glossing_abbreviations
# plurality = ['SG', 'PL']
# gender = [0, 1, 3] #is there any gender? if so how many
# tenses = ['PRES', 'IMPERF', 'FUT', 'PST'] #how many tenses exist?
# indefinite = [1, 2, 3, 4] #how many indefinite endings are there?
# indobj = [0, 1, 2, 3] #are there indirect objects? if so how many?
# dirobj = [0, 1, 2, 3] #how many direct objects are required?
# neg = [1, 2, 3, 4]#how many negative markers are required?
# poss = [1, 2, 3]# how many possessive markers
# q = [1, 2, 3] #how many question words are there?
# vt = [0, 1, 2, 3] #are there transitive verbs? how many objects do they require?