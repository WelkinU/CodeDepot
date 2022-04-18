''' Solver for the generalized solution of "The 3's Challenge" puzzle described here:
from https://www.youtube.com/watch?v=SkP2VBzgpKA

This solver can take any starting tuple (even tuples with length other than 3).

Solver can also be configured to use any combination of allowable functions. Currently, it
does addition, subtraction, multiplication, division, factorial and sqrt.
- Modify the join_functions list to add functions with 2 inputs and 1 output.
- Modify the inplace_modifier_functions list to add functions with 1 input and 1 output.
'''

import queue
import math
from pprint import pprint
import operator #for basic Python functions. Docs: https://docs.python.org/3/library/operator.html#module-operator


def find_combinations(starting_tuple = (3,3,3), output_lower_bound = 0, output_upper_bound = 10, max_iter = 1000):
	''' Uses a breadth first search to search the space of possible tuple mutations.
	Outputs the integer solutions and the steps to achieve that solution.

	Arguments:
	starting_tuple {tuple} -- Tuple representing the initial problem state. Tuple can be any length > 0 (not just length 3).
	output_lower_bound {int} -- The lower limit of integer solutions to print() out.
	output_upper_bound {int} -- The up limit of integer solutions to print() out. Used to avoid excessive solution printing
									of integer output like 720 = 6!, that people may not care about
	max_iter {int} -- The maximum number of BFS iterations (to cap runtime in case of very large search spaces)

	'''
	assert output_lower_bound <= output_upper_bound

	#########################################################
	#------------------ ADD FUNCTIONS HERE ------------------
	#########################################################
	#These functions have 2 inputs and 1 output
	join_functions = [
		operator.add,
		operator.sub,
		operator.mul,
		special_divide, #handles divide by zero, maintains int typing
	]

	#These functions have 1 input and 1 output
	inplace_modifier_functions = [
		math.factorial,
		math.sqrt,
	]
	#########################################################

	q = queue.SimpleQueue()
	q.put(starting_tuple)

	tuple_library = {starting_tuple: None}

	i = 0
	while not q.empty():
		i += 1
		if i >= max_iter:
			print('Exceeded iteration limit. Breaking search.')
			break

		tuple_to_mutate = q.get()
		new_tuple_list = []
		if len(tuple_to_mutate) > 1: 
			#create all mutations of the tuple_to_mutate that can be created with functions in list join_functions
			for func in join_functions:				
				for idx in range(len(tuple_to_mutate) - 1):
					
					try:
						#generate next tuple via mutating with a joining function
						new_tuple = (*tuple_to_mutate[0:idx],
									func(tuple_to_mutate[idx], tuple_to_mutate[idx + 1]),
									*tuple_to_mutate[idx+2:]
									)

						new_tuple_list.append(new_tuple)
					except ZeroDivisionError:
						pass  #catch zero divides, and zero mod() divides
					except Exception as e:
						print(f'You have an error in your join_function: {e}')

		#create all mutations of the tuple to mutate, this time using only inplace modifier functions
		for func in inplace_modifier_functions:
			for idx in range(len(tuple_to_mutate)):

				val = func(tuple_to_mutate[idx])
				if float(val).is_integer(): #add this check so sqrt(4) -> 2 (int) instead of 2.0 (float)
					val = int(val)

				new_tuple = (*tuple_to_mutate[0:idx], 
							val,
							*tuple_to_mutate[idx+1:])
				
				new_tuple_list.append(new_tuple)

		#check if mutations are valid and undiscovered, if they are, add them to tuple library and queue for future mutation
		for new_tuple in new_tuple_list:
			if new_tuple not in tuple_library.keys():

				# check if we converged to a new integer solution, then print out our discovery!
				if len(new_tuple) == 1 and new_tuple[0] is not None and float(new_tuple[0]).is_integer(): 
					if output_lower_bound<= new_tuple[0] <= output_upper_bound:
						print(f'Discovered {new_tuple[0]}')
						temp = tuple_to_mutate
						while temp is not None:
							print(f'<- {temp} ', end = '')
							temp = tuple_library[temp]
						print('')

						q.put(new_tuple) #we do want to add the tuple back to the queue because inplace operations can still be used

					tuple_library[new_tuple] = tuple_to_mutate #add to library of tuples discovered
					continue

				#otherwise, check if this tuple is valid, if so add it to the tuple library, and
				#add to the queue of new tuples for future mutation
				if validate_tuple(new_tuple):
					tuple_library[new_tuple] = tuple_to_mutate
					q.put(new_tuple)

	#pprint(tuple_library) #pretty print the final library of all discovered tuples
	print(f'Completed after {i} iterations')


def validate_tuple(t, min_value = 0, max_value = 100):
	''' Used to prune tuples that are not needed for further mutation in breadth first search.

	Filters out tuples with non-integer values, invalid values (divide by zero, etc.),
	or where values exceed lower/upper range limits (we don't need to consider 720 factorial
	for example). 
	
	Arguments:
	t {tuple} -- Tuple to validate
	min_value {int} -- Tuples containing values less than this amount will be filtered out from BFS
	max_value {int} -- Tuples containing values greater than this amount will be filtered out from BFS
	'''

	for val in t:
		#throw out tuples that don't meet this condition
		if val is None or not float(val).is_integer() or val < min_value or abs(val) > max_value:
			return False

	return True


def special_divide(x,y):
	if y == 0:
		return None #basically tell validate_tuple() it's invalid

	#this isn't strictly necessary, could return x/y, but this preserves int, 
	#rather than float conversion. Looks better when you print it out.
	if x % y == 0:
		return int(x//y) 
	else:
		return None #basically tell validate_tuple() it's invalid


if __name__ == '__main__':
	import argparse

	def input_tuple(s):
		'''Special validator for --tuple argument'''
		try:
			ret = tuple([int(x) for x in s.split(',')])
			return ret
		except:
			raise argparse.ArgumentTypeError("--tuple argument must be in form --tuple x1,x2,x3 ...")

	parser = argparse.ArgumentParser()
	parser.add_argument('--tuple', help="Starting tuple, can be any length. Example Usage: --tuple 3,3,3", type=input_tuple, default = '3,3,3')
	parser.add_argument('--lower', type=int, default=0, help='Lower bound for integers solutions to detect.')
	parser.add_argument('--upper', type=int, default=10, help='Upper bound for integers solutions to detect.')
	parser.add_argument('--maxiter', type=int, default=1000, help='Maximum number of tuples to queue in the breadth-first-search. Intended to cap runtime in case of very large search spaces')
	args = parser.parse_args()

	find_combinations(starting_tuple = args.tuple, output_lower_bound = args.lower, output_upper_bound = args.upper)

	