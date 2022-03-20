# Various Coding Challenges

This repository's goal is to be a way to share/host some small independent scripts that don't need a whole repo.

## Generalized Threes Challenge Solver (GeneralizedThreesChallengeSolver.py)

The problem: Make each equation true using mathematical operations. You should be able to do all except 10 with just add, subtract, multiply, divide, factorial, sqrt. Problem from: https://www.youtube.com/watch?v=SkP2VBzgpKA

![Threes Challenge](images/ThreesChallenge.png)

This code takes an arbitrary input tuple, in this case (3,3,3), and does a breadth first search of the space of possible solutions to find all valid integer solutions. The code prints all valid solutions and path to reach those solutions.

Notes

- The input tuple can be any length, and have any integers on it. 
- To add your own functions, just add them to the list join_functions or inplace_modifier_functions and the code will incorperate those into the search.