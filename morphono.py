# morphology/phonology
from methodselector import MethodSelector
from random import choice, randint


class Phonology(MethodSelector):
    def __init__(self):
        self.base_vowels = ['a', 'i', 'u']
        self.extra_vowels = ['e', 'o']
        self.base_consonants = ['p', 't', 'k']
        self.extra_consonants = ['b', 'd', 'f', 'g', 'j', 'l', 'm', 'n', 'r', 's', 'z']
        self.set_likelihoods_map({
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
        })

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
        new = choice(self.extra_consonants)
        while new in inventory:
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

    def get_inventory(self, cons_adjustment=0, vowel_adjustment=0):
        return {"V": self.get_random_method("v", vowel_adjustment)(),
                "C": self.get_random_method("c", cons_adjustment)()}


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