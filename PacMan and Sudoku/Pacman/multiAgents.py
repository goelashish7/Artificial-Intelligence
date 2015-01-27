#!/usr/bin/python
# -*- coding: utf-8 -*-
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from util import manhattanDistance
from game import Directions
import random
import util
from time import time
from game import Agent


class ReflexAgent(Agent):

    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """

        # Collect legal moves and successor states

        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions

        scores = [self.evaluationFunction(gameState, action)
                  for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores))
                       if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

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

        successorGameState = \
            currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        if successorGameState.isWin():
            return float('inf')
        if currentGameState.isLose():
            return -float('inf')
        (scaredGhosts, activeGhosts) = ([], [])
        #Find which ghosts are active/Scared
        for ghost in currentGameState.getGhostStates():
            if not ghost.scaredTimer:
                activeGhosts.append(ghost)
            else:
                scaredGhosts.append(ghost)
        currentPos = newPos
        ActiveghostDistance = map(lambda x: \
                                  util.manhattanDistance(currentPos,
                                  x.getPosition()), activeGhosts)
        #Find nearest active ghost to pacman
        if len(ActiveghostDistance) == 0:
            manhattanDistanceToClosestGhost = 0
        else:
            manhattanDistanceToClosestGhost = min(ActiveghostDistance)
        score = max(manhattanDistanceToClosestGhost, 3) \
            + successorGameState.getScore()

        ScaredghostDistance = map(lambda x: \
                                  util.manhattanDistance(currentPos,
                                  x.getPosition()), scaredGhosts)
        #Find nearest scary ghost to pacman
        if len(ScaredghostDistance) == 0:
            manhattanDistanceToClosestScaredGhost = 0
        else:
            manhattanDistanceToClosestScaredGhost = \
                min(ScaredghostDistance)
        score += manhattanDistanceToClosestScaredGhost * -1

        foodlist = newFood.asList()
        foodDistance = map(lambda x: util.manhattanDistance(currentPos,
                           x), foodlist)
        if len(foodDistance) == 0:
            closestfoodDistance = 0
        else:
            closestfoodDistance = min(foodDistance)
        #If number of foods are less in successor state then assign big cost
        if currentGameState.getNumFood() \
            > successorGameState.getNumFood():
            score += 100
        if action == Directions.STOP:
            score -= 3
        #Closest food would decrease the score least
        score -= 3 * closestfoodDistance
        #To encourage pacman to move towards capsulte,we give it a very high score
        capsuleplaces = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in capsuleplaces:
            score += 120
        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):

    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        def miniMax(
            gameState,
            depth,
            agentindex,
            numghosts,
            MaxPlayer,
            ):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if MaxPlayer:
                v = -float('inf')
                legalActions = gameState.getLegalActions(0)
                for action in legalActions:
                    v = max(v, miniMax(gameState.generateSuccessor(0,
                            action), depth, 1, numghosts, False))
                return v
            else:
                v = float('inf')
                legalActions = gameState.getLegalActions(agentindex)
                if agentindex == numghosts:
                    for action in legalActions:
                        v = min(v,
                                miniMax(gameState.generateSuccessor(agentindex,
                                action), depth - 1, 0, numghosts, True))
                else:
                    for action in legalActions:
                        v = min(v,
                                miniMax(gameState.generateSuccessor(agentindex,
                                action), depth, agentindex + 1,
                                numghosts, False))
                return v

        legalActions = gameState.getLegalActions()
        numghosts = gameState.getNumAgents() - 1
        bestaction = Directions.STOP
        score = -float('inf')

        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, miniMax(nextState, self.depth, 1,
                        numghosts, False))
            if score > prevscore:
                bestaction = action
 
        return bestaction


        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):

    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alphaBetaminiMax(
            gameState,
            alpha,
            beta,
            depth,
            agentindex,
            numghosts,
            MaxPlayer,
            ):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if MaxPlayer:
                v = -float('inf')
                legalActions = gameState.getLegalActions(0)
                for action in legalActions:
                    v = max(v, alphaBetaminiMax(
                        gameState.generateSuccessor(0, action),
                        alpha,
                        beta,
                        depth,
                        1,
                        numghosts,
                        False,
                        ))
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
                return v
            else:
                v = float('inf')
                legalActions = gameState.getLegalActions(agentindex)
                if agentindex == numghosts:
                    for action in legalActions:
                        v = min(v, alphaBetaminiMax(
                            gameState.generateSuccessor(agentindex,
                                    action),
                            alpha,
                            beta,
                            depth - 1,
                            0,
                            numghosts,
                            True,
                            ))
                        if v <= alpha:
                            return v
                        beta = min(beta, v)
                else:
                    for action in legalActions:
                        v = min(v, alphaBetaminiMax(
                            gameState.generateSuccessor(agentindex,
                                    action),
                            alpha,
                            beta,
                            depth,
                            agentindex + 1,
                            numghosts,
                            False,
                            ))
                        if v <= alpha:
                            return v
                        beta = min(beta, v)
                return v

        legalActions = gameState.getLegalActions()
        numghosts = gameState.getNumAgents() - 1
        bestaction = Directions.STOP
        score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, alphaBetaminiMax(
                nextState,
                alpha,
                beta,
                self.depth,
                1,
                numghosts,
                False,
                ))
            if score > prevscore:
                bestaction = action
            if score >= beta:
                return bestaction
            alpha = max(alpha, score)
                   
        return bestaction
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

        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    util.raiseNotDefined()


# Abbreviation

better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):

    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """

        util.raiseNotDefined()



      