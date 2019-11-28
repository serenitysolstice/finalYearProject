#http://norvig.com/spell-correct.html
#Souce of the base code, 20/02/19, written by Peter Norvig
#Last updated by him in August 2016
#Couple of edits made, and annotated, to better suit my needs.

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('C:\\Users\\user\\Documents\\major_project\\A collection of scientists in Wales between 1804 and 1919 built using Natural Language Processing techniques\\software\\textfiles\\english-words\\words.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`." 
    if '-' in word: #replace hyphens in articles or processed text starts getting complicated
        word = word.replace('-', ' ')
    letters    = """abcdefghijklmnopqrstuvwxyz"""
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#Added third edits function - makes the code take longer to run, but should add more accuracy.
'''def edits3(word):
    "All edits that are three edits away from 'word'"
    return (e3 for el in edits1(word) for e3 in edits1(el))'''