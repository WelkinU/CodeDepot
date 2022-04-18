''' American and European Options Pricing based off binomial option model.
Uses the math described here https://youtu.be/L8hMr07F4k8?t=300

Toggle the early_exercise variable to switch between American (True) and
European (False) options.

Intended to be extensible to trinomial model as well (only have to update
get_binomial_replicating_value_cash() function)

'''
import queue
from numpy import linalg

class Node:
    ''' A class that represents the state of a particular node in the tree.
    Technically could be replaced with a dictionary for compatibility with 
    tree visualization libraries that take JSON data. I chose to use a class
    instaed of a dict because it seemed more descriptive'''

    def __init__(self, parent, current_value, time, children = [], id = None ):
        self.parent = parent
        self.children = children
        self.time = time
        self.current_value = current_value
        self.id = id

        #to be calculated
        self.option_value = None

    def __str__(self):
        return f'''
            ID: {self.id}
            Parent node ID: {self.parent}
            Children node ID's: {self.children}
            Time: {self.time}
            Current Value: {self.current_value}
            Option Value: {self.option_value}
            '''.replace('    ','')

    def __eq__(self, other):
        if self.current_value == other.current_value and self.time == other.time:
            return True
        else:
            return False

class OptionPricingTree:
    ''' From initial conditions, builds a tree of Node objects representing the Binomial option price model.

    Also calculates option intrinsic value and value in continuing down the tree (comparison used for early
    option exercise if selected)
    '''

    def __init__(self,  initial_price: float = 100, 
                        strike: float = 100, 
                        option_type: str = 'put', 
                        early_exercise: bool = True, 
                        time_periods: int = 3,
                        next_step_change: list = [1.07, 1/1.07], 
                        next_step_prob: list = [0.5, 0.5],
                        risk_free_rate_per_period: float = 1.01,
                        debug: bool = True):
        '''
        Arguments:
        initial_price {float} -- Initial price of the stock
        strike {float} -- The option strike price
        option_type {str} -- The type of option. Either "call" or "put"
        early_exercise {bool} -- American option (True) or European option (False)
        time_periods {int} -- The number of time steps (aka. the number of tree layers after the root)
        next_step_change {list} -- List of floats describing multipliers to get to the next state.
                                    Each non-terminal node in the tree has a child with an element in this list
                                    multiplied by the parent's current price
        next_step_prob {list} -- This doesn't actually matter to the model... But it's the probability of
                                choosing a branch described in the next_step_change variable. Must be same
                                length.
        risk_free_rate_per_period {float} -- The risk free rate of return per time period. Generally will
                                            be a float >= 1
        debug {bool} -- Show debug output, like when early exercise is happening
        '''

        #do some error checking
        assert option_type in ['call','put'], 'option_type must be "call" or "put"'
        assert time_periods > 0, f'time_periods ({time_periods}) must be greater than 0'
        assert sum(next_step_prob) == 1, f'Next step probabilities must sum to 1. Sum = {sum(next_step_prob)}'
        assert len(next_step_change) == len(next_step_prob), \
            f'next_step_change ({len(next_step_change)} must have same len as next_step_prob {len(next_step_prob)}'
        assert max(next_step_change) > risk_free_rate_per_period > min(next_step_change), 'U > R > D must be satisfied'

        #initialize some self variables
        self.initial_price = initial_price
        self.strike = strike
        self.option_type = option_type
        self.early_exercise = early_exercise
        self.time_periods = time_periods
        self.next_step_change = next_step_change
        self.next_step_prob = next_step_prob
        self.risk_free_rate = risk_free_rate_per_period
        self.debug = debug

        #create the tree, and calculate option values
        self.create_tree()
        self.compute_option_values()
    
    def create_tree(self):
        #initialize root node
        self.all_nodes = [Node(parent = None,
                                current_value = self.initial_price,
                                time = 0, 
                                id = 0)]

        q = queue.SimpleQueue()
        q.put(0) #put root index in queue
        
        while not q.empty():
            current_node_idx = q.get()

            if self.all_nodes[current_node_idx].time < self.time_periods:
                #add child nodes to parent
                for multiplier, prob in zip(self.next_step_change, self.next_step_prob):
                    #create child node to add
                    node_id_to_add = len(self.all_nodes)
                    node_to_add = Node(parent = current_node_idx,
                                        current_value = round(self.all_nodes[current_node_idx].current_value * multiplier, 3),
                                        time = self.all_nodes[current_node_idx].time + 1,
                                        id = node_id_to_add)

                    if node_to_add not in self.all_nodes:
                        #add the node to our list of all nodes
                        self.all_nodes.append(node_to_add)

                        #update parent to point to the node we're adding
                        self.all_nodes[current_node_idx].children = self.all_nodes[current_node_idx].children + [node_id_to_add]

                        #add pointer to our newly created to the queue of nodes to process
                        q.put(node_id_to_add)

                    else:
                        #Two parent nodes can point to same child in lattice structure
                        #for this to happen, the child will have same current_value and time_step
                        #in this case, we just point parent to already existing node 
                        #(don't need to update other parent in this exercise)
                        self.all_nodes[current_node_idx].children = self.all_nodes[current_node_idx].children + [self.all_nodes.index(node_to_add)]


    def compute_option_values(self):
        #compute option intrinsic value at each node
        for idx in range(len(self.all_nodes)):
            self.all_nodes[idx].option_value = round(self.get_option_intrinsic_value(self.all_nodes[idx]),3)

        
        #use reversed() to work backward
        for idx in reversed(range(len(self.all_nodes))):
            if len(self.all_nodes[idx].children) > 0:
                #expected value calculation
                value_of_continuing = self.get_binomial_replicating_value_cash(self.all_nodes[idx])
                value_of_continuing = round(value_of_continuing, 3) #rounding for display purposes
                
                if self.early_exercise:
                    #handle early stopping in American options
                    if self.all_nodes[idx].option_value > value_of_continuing:
                        if self.debug:
                            print(f'Early exercise on node {idx}. Option value ({self.all_nodes[idx].option_value}) > Value of Continuing ({value_of_continuing})')

                    self.all_nodes[idx].option_value = max(self.all_nodes[idx].option_value, value_of_continuing)

                else: 
                    self.all_nodes[idx].option_value = value_of_continuing

    def get_option_intrinsic_value(self, n: Node):
        if self.option_type == 'call':
            return max(n.current_value - self.strike, 0)
        else: #put option
            return max(self.strike - n.current_value,0)

    def get_binomial_replicating_value_cash(self, n: Node):
        assert len(self.next_step_change) == 2, 'Method only used for binary trees!'
        u = max(self.next_step_change)
        d = min(self.next_step_change)

        #get risk neutral probs
        q = (self.risk_free_rate - d) / (u - d)

        #get child expected values
        child_option_values = [self.all_nodes[idx].option_value for idx in n.children]
        option_value = (q * child_option_values[0] + (1-q) * child_option_values[1]) / self.risk_free_rate
        return option_value

#########################################################
#---------------- EXAMPLES / TESTING ZONE ---------------
#########################################################

if __name__ == '__main__':
    t = OptionPricingTree()
    
    #print state of all nodes
    #for node in t.all_nodes:
    #    print(node)
    
    print(f'Computed option price: {t.all_nodes[0].option_value}')