import numpy as np
from utils import entropy
from wordle import Wordle, WordleInference

## Not great, has names
with open('words.txt', 'r') as f:
    allwords = f.read().split()

secret_word = input('Enter secret word: ') # TODO: make script to take hint output from Wordle webpage

word_bank = [w for w in allwords if len(w) == len(secret_word)]
np.random.shuffle(word_bank) # enables starting with random choice from all high entropy words
guess = word_bank[np.argmax([entropy(w) for w in word_bank])] #start guess

wordle = Wordle(secret_word)
inferer = WordleInference(len(secret_word), word_bank, secret_word)
for t in range(6):
    print('\nguess', t+1)
    flags = wordle.verify(guess)
    if wordle.solved:
        print(f'solved word "{guess}" in {t+1} steps')
        break

    inferer.update_priors(guess, flags)
    guess = inferer.next_guess(t)