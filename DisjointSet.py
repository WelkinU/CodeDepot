''' This file contains 2 implementations of a Disjoint Set data structure.

Implementation #1 (class DisjointSet):
    Represents a single level uptree data structure using a list of lists/ints
    lists represent sets, ints represent pointers to sets

Implementation #2 (class DisjointSetNumpy):
    Represents a single level uptree data structure with a numpy array. 
    Union operation is slightly less efficient for very large disjoint sets.
'''

import numpy as np

class DisjointSet:

    def __init__(self, initial_size = 0):
        ''' Representing disjoint set using an UpTree structure. Using a single level uptree instead of multilevel.

        Using a list of lists/ints, structure to store the disjoint set structure
        lists are disjoint set groupings, ints are index pointers to their respective groupings '''

        if initial_size > 0:
            self.sets = [[i] for i in range(initial_size)]
        else:
            self.sets = []

    def __getitem__(self, idx):
        ''' Magic method to allow indexing into the disjoint set like this:
        myDisjointSet[my_index] 

        Returns the set associated with the input index.
        '''

        if isinstance(self.sets[idx], int):
            return self.sets[self.sets[idx]] #if index is pointer, return set it points to
        else:
            return self.sets[idx] #if index is a set, return the set

    def __str__(self):
        ''' Magic method to print internal state of object like this:
        print(myDisjointSet)'''

        return str(self.sets) 

    def addIndex(self):
        ''' Use this function to add an index to the disjoint set. 
        Use the initial_size argument to initialize disjoint set with many indicies.'''

        self.sets.append([len(self.sets)])

    def union(self, i1, i2):
        ''' Set union the sets including indicies i1 and i2 and update pointers to maintain
        a single level uptree'''

        #if either i1 or i2 are points, replace their value with the pointer
        if isinstance(self.sets[i1], int):
            i1 = self.sets[i1]
        if isinstance(self.sets[i2], int):
            i2 = self.sets[i2]

        if i1 == i2: #check if i1 and i2 point to the same set, if so we're done
            return

        i1, i2 = min(i1,i2), max(i1,i2) #check to make sure i1 <= i2, this is an UPtree after all

        self.sets[i1].extend(self.sets[i2])

        #update pointers to avoid multi-level uptree, and keep only single level uptree
        #update values for the whole set to avoid pointers to other pointers (multilevel uptree)
        #first value in self.sets[i1] is a self reference to top level set, so can't update it without deleting the set
        for i in self.sets[i1][1:]:
            self.sets[i] = i1


class DisjointSetNumpy:

    def __init__(self, initial_size = 0):
        self.sets = np.arange(initial_size)
        
    def addItem(self):
        ''' Add an index to the disjoint set'''
        self.sets.append(len(sets))

    def union(self,i1, i2):
        ''' Unions sets containing indicies i1 and i2.
            
            Very simple code, but union is linear instead of constant time update.
        '''
        self.sets[self.sets == self.sets[(max(i1,i2))]] = self.sets[min(i1,i2)]
