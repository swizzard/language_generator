# morphology/phonology


from phono_setup import phonolen


V #this is the vowel set, between like 2 and 6
C #this is the consonant set, between 2 and like 15

pronouns = ['1st', '2nd', '3rd']  #these are all pulled from the Lipzig gloss https://en.wikipedia.org/wiki/List_of_glossing_abbreviations
plurality = ['SG', 'PL']
gender = [0, 1, 3] #is there any gender? if so how many
tenses = ['PRES', 'IMPERF', 'FUT', 'PST'] #how many tenses exist? 
indefinite = [1, 2, 3, 4] #how many indefinite endings are there?
indobj = [0, 1, 2, 3] #are there indirect objects? if so how many?
dirobj = [0, 1, 2, 3] #how many direct objects are required?
neg = [1, 2, 3, 4]#how many negative markers are required?
poss = [1, 2, 3]# how many possessive markers
q = [1, 2, 3] #how many question words are there?
vt = [0, 1, 2, 3] #are there transitive verbs? how many objects do they require?