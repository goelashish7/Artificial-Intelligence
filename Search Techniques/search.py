# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from __builtin__ import str

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  from game import Directions
  from util import Stack
  n=Directions.NORTH
  s=Directions.SOUTH
  e=Directions.EAST
  w=Directions.WEST
  explored=[]
  frontier=Stack()
  frontierSet=[]
  start_node=problem.getStartState()
  if problem.isGoalState(start_node)==True:
    return []
  frontier.push((start_node,[]))
  while frontier.isEmpty()==False:
      currentNode=frontier.pop()
      currentState=currentNode[0]
      actions=currentNode[1]
      if(problem.isGoalState(currentState)==True):
          return actions
      explored.extend(currentState)
      successors=problem.getSuccessors(currentState)
      for successor in successors:
          succState=successor[0]
          succAction=successor[1]
          if succState not in explored and succState not in frontierSet:
              frontierSet.append(succState)
              tempPath=list(actions)
              if(succAction=='North'):
                tempPath.append(n)
              elif(succAction=='East'):
                tempPath.append(e)
              elif(succAction=='South'):
                tempPath.append(s)
              elif(succAction=='West'):
                tempPath.append(w)
              frontier.push((succState,tempPath))
  return []            

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import Queue
  n=Directions.NORTH
  s=Directions.SOUTH
  e=Directions.EAST
  w=Directions.WEST
  explored=[]
  frontier=Queue()
  frontierSet=[]
  start_node=problem.getStartState()
  if problem.isGoalState(start_node)==True:
    return []
  frontier.push((start_node,[]))
  while frontier.isEmpty()==False:
      currentNode=frontier.pop()
      currentState=currentNode[0]
      actions=currentNode[1]
      if(problem.isGoalState(currentState)==True):
          #print actions
          return actions
      explored.append(str(currentState))
      successors=problem.getSuccessors(currentState)
      for successor in successors:
          succState=successor[0]
          succAction=successor[1]
          if str(succState) not in explored and str(succState) not in frontierSet:
              frontierSet.append(str(succState))
              tempPath=list(actions)
              if(succAction=='North'):
                tempPath.append(n)
              elif(succAction=='East'):
                tempPath.append(e)
              elif(succAction=='South'):
                tempPath.append(s)
              elif(succAction=='West'):
                tempPath.append(w)
              frontier.push((succState,tempPath))
  return []            
     
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from game import Directions   
  from util import PriorityQueue
  n=Directions.NORTH
  s=Directions.SOUTH
  e=Directions.EAST
  w=Directions.WEST
  explored=[]
  frontier=PriorityQueue()
  frontierSet=[]
  nodePath={}
  gDistance={}
  canBeExpanded={}
  dist=0 # dist = g(n)
  start_node=problem.getStartState()
  gDistance[str(start_node)]=0
  nodePath[str(start_node)]=[]
  canBeExpanded[str(start_node)]=True
  if problem.isGoalState(start_node)==True:
    return []
  frontier.push((start_node),dist)
  while frontier.isEmpty()==False:
      #pop the current node
      currentNode=frontier.pop()
      #Retrieve the current state
      parentState=currentNode # The state to be explored
      parentAction=nodePath[str(parentState)] # Action required to reach to this node.
      parentDistance=gDistance[str(parentState)] # Distance to this node 
      #if(str(parentState) in explored):
       #   continue
      if(str(parentState) in canBeExpanded and canBeExpanded[str(parentState)]==False):
        continue
      canBeExpanded[str(parentState)]=False
      if(problem.isGoalState(parentState)==True):
          return nodePath[str(parentState)]
      explored.append(str(parentState))
      successors=problem.getSuccessors(parentState)
      for successor in successors:
          succState=successor[0]
          succAction=successor[1]
          succCost=successor[2]
          tentativegDistance=parentDistance+succCost
          tempPath=list(parentAction)
          if(succAction=='North'):
            tempPath.append(n)
          elif(succAction=='East'):
            tempPath.append(e)
          elif(succAction=='South'):
            tempPath.append(s)
          elif(succAction=='West'):
            tempPath.append(w)    
       #   if str(succState) in explored:
        #      continue
          dictkey = str(succState)
          #print dictkey

          # dictkey=','.join([succState[0],succState[1]])                
          if dictkey in frontierSet or dictkey in explored:
              oldDistance = gDistance[dictkey]
              if tentativegDistance >= oldDistance:
                  continue
          else:
              frontierSet.append(str(succState))
          canBeExpanded[str(parentState)]=True
          gDistance[dictkey]=tentativegDistance
          nodePath[dictkey]=tempPath
          frontier.push((succState),tentativegDistance)
  return [] 

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  from searchAgents import manhattanHeuristic
  return manhattanHeuristic(state,problem)
  #return 0
