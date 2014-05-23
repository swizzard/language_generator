CONFIG = {
    'redis':
        {},
    'Phonology': {
        'base_likelihoods': {
            "v": {
                "v2": 25,
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
             },
        },
        'adjustments': {
            'v_adjustment': 0,
            'c_adjustment': 0
        },
        'base_vowels': ['a', 'i', 'u'],
        'extra_vowels': ['e', 'o', 'y', 'ə', 'ɪ', 'ɒ', 'ɑ', 'œ', 'ʏ', 'ɯ' 'ʉ', 'ɨ', 'ɵ', 'ɛ', 'ʊ', 'ɔ', 'æ', 'ɐ', 'ɜ',
                          'ʌ', 'ø'],
        'base_consonants': ['p', 't', 'k'],
        'extra_consonants': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w',
                              'x', 'z', 'ʍ', 'ɹ', 'θ', 'ʃ', 'ð', 'ɸ', 'ɣ', 'ɥ', 'ɟ', 'ɬ', 'ʒ', 'χ', 'ç', 'ʋ', 'β', 'ɲ',
                              'ʀ', 'ɢ', 'ʟ', 'ʙ', 'ɴ', 'ɽ', 'ʈ', 'ʂ', 'ʑ', 'ŋ', 'ɱ']
    },
    'MorphemeGeneratorMixin': {
        'hierarchy': ['CV', 'CVC', 'CVV', 'CVCV'],
        'templates': {'CV': '{c1}{v1}', 'CVC': '{c1}{v1}{c2}', 'CVV': '{c1}{v1}{v2}', 'CVCV': '{c1}{v1}{c2}{v2}'}
    },
    'Nominal': {
        'base_likelihoods': {
            'person': {
                'person': 100
            },
             'case': {
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
                 'pron_3ps_gen_only': 20 # i.e. he/she/it vs they
            }
        },
        'adjustments': {
            'case_adjustment': 0,
            'number_adjustment': 0,
            'gender_adjustment': 0,
            'nominal_agglutinativity_adjustment': 0,
            'pron_drop_adjustment': 0,
            'pron_agreement_adjustment': 0},
        'case': ['nom', 'acc', 'dat', 'gen'],
        'number': ['sg', 'pl', 'dual'],
        'gender': ['masc', 'fem', 'neut'],
        'person': ['1st', '2nd', '3rd']
    }
}