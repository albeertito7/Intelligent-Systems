# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

# answerNoise: refers to how often an agent ends up in an unintended successor state when they perform an action

def question2():
    answerDiscount = 0.9 # putting this value = 1, doesn't matter cuz of a noisy movement of 0.2 by default affecting the pacman might never be able to cross the bridge
    answerNoise = 0 # changing this value we set up that pacman chose the action that wants
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.5 # high enough to enable pacman to explore till the exit +1
    answerNoise = 0 # to not get into the pit
    answerLivingReward = -1 # great penalty to take risks
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.5 # high enough to enable pacman to explore till the exit +1
    answerNoise = 0.2 # set high enough to make pacman not to take the risks, and lower enough to enable pacman to exit the close exit +1
    answerLivingReward = -1 # great penalty to take risks
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.999 # prioritize the learning over the learned, so pacman achieves the 10 points
    answerNoise = 0 # pacman is not afraid of the pit, cuz controls at all its actions
    answerLivingReward = -1 # high penalty => take risks
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.2
    answerNoise = 0.5 # higher noisy => pacman doesn't want to take risk cuz maybe it will get into the pit
    answerLivingReward = 1 # positive living reward => pacman CONSERVATIVE
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.999 # doesn't matter, but setting it we assure that pacman really knows about 10 points exit but prefers to get the living reward
    answerNoise = 0 # controls all of its movements
    answerLivingReward = 1000 # pacman will be always in the grid world
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE' # because of the epsilon doesn't let us chose our actions, it's just a random choice always
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))