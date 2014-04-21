from random import randint, sample
#random.seed()


V = ['a', 'e', 'i', 'o', 'u']
C = ['b', 'k', 'd', 'f', 'g', 'j', 'l', 'm', 'n', 'r', 'p', 's', 'z']

'''Vowels_N = randint(2, 5)#choose the number of vowels for the language
print (Vowels_N)
Lang_V = sample(V,Vowels_N) #out of the number of vowels, randomly pick those from the list
print (Lang_V)

Consonants_N = randint(3, 13)#choose the number of consonants for each language
print (Consonants_N)
Lang_C = sample(C, Consonants_N) #out of the number of consonants, randomly pick those from the list
print (Lang_C)
'''

def phonolen(type):
    N  = randint(2,len(type)) #choose the number of V or C for each language
    Lang = sample(type, N)  ##out of the number of V or C, randomly pick those from the list
    return Lang

print (phonolen(V))
print (phonolen(C))