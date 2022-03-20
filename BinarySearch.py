''' Performs binary search to find value of x such that:
	target_output = func(x)
	or alternatively: x = func^-1(target_output)

	Was re-writing this code too much, so I made a general module for re-use
'''

import math #just needed for examples section

def binary_search(func, target_output, lower, upper, tolerance = 0.0001, max_iter = 50):
	''' Performs binary search to find value of x such that:
	target_output = func(x)
	or alternatively: x = func^-1(target_output)

	Arguments:
		func {function} -- This is the function to use
		target_output {int} -- The target value of the function
		lower {float} -- Initial lower bound for search
		upper {float} -- Initial upper bound for search

	Optional Arguments:
		tolerance {float} -- Once abs(func(x) - target_output) < tolerance, then the search stops
		max_iter {int} -- Maximum number of binary search iterations (to prevent infinite loop if no convergance)
	'''

	if abs(lower) > abs(upper):
		upper, lower = lower, upper #swap upper and lower

	guess = (lower + upper) / 2
	for i in range(max_iter):
		estimate = func(guess)
		print(f'Iter {i} Guess {guess} F(guess) = {estimate}, L = {lower}, U = {upper}')
		if abs(target_output - estimate) < tolerance:
			return guess

		if estimate < target_output:
			lower = guess
			guess = (lower + upper)/2	
		else:
			upper = guess
			guess = (lower + upper)/2

	return guess

if __name__ == '__main__':

	########################################
	#------------ EXAMPLES ZONE ------------
	########################################

	#converges to 5
	est = binary_search(func = lambda x: x**2, target_output = 25, lower = 0, upper = 25)
	print(f'Estimate: {est}')
	print('\n-----------------------------------------------------------------------------\n')

	#converges to -2020/305 ~= -6.62295
	f = lambda x: x * math.floor(x * math.floor(x * math.floor(x)))
	est = binary_search(func = f, target_output = 2020, lower = - 8, upper = -6)

	print(f'Estimate: {est}')

