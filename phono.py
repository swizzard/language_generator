from random import choice, randint

from methodselector import MethodSelector


class Phonology(MethodSelector):
    def __init__(self, likelihoods_dict=None, adjustments_dict=None):
        self.base_vowels = ['a', 'i', 'u']
        self.extra_vowels = ['e', 'o', 'y', 'ə', 'ɪ', 'ɒ', 'ɑ', 'œ', 'ʏ', 'ɯ' 'ʉ', 'ɨ', 'ɵ', 'ɛ', 'ʊ', 'ɔ', 'æ',
                             'ɐ', 'ɜ', 'ʌ', 'ø']
        self.base_consonants = ['p', 't', 'k']
        self.extra_consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
                                 'v', 'w', 'x', 'z', 'ʍ', 'ɹ', 'θ', 'ʃ', 'ð', 'ɸ', 'ɣ', 'ɥ', 'ɟ', 'ɬ', 'ʒ', 'χ',
                                 'ç', 'ʋ', 'β', 'ɲ', 'ʀ', 'ɢ', 'ʟ', 'ʙ', 'ɴ', 'ɽ', 'ʈ', 'ʂ', 'ʑ', 'ŋ', 'ɱ']
        self.base_likelihoods = {
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
             'get_inventory': {
                 'get_inventory': 100
             }
        }
        self.adjustments = {
            'v_adjustment': 0,
            'c_adjustment': 0
        }
        if isinstance(likelihoods_dict, dict):
            self.base_likelihoods.update(likelihoods_dict)
        self.set_likelihoods_map(self.base_likelihoods)
        if isinstance(adjustments_dict, dict):
            self.adjustments.update(adjustments_dict)
        self.inventory = self.get_inventory()

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
        inventory = {'V': self.get_random_method('v')(), 'C': self.get_random_method('c')()}
        maxes = {'max_CV': len(inventory['C']) * len(inventory['V']), 'max_CVC': (len(inventory['C']) ** 2) * len(
            inventory['V']),
                 'max_CVV': len(inventory['C']) * (len(inventory['V']) ** 2), 'max_CVCV': (len(inventory['C']) ** 2) * (len(inventory['V']) ** 2)}
        inventory.update(maxes)
        return inventory
