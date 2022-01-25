import numpy as np
from utils import ALLCAPS, chunks, compare, count_c, has_valid_char, is_unordered_sublist, entropy

class Wordle:
    """class to simulate Wordle game"""
    def __init__(self, word):
        self.word = word
        self.length = len(word)
        self.history = [] # unused outside class
        self.solved = False
    
    def show_flags(self, guess, flags):
        """print guess along with its flags side by side"""
        for c in guess:
                print(ALLCAPS[c], '', end='')
        print()
        for f in flags:
            print(f, '', end='')
        print()
    
    def verify(self, guess):
        """Verify if guess is correct, and if not gives clues (Green, Yellow, Gray)"""
        # include try/catch to make sure green letters are there? (not in game)
        flags = []
        c_encounter = {c:count_c(c, self.word) for c in set(self.word)}
        if guess == self.word:
            print('correct!')
            flags = ['+' for i in range(self.length)]
            self.solved = True
            return
        word2word = compare(guess, self.word)
        for ix, b in enumerate(word2word):
            char = guess[ix]
            ## GREEN right character, right position
            if b:
                flags.append('+') #green
                c_encounter[char] -= 1
            else:
                ## YELLOW right character, wrong position
                ## accounts for character count. e.g., if character count of 1
                ## and shown yellow flag, should be gray on its next encounter in the guess word
                if char in self.word and c_encounter[char] > 0: 
                    flags.append('!') #yellow
                    c_encounter[char] -= 1
                ## GRAY no such character
                else:
                    flags.append('-')
        
        self.history.append(flags)
        self.show_flags(guess, flags)
        return flags
    
class WordleInference:
    """Contains features/inference data and guesses correct word based off hints"""
    def __init__(self, length, word_bank, truth=None):
        self.optimal = ['_' for i in range(length)] # fixes green letters
        self.word_bank = word_bank
        self.priority_char = [] #accounts for repeated char (hence a list)
        self.char_bank = {c for c in 'abcdefghijklmnopqrstuvwxyz'}
#         self.null_opt =  ['_' for i in range(length)] # _____
        self.candidate_hist = dict()
        
        #debugging
        self.truth = truth #ground truth
        
    def update_priors(self, guess, flags):
        """ Update inferred word features based on flags
        theoretically like gradient descent
        """
        priority_seen = set(self.priority_char) #Yellow characters seen from previous guess
        for ix, (c, f) in enumerate(zip(guess, flags)):
            if f == '+': # Green
                self.optimal[ix] = c
            elif f == '!' and c not in priority_seen: # Yellow
                self.priority_char.append(c)
            elif f == '-' and c not in self.priority_char + self.optimal: # Gray, second boolean for edge case
                try:
                    self.char_bank.remove(c)
                except KeyError: # for duplicate absent letters
                    pass
        try:
            self.word_bank.remove(guess)
        except ValueError: #list.remove(x): x not in list TODO WHY IS THIS HAPPENING HERE
            pass

    def next_guess(self, it=None): #it: debug iteration
        """Find most likely next guess based on updated priors in previous step"""
        candidates = []
#         preferred_candidates = [] # for those with letters that match exactly
        word_bank = self.word_bank.copy()
        for w in word_bank:
            ## skip words with gray letters
            if not has_valid_char(w, self.char_bank):
                self.word_bank.remove(w)
                continue
            ## skip words without yellow letters
            if not is_unordered_sublist(self.priority_char, w):
                self.word_bank.remove(w)
                continue
            
            ## Comparing green letters
            # compare these two variables to decide if candidate
            fixed_char_count = 0 #number of green letters
            w_sim_count = 0  # see if current word shares the above
            for ix, c in enumerate(self.optimal):
                if c != '_':
                    fixed_char_count += 1
                    if w[ix] == c:
                        
                        w_sim_count += 1
            if fixed_char_count == w_sim_count:
                candidates.append(w)
            else:
                self.word_bank.remove(w)
                if len(candidates) == 0: #worst case scenario
                    candidates.append(w)
                    self.word_bank.append(w)
                
        self.candidate_hist[it] = candidates
        return candidates[np.argmax([entropy(w) for w in candidates])] 