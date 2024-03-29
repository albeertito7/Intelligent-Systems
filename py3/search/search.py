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
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    ## util.raiseNotDefined()
    startingNode = problem.getStartState()

    stack = util.Stack() ## create the stack ## LIFO (Last-In First-Out)
    visitedNodes = [] ## create the list of visited nodes

    stack.push((startingNode, [])) ## push the startingNode with the list of actions empty cuz it's the beginning one

    while not stack.isEmpty(): ## if the stack is empty means all the tree nodes were visited, so the search is finished
        currentNode, actions = stack.pop() ## retrieve the tuple

        if problem.isGoalState(currentNode): ## terminal test
            return actions ## return the actions

        if currentNode not in visitedNodes: ## if not visited
            visitedNodes.append(currentNode) ## add current node if it's the first time when visited

            for nextNode, action, cost in problem.getSuccessors(currentNode): ## for each successor add it and the its action path to the stack
                newAction = actions + [action] ## the newAction path, add the new action the get the succesor to the action path list done till now
                stack.push((nextNode, newAction))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    ## util.raiseNotDefined()
    startingNode = problem.getStartState()

    queue = util.Queue() ## create the queue ## FIFO (First-In First-Out)
    visitedNodes = []
    queue.push((startingNode, []))

    while not queue.isEmpty():
        currentNode, actions = queue.pop()

        if problem.isGoalState(currentNode):
                return actions

        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                newAction = actions + [action]
                queue.push((nextNode, newAction))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ## util.raiseNotDefined()
    startingNode = problem.getStartState()

    queue = util.PriorityQueue() ## using a priority queue
    visitedNodes = []
    queue.push((startingNode, [], 0), 0) ## structure: ((node, actions path to the node, cost), priority)

    while not queue.isEmpty():

        currentNode, actions, prevCost = queue.pop()

        if problem.isGoalState(currentNode):
            return actions

        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                newAction = actions + [action]
                priority = prevCost + cost ## resolving the next cost/priority
                queue.push((nextNode, newAction, priority), priority)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ## util.raiseNotDefined()
    startingNode = problem.getStartState()

    pQueue = util.PriorityQueue()
    visitedNodes = []
    pQueue.push((startingNode, [], 0), 0)

    while not pQueue.isEmpty():

        currentNode, actions, prevCost = pQueue.pop()
        
        if problem.isGoalState(currentNode):
                return actions

        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)

            for nextNode, action, cost in problem.getSuccessors(currentNode):
                newAction = actions + [action]
                newCostToNode = prevCost + cost
                heuristicCost = newCostToNode + heuristic(nextNode,problem)
                pQueue.push((nextNode, newAction, newCostToNode),heuristicCost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
