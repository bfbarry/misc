# Wordle Solver

Given the color coded hints, solves the Wordle puzzle. 
TODO: make script to take hint output from Wordle webpage

guess.py illustrates the algorithm given a secret word
```
Enter secret word: knoll

guess 1
B R U I N 
- - - - ! 

guess 2
E N O C H 
- + + - - 

guess 3
K N O W S 
+ + + - - 

guess 4
correct!
solved word "knoll" in 4 steps
```

(in some rarish cases it doesn't finish in 6 steps :/ )
## algorithm

1. start with n-letter word with highest entropy
2. Retrieve hints from Wordle game
3. Update priors based on hints
4. Iterate over remaining word bank and make next best guess based on:
    - remaining letters bank: if a word doesn't have a letter in the letter bank, reject
    - Given priority ("yellow") letters: if a word doesn't have one, reject
    - Given fixed ("green") letters: if a word doesn't have letters there, reject


Theory/Data science questions:
- are there any words for which it is very hard for this algorithm (or human) to guess within 6 tries?
- Look into distribution of guess times