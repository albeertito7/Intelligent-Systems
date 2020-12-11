# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent): ## just look at ur possible actions and apply a functions about how good would be the actions but just think one step ahead, not building a tree as the minimax function
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState): ##the action every time the pacman has to move
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        ##print legalMoves

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores) ##computes the higher value of the scores retrieved
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        print legalMoves[chosenIndex]
        ##raw_input("Continue?")
        return legalMoves[chosenIndex] ##return an action of the possible moves

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) ## result action, if in a state we apply an action returns de new state
        newPos = successorGameState.getPacmanPosition() ## which is the new position of the pacman in the new state?
        newFood = successorGameState.getFood() ## whish is the new position map of the food?
        newGhostStates = successorGameState.getGhostStates() ## which is the ghoststates?
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] ## Can pacman eat the ghost in this new state?

        print "Action", action
        print "NewPos", newPos
        print "NewFood", newFood #false (F) no foow, true (T) there is food 

        ## first of all lets have a look at the food, then we'll focus on the ghosts

        "*** YOUR CODE HERE ***"
        ## return successorGameState.getScore() ## need to return the score

        old_food = currentGameState.getFood() ## old food state, is a matrix
        total_score = 0.0 ## our personal score to be returned

        for x in xrange(old_food.width):
          for y in xrange(old_food.height):
            if old_food[x][y]: ## if there is food
              d = manhattanDistance((x, y), newPos) ## compute the right angle distance between food coordinates and new pacman position
              if d==0: ## if its next to the pacman
                  total_score += 100 ## add a good value to the score
              else:
                total_score += 1.0/(d*d) ## add a value depending on the distance

        ## need to consider not only the food but also the position of the ghost that must affect the score too 
        for ghost in newGhostStates:
          d = manhattanDistance(ghost.getPosition(), newPos)
          if d<=1:
            if(ghost.scaredTimer != 0):
              total_score += 2000
            else:
              total_score -= 200

        ## also would be so interesting to consider the capsules/fruits and if it's good or not to eat these ones
        ## for now we are considering them as the highest valueble elements, not applying any kind of condition
        for capsule in currentGameState.getCapsules():
          d = manhattanDistance(capsule, newPos) 
          if d==0:
            total_score += 3000
          else:
            total_score += 1.0/(d*d)

        return total_score
        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent): ## class for the minimax
    """
      Your minimax agent (question 2)

      - to work with any number of ghosts
      - minimax tree
        - multiple min layers (one for each ghost) for every max layer
        - expand the tree a ply, stop algorithm till one depth cuz the tree is too huge

    """

    def getAction(self, gameState): ## this the minimax-decision function that returns an action using minimax algorithm
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ## implementation functions for doing minimax-decision algorithm
        import sys
        
        ## transition model, defines the result (newGameState) of an agent's action in a gameState
        def result(gameState, agent, action):
          return gameState.generateSuccessor(agent, action)
        
        ## return the set of legal actions of an agent in a specific state
        def actions(gameState, agent):
          return gameState.getLegalActions(agent)

        ## defines the final numeric value for a game that ends in terminal state
        def utility(gameState):
          return self.evaluationFunction(gameState)

        ## which is true when the game is over, otherwise is false
        def terminalTest(gameState, depth): ## how much depth is left? how much further pacman can go through the tree? ## self.depth is not this one
          return depth == 0 or gameState.isWin() or gameState.isLose()

        ## 
        def max_value(gameState, agent, depth):
          if terminalTest(gameState, depth): ## is a terminal state or need to stop going deeper
            return utility(gameState) ## returns the score value
          v = -sys.maxint ## represents minus infinite, temporal variable, need to find the max of the minimum value
          for action in actions(gameState, agent): ## iterate through the set of legal actions
            ## getting the max between thee temporal var and the min_value result function
            ## min_value: gets the min utility value of the gameStates from applying the action
            v = max(v, min_value(result(gameState, agent, action), 1, depth)) ## 1 cuz the next agent is the first ghost
          return v

        ##
        def min_value(gameState, agent, depth):
          if terminalTest(gameState, depth):
            return utility(gameState)
          v = sys.maxint ## represents infinite, temporal variable, need to find the min of the values
          for action in actions(gameState, agent):
            if(agent == gameState.getNumAgents()-1): ## minus 1 cuz the max player needs to be removed from the agents count
              v = min(v, max_value(result(gameState, agent, action), 0, depth-1)) ## 0 cuz the next player to move is the max one, depth-1 we got a move
            else:
              v = min(v, min_value(result(gameState, agent, action), agent+1, depth)) ## the same depth, a move is not completed
          return v

        ## return action!!! ## minimax-decision algorithm applied
        v = -sys.maxint
        actionSet = []
        for action in actions(gameState, 0): ## agent 0 (pacman) which is the one who apply the minimax-decision function
          u = min_value(result(gameState, 0, action), 1, self.depth) ## the depth specified for the user ## 1 cuz the next agent is 0+1, a ghost
          if u == v:
            actionSet.append(action)
          elif u > v:
            v = u
            actionSet = [action]
        
        ## need to return the action that pacman must take
        return random.choice(actionSet) ## random choice between all minimax actions got

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

