# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations ## the depth
        self.values = util.Counter() # A Counter is a dict with default 0 ## hash value, going to store the v values

        # Write value iteration code here
        "*** YOUR CODE HERE ***" ## in the code we must update the self.values
        for i in range(self.iterations):
            values = util.Counter() ## totalCount

            ## need to explore all the states
            for state in self.mdp.getStates(): ##
                ##compute all q-values for each possible action for the state
                QValueForAction = util.Counter() ## keys are actions, values are q-values
                for action in self.mdp.getPossibleActions(state):
                    ## update the hash of q-values
                    QValueForAction[action] = self.computeQValueFromValues(state, action)
                values[state] = QValueForAction[QValueForAction.argMax()]
            self.values = values ## at the end, update values to go to the next step


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action): ## returns the Q-value of the (state, action) pair given by the value function given by self.values
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        QValue = 0

        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            QValue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])

        return QValue
        ##util.raiseNotDefined()

    def computeActionFromValues(self, state): ## computes the best action according to the value function given by self.values
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state): return None

        QvalueForAction = util.Counter()

        for action in self.mdp.getPossibleActions(state):
            QvalueForAction[action] = self.computeQValueFromValues(state, action)
        
        return QvalueForAction.argMax()
        ##util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
