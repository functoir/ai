#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements A* search, an informed Graph Search algorithms
    that attempts to find the best path in a by considering the path cost
    from the source to the current node and a precomputed heuristic
    estimate of the shortest distance from shortest distance from the
    current node to the desired goal state.
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai", "Alberto Quattrini Li"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

from SearchSolution import SearchSolution
from PriorityQueue import PriorityQueue

# define global constant for infinite weight
INFINITY = 2**20

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost
        

    def priority(self):
        """Return the current Node's priority value.
            This value is the sum of the transition cost
            to the Node and the heuristic estimating distance
            to the goal state.
        """
        return self.heuristic + self.transition_cost

    # Comparators for the heapq module.
    # These functions are used ot devise an ordering for AstarNode instances,
    # in order to arrange them in the priority queue.
    def __gt__(self, other):
        return self.priority() > other.priority()
    
    def __lt__(self, other):
        return self.priority() < other.priority()
    
    def __eq__(self, other):
        return self.priority() == other.priority()
    
    def __ge__(self, other):
        return self.priority() >= other.priority()
    
    def __le__(self, other):
        return self.priority() <= other.priority()
    

def backchain(node):
    """
        Backtrack and rebuild the path generated by the search.
    """
    
    # initialize an array to hold the sequence of states in the path.
    result = []
    current = node
    
    # backtrack until the root node is reached, 
    # i.e. a node is found whose predecessor is None.
    while current:
        
        # append states to the path.
        result.append(current.state)
        current = current.parent

    # reverse the path to get the correct order, and return the result.
    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    """Run A* search on the search problem with the specified heuristic function."""
    
    # initialize the handler for the search solution.
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)
    
    # initialize the start node and priority queue,
    # then push the start node into the queue.
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    queue = PriorityQueue()
    queue.push(start_node)

    # initilize a dictionary to hold states and associated costs
    # to avoid evaluating paths that have been superseded by lesser-cost paths.
    visited_cost = {}
    visited_cost[start_node.state] = 0

    # while priority queue is not empty (i.e. there are still nodes to explore)...
    while queue:
        
        # get node in front of priority queue and check it's state.
        current_node = queue.pop()
        current_state = current_node.state
        
        # if the node has been superseded by another node (for the same state) 
        # that had a lesser cost, skip the current node
        # and proceed to the next node in the queue.
        if visited_cost[current_state] != current_node.transition_cost:
            continue
            
        solution.nodes_visited = solution.nodes_visited + 1
        
        # if current state the goal state, backtrack and rebuild the path.
        if search_problem.is_goal(current_state):
            solution.cost = visited_cost[current_state]
            solution.path = backchain(current_node)
            break
        
        # if current node is not the goal state:
        #   1. get cost of current state and compute cost for next state.
        current_cost = current_node.transition_cost
        next_cost = current_cost + 1
        
        #   2. get all possible next states for the current state
        #   3. for each next state, calculate the cost of the transition 
        #      using the cost to current, transition cost, and heuristic and cost to current.
        for next_state in search_problem.get_successors(current_state):
        
            #   4. if a node's new cost is more favorable than its current cost,
            #      save the new cost to the costs dictionary and push it into the priority queue.
            if visited_cost.get(next_state, INFINITY) > next_cost:
                visited_cost[next_state] = next_cost
                next_node = AstarNode(next_state, heuristic_fn(next_state),
                                      parent=current_node, transition_cost=next_cost)
                queue.push(next_node)
                

    # once the priority queue is empty or an exit occurs 
    # (i.e. a goal state has been found), return the solution.
    return solution
