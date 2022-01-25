import numpy as np

ALLCAPS = {l:u for (l,u) in zip('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')}

## BASIC HELPER FUNC
def chunks(w):
    return [e for e in w]

def compare(w1, w2):
    """First round of comparing: positional comparison"""
    return [a==b for (a,b) in zip(w1, w2)]

def count_c(c, w):
    """counts characters in w (can be list or str)"""
    return len([e for e in w if e==c])

def has_valid_char(word, char_bank):
    """Check if word has chars found in char_bank"""
    return len(set(word) - char_bank) == 0

def is_unordered_sublist(sub, super_):
    """check if sub is contained in super_ (both iterables)"""
    bools = []
    for c in set(sub):
        if c in super_ and count_c(c, sub) <= count_c(c, super_): # <= in case the priority_char added less than the actual word
            bools.append(1)
        else:
            bools.append(0)
            
    return 0 not in bools

## INFO THEORY
def entropy(word):
    """Shannon Entropy of a string"""
    prob_log_prob = []
    for c in set(word):
        p = count_c(c, word)/len(word)
        prob_log_prob.append(p*np.log(p))
    return -sum(prob_log_prob)