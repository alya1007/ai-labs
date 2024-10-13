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
import random
import util
import sys

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()      # Pacman position after moving
        newFood = successorGameState.getFood()               # Remaining food
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        listFood = newFood.asList()                        # All remaining food as list
        ghostPos = successorGameState.getGhostPositions()  # Get the ghost position
        # Initialize with list
        mFoodDist = []
        mGhostDist = []

        # Find the distance of all the foods to the pacman
        for food in listFood:
            mFoodDist.append(manhattanDistance(food, newPos))

        # Find the distance of all the ghost to the pacman
        for ghost in ghostPos:
            mGhostDist.append(manhattanDistance(ghost, newPos))

        if currentGameState.getPacmanPosition() == newPos:
            return (-(float("inf")))

        for ghostDistance in mGhostDist:
            if ghostDistance < 2:
                return (-(float("inf")))

        if len(mFoodDist) == 0:
            return float("inf")
        else:
            minFoodDist = min(mFoodDist)
            maxFoodDist = max(mFoodDist)

        return 1000/sum(mFoodDist) + 10000/len(mFoodDist)


def minDistances(currentGameState):
    """
        This function initializes the positions of
        pacman, pallets and ghost states.

        It then creates a list of distances to the nearest
        pallets and the nearest distance becomes the
        value of food score.

        It also creates a list of distances to the
        nearest active ghosts and the nearest distance
        becomes the value of ghost danger.
    """
    pacmanPos = currentGameState.getPacmanPosition()
    ghostList = currentGameState.getGhostStates()
    foods = currentGameState.getFood()

    # Distance to nearest food
    foodDistList = [util.manhattanDistance(
        each, pacmanPos) for each in foods.asList()]
    if foodDistList:
        palletScore = min(foodDistList)
    else:
        palletScore = 0

    # List of distances to nearest active ghosts
    ghostDistList = [util.manhattanDistance(
        pacmanPos, each.getPosition()) for each in ghostList if each.scaredTimer == 0]

    if ghostDistList:
        # Nearest ghost distance
        ghostDanger = min(ghostDistList)
    else:
        # No active ghosts so the distance is infinite
        ghostDanger = float("inf")

    return palletScore, ghostDanger


def scoreEvaluationFunction(currentGameState):
    """
        The score is then calculated by subtracting
        ghost danger from food score.
    """

    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    palletScore, ghostDanger = minDistances(currentGameState)
    score = palletScore - ghostDanger

    return score


def advancedScoreEvaluationFunction(currentGameState):
    """
        Adjustments:
        - Encourage moving closer to food
        - Penalize getting closer to ghosts
        - Encourage eating all food
        - Encourage eating power pellets
    """
    foods = currentGameState.getFood()
    capsules = currentGameState.getCapsules()

    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    palletScore, ghostDanger = minDistances(currentGameState)
    # Evaluate score
    score = currentGameState.getScore()

    # Adjust score based on food distance and ghost danger
    score += 10 / (palletScore + 1)  # Encourage moving closer to food
    if ghostDanger != float("inf"):  # Only adjust for ghosts if they are near
        score -= 10 / (ghostDanger + 1)  # Penalize getting closer to ghosts

    # Reward for fewer remaining food pellets and capsules
    score += 100 / (len(foods.asList()) + 1)  # Encourage eating all food
    score += 100 / (len(capsules) + 1)  # Encourage eating power pellets

    return score


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

    def getAction(self, gameState):

        def minimax(gameState, depth, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                maxEval = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    eval = minimax(gameState.generateSuccessor(
                        agentIndex, action), depth - 1, agentIndex + 1)
                    maxEval = max(maxEval, eval)
                return maxEval
            else:
                minEval = float("inf")
                for action in gameState.getLegalActions(agentIndex):
                    # If last ghost then next agent is pacman
                    if agentIndex == gameState.getNumAgents() - 1:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth - 1, 0)
                    # Else next agent is ghost
                    else:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth, agentIndex + 1)
                    minEval = min(minEval, eval)
                return minEval

        bestAction = Directions.STOP

        v = float("-inf")

        for action in gameState.getLegalActions(0):
            temp = minimax(gameState.generateSuccessor(
                0, action), self.depth, 1)
            if temp > v:
                v = temp
                bestAction = action

        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        def minimax(gameState, depth, alpha, beta, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                maxEval = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    eval = minimax(gameState.generateSuccessor(
                        agentIndex, action), depth - 1, alpha, beta, agentIndex + 1)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return maxEval
            else:
                minEval = float("inf")
                for action in gameState.getLegalActions(agentIndex):
                    # If last ghost then next agent is pacman
                    if agentIndex == gameState.getNumAgents() - 1:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth - 1, alpha, beta, 0)
                    # Else next agent is ghost
                    else:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth, alpha, beta, agentIndex + 1)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return minEval

        bestAction = Directions.STOP

        v = float("-inf")

        for action in gameState.getLegalActions(0):
            temp = minimax(gameState.generateSuccessor(
                0, action), self.depth, float("-inf"), float("inf"), 1)
            if temp > v:
                v = temp
                bestAction = action

        return bestAction


class MinimaxImprovedAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):

        def minimax(gameState, depth, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                maxEval = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    eval = minimax(gameState.generateSuccessor(
                        agentIndex, action), depth - 1, agentIndex + 1)
                    maxEval = max(maxEval, eval)
                return maxEval
            else:
                minEval = float("inf")
                for action in gameState.getLegalActions(agentIndex):
                    # If last ghost then next agent is pacman
                    if agentIndex == gameState.getNumAgents() - 1:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth - 1, 0)
                    # Else next agent is ghost
                    else:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth, agentIndex + 1)
                    minEval = min(minEval, eval)
                return minEval

        bestAction = Directions.STOP

        v = float("-inf")

        for d in range(1, self.depth + 1):
            for action in gameState.getLegalActions(0):
                temp = minimax(gameState.generateSuccessor(
                    0, action), d, 1)
                if temp > v:
                    v = temp
                    bestAction = action

        return bestAction


def aStarSearch(gameState, pacmanPos, targetFood):
    frontier = util.PriorityQueue()
    startState = (pacmanPos, [])
    frontier.push(startState, 0)

    explored = set()

    while not frontier.isEmpty():
        (currentPos, actions) = frontier.pop()

        if currentPos == targetFood:
            return actions

        if currentPos not in explored:
            explored.add(currentPos)
            for action in gameState.getLegalActions(0):
                successor = gameState.generatePacmanSuccessor(
                    action)
                successorPos = successor.getPacmanPosition()
                newActions = actions + [action]
                # cost is the sum of the number of actions and the manhattan distance to the target food
                cost = len(newActions) + \
                    manhattanDistance(successorPos, targetFood)
                frontier.push((successorPos, newActions), cost)

    return []


class AStarMinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):

        def aStarHeuristic(successorGameState, targetFood):
            # Get Pacman's current position after the move
            pacmanPos = successorGameState.getPacmanPosition()
            return len(aStarSearch(successorGameState, pacmanPos, targetFood))

        def minimax(gameState, depth, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                maxEval = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    # Find closest food using A*
                    foodList = successor.getFood().asList()
                    if foodList:
                        minFoodDist = min(
                            [aStarHeuristic(successor, food) for food in foodList])
                    else:
                        minFoodDist = 0
                    # This encourages Pacman to move towards food
                    # as it lowers the evaluation score the farther
                    # away Pacman is from the food.
                    eval = minimax(successor, depth - 1,
                                   agentIndex + 1) - minFoodDist
                    maxEval = max(maxEval, eval)
                return maxEval
            else:
                minEval = float("inf")
                for action in gameState.getLegalActions(agentIndex):
                    if agentIndex == gameState.getNumAgents() - 1:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth - 1, 0)
                    else:
                        eval = minimax(gameState.generateSuccessor(
                            agentIndex, action), depth, agentIndex + 1)
                    minEval = min(minEval, eval)
                return minEval

        bestAction = Directions.STOP
        v = float("-inf")

        for action in gameState.getLegalActions(0):
            temp = minimax(gameState.generateSuccessor(
                0, action), self.depth, 1)
            if temp > v:
                v = temp
                bestAction = action

        return bestAction


class AStarAlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):

        def aStarHeuristic(successorGameState, targetFood):
            pacmanPos = successorGameState.getPacmanPosition()
            return len(aStarSearch(successorGameState, pacmanPos, targetFood))

        def alphaBeta(gameState, depth, alpha, beta, agentIndex):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agentIndex == 0:
                maxEval = float("-inf")
                for action in gameState.getLegalActions(agentIndex):
                    successor = gameState.generateSuccessor(agentIndex, action)
                    foodList = successor.getFood().asList()
                    if foodList:
                        minFoodDist = min(
                            [aStarHeuristic(successor, food) for food in foodList])
                    else:
                        minFoodDist = 0
                    eval = alphaBeta(successor, depth - 1, alpha,
                                     beta, agentIndex + 1) - minFoodDist
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return maxEval
            else:
                minEval = float("inf")
                for action in gameState.getLegalActions(agentIndex):
                    if agentIndex == gameState.getNumAgents() - 1:
                        eval = alphaBeta(gameState.generateSuccessor(
                            agentIndex, action), depth - 1, alpha, beta, 0)
                    else:
                        eval = alphaBeta(gameState.generateSuccessor(
                            agentIndex, action), depth, alpha, beta, agentIndex + 1)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return minEval

        bestAction = Directions.STOP
        v = float("-inf")

        for action in gameState.getLegalActions(0):
            temp = alphaBeta(gameState.generateSuccessor(
                0, action), self.depth, float("-inf"), float("inf"), 1)
            if temp > v:
                v = temp
                bestAction = action

        return bestAction