def getKey(value,additionalData):
    from game import Grid
    newValue=[]
    costValue=""
    for i in range(len(value)):
        if(isinstance(value[i], Grid)):
             foodgrid=value[i]
             foodList = foodgrid.asList()
             if(not additionalData):
               for i in range(len(foodList)):
                 additionalData.append(foodList[i])
             for i in range(len(additionalData)):
                 foodX=additionalData[i][0]
                 foodY=additionalData[i][1]
                 if  (foodX,foodY) in foodList: 
                    costValue+='1'      
                 else:
                    costValue+='0'
             newValue.append(costValue)
        else:
             newValue.append(value[i])
    return tuple(newValue)      
    
def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions   
  from util import PriorityQueue
  import sys
  n=Directions.NORTH
  s=Directions.SOUTH
  e=Directions.EAST
  w=Directions.WEST
  explored=[]
  frontier=PriorityQueue()
  frontierSet=[]
  nodePath={}
  gDistance={}
  #To check for 
  canBeExpanded={}
  additionalData=[]
  dist=0 # dist = g(n)
  start_node=problem.getStartState()
  startkey=getKey(start_node,additionalData)
  gDistance[str(startkey)]=sys.maxint
  nodePath[str(startkey)]=[]
  canBeExpanded[str(startkey)]=True
  if problem.isGoalState(start_node)==True:
    return []
  frontier.push((start_node),dist)
  while frontier.isEmpty()==False:
      #pop the current node
      currentNode=frontier.pop()
      #Retrieve the current state
      parentState=currentNode # The state to be explored
      parentStateKey=getKey(parentState,additionalData)
    #  print parentStateKey
      parentAction=nodePath.get(str(parentStateKey),"") # Action required to reach to this node.
      parentDistance=gDistance.get(str(parentStateKey),0) # Distance to this node 
      #print parentAction 
      #print parentState[1].__dict__['data']
      #if(parentState[0][0]==6 and parentState[0][1]==6):
       #      print "c";
     # if(str(parentStateKey) in explored):
      #s    continue
      if(str(parentStateKey) in canBeExpanded and canBeExpanded[str(parentStateKey)]==False):
        continue
      canBeExpanded[str(parentStateKey)]=False
      if(problem.isGoalState(parentState)==True):
          return nodePath[str(parentStateKey)]
      explored.append(str(parentStateKey))
      successors=problem.getSuccessors(parentState)
      for successor in successors:
          succState=successor[0]
          succAction=successor[1]
          succCost=successor[2]
          tentativegDistance=parentDistance+succCost
          heuristicdistance=heuristic(succState,problem)
          tempPath=list(parentAction)
          if(succAction=='North'):
            tempPath.append(n)
          elif(succAction=='East'):
            tempPath.append(e)
          elif(succAction=='South'):
            tempPath.append(s)
          elif(succAction=='West'):
            tempPath.append(w)    
          succStateKey=getKey(succState,additionalData)
          #if str(succStateKey) in explored:
          #   continue
          dictkey = str(succStateKey)
          #print dictkey

          # dictkey=','.join([succState[0],succState[1]])                
          if dictkey in frontierSet or dictkey in explored:
              oldDistance = gDistance[dictkey]
              if tentativegDistance > oldDistance:
                  continue
          else:
              frontierSet.append(str(succStateKey))
          gDistance[dictkey]=tentativegDistance
          nodePath[dictkey]=tempPath
          totalDistance=tentativegDistance+heuristicdistance
          canBeExpanded[dictkey]=True
          frontier.push((succState),totalDistance)
  return []

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch