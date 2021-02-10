# qlearningAgents.py
# ------------------
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

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent): ## now we are computing q-values instead of values
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        # structure dict to store Q(s,a), so mapping tuples (state, action) to its value
        self.values = util.Counter() # init the structure where the q-values (s,a) will be stored
        # the key will be the state and action: and from this key will get a q-value

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state, action) not in self.values: # q-state exists?
          self.values[(state, action)] = 0.0 # if it's the first time
        return self.values[(state, action)] # if not just return the value
        # util.raiseNotDefined()


    def computeValueFromQValues(self, state): # to calc maxQ(s,a) = V(s) that corresponds to the future expected utility
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state) #do we have legal actions?
        if len(legalActions) == 0:
          return 0.0 # if there's no legal action -> terminal state?
        tmp = util.Counter() # temporal hash to store the maximum
        for action in legalActions: #explore all the legal actions
            tmp[action] = self.getQValue(state, action)
        return tmp[tmp.argMax()] # return the maximum Q(state, action), returning the max q-value
        # util.raiseNotDefined()

    def computeActionFromQValues(self, state): # needed for policy extraction, extract the best action possible till the moment
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state) #do we have legal actions?
        if len(legalActions) == 0:
          return None
        tmp = util.Counter() # temporal hash
        for action in legalActions: # explore all the legal actions
            tmp[action] = self.getQValue(state, action)
        return tmp.argMax() # now we extract the action that maximizes the expected state value
        # util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state) # get actions cuz we'll need to decide among them
        action = None
        "*** YOUR CODE HERE ***"
        if len(legalActions) != 0: # are there some legal actions?
          if util.flipCoin(self.epsilon): # as we are using random choice, we simply flip a coin -> modelling that by using epsilon
            action = random.choice(legalActions) # take a random action -> exploration
          else:
            action = self.computeActionFromQValues(state) # the best action (max), follow the best policy learned till now -> exploitation
        return action
        #util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        oldQValue = self.values[(state, action)] # this the utility the system thinks 
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        # self.values[(state, action)] = (1 - self.alpha) * oldQValue + self.alpha * sample
        self.values[(state, action)] = oldQValue + self.alpha * (sample - oldQValue) # alegraic developing from the previous notation
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state) # we want to extract the actions from the Q-Values got -> policy extraction

    def getValue(self, state):
        return self.computeValueFromQValues(state) # get the Value of a State from its Q-Values, to evaluation how good or bad is it -> policy evaluation


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter() # we are not storing anymore the expected q-values, but we are using weighted features to know how good is a q-state

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action): # calc the q-value at a specific moment, from the currently weights applied to each feature
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action) # list of features -> functions that let us know how good or bad is a specific state depending on the factor computed
        qvalue = 0
        for f in features: # for each feature, we weighted it by its weight -> linear function where Q(s,a) = w1·f1(s,a) ... wn·fn(s,a)
          qvalue += self.getWeights()[f] * features[f]
        return qvalue
        # util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # to calc the difference
        features = self.featExtractor.getFeatures(state, action)
        sample = reward + self.discount * self.computeValueFromQValues(nextState)
        oldQValue = self.getQValue(state, action) # now is not returned the expected q-value, but the weighted featured q-value
        difference = sample - oldQValue

        # iteration
        for f in features:
          self.weights[f] = self.weights[f] + self.alpha * (difference) * features[f] # updating the weights
        # util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
