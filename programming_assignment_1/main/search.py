# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    from util import Stack
    from game import Directions

    # the component of tree is (state, the path to the state)
    tree = Stack()
    tree.push((problem.get_start_state(), [])) #set path of the state to empty

    # store the visited state
    visited = [] #set the visited state to empty
    final = []
    while(not tree.is_empty()): #while the tree still has path/grid to visit
        (state, path) = tree.pop() 
        if(problem.is_goal_state(state)): 
            final = path
            return final
        successors = problem.get_successors(state) 
        for successor in successors:
            if(successor.state not in visited):  # any state has been visited doesn't need to be visited again
                visited.append(successor.state)
                tree.push((successor.state, path + [successor.action]))
    return path 


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()
    from util import Queue
    from game import Directions

    # the component of tree is (state, the path to the state)
    tree = Queue()
    tree.push((problem.get_start_state(), [])) #set path of the state to empty

    # store the visited state
    visited = [] #set the visited state to empty
    final = []
    while(not tree.is_empty()): #while the tree still has path/grid to visit
        (state, path) = tree.pop() 
        if(problem.is_goal_state(state)): 
            final = path
            return final
        successors = problem.get_successors(state) 
        for successor in successors:
            if(successor.state not in visited):  # any state has been visited doesn't need to be visited again
                visited.append(successor.state)
                tree.push((successor.state, path + [successor.action]))
    return path 


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0
    
def heuristic1(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y     = problem.goal
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        
        optimisitic_number_of_steps_to_goal = abs(goal_x-pacman_x) + abs(goal_y-pacman_y)
        return optimisitic_number_of_steps_to_goal
    # 
    # traveling-salesman problem (collect multiple food pellets)
    # 
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position
        
        # YOUR CODE HERE (set value of optimisitic_number_of_steps_to_goal)
        min_dis = 10000
        food = food_grid.as_list() 
        if not food:
            return 0
        max_dis = 0

        for food in food:
            food_x, food_y = food
            key = position + food
            if key in problem.heuristic_info:
                distance = problem.heuristic_info[key]
            else:
                # Use manhattan distance to calculate
                distance = abs(food_x - pacman_x) + abs(food_y - pacman_y)
                problem.heuristic_info[key] = distance

            if distance > max_dis:
                max_dis = distance

        return max_dis
        '''
        for food_position in food_grid:
            food_x, food_y = food_position
            min_dis = min(min_dis, abs(food_x-pacman_x) + abs(food_y-pacman_y))

        optimisitic_number_of_steps_to_goal = min_dis
        print(optimisitic_number_of_steps_to_goal)
        return optimisitic_number_of_steps_to_goal
        '''

class Node():
    cost = 0
    total_cost = 0
    state = None
    action = None
    parent_node = None

    def __init__(self, cost, total_cost, state, action, parent_node):
        self.cost = cost
        self.total_cost = total_cost
        self.state = state
        self.action = action
        self.parent_node = parent_node

    def __lt__(self, other):
        return self.total_cost < other.total_cost


def a_star_search(problem, heuristic=heuristic1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "* YOUR CODE HERE *"
    from queue import PriorityQueue
    from game import Directions

    # the component of tree is (state, the path to the state)
    tree = PriorityQueue()

    tree.put(Node(0, 0, problem.get_start_state(), None, None))  # set path of the state to empty

    # store the visited state
    visited = set()  # set the visited state to empty

    while (not tree.empty()):  # while the tree still has path/grid to visit
        
        parent_node = tree.get()
        while (parent_node.state in visited):
            parent_node = tree.get()
        current_state = parent_node.state
        visited.add(current_state)
        
        if (problem.is_goal_state(current_state)):
            path = []
            trace_node = parent_node
            while trace_node.parent_node is not None:
                path.insert(0, trace_node.action)
                trace_node = trace_node.parent_node
            return path
        
        successors = problem.get_successors(current_state)
        for successor in successors:
            new_cost = parent_node.cost + successor.cost
            new_total_cost = parent_node.cost + successor.cost + heuristic(successor.state, problem)
            tree.put(Node(new_cost, new_total_cost, successor.state, successor.action, parent_node))
    return path

    # What does this function need to return?
    #     list of actions that reaches the goal
    # 
    # What data is available?
    #     start_state = problem.get_start_state() # returns a string
    # 
    #     problem.is_goal_state(start_state) # returns boolean
    # 
    #     transitions = problem.get_successors(start_state)
    #     transitions[0].state
    #     transitions[0].action
    #     transitions[0].cost
    # 
    #     print(transitions) # would look like the list-of-lists on the next line
    #     [
    #         [ "B", "0:A->B", 1.0, ],
    #         [ "C", "1:A->C", 2.0, ],
    #         [ "D", "2:A->D", 4.0, ],
    #     ]
    # 
    # Example:
    """
    start_state = problem.get_start_state()
    example_path = []
    current_state = start_state
    for i in range (0,10):    
        transitions = problem.get_successors(current_state)
        ### calculate which transition be the best from current state


        ### pick action i based on calculation
        i = 0
        example_path.append(transitions[i].action)
        current_state = transitions[i].state
        

        ### if current_state is goal_state terminate
    
    path_cost = problem.get_cost_of_actions(example_path)
    
    return example_path
    """
    util.raise_not_defined()


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search