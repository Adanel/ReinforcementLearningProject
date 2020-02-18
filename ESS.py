import numpy as np
import random
import pickle

'''
TODO

- function that update the board accoring to each player turn
- player class that compute best action
- implement action choice in the game

'''

class State:
    
    def __init__(self, attacker, defender, levels, nb_pieces):
        
        self.levels = levels
        self.nb_pieces = nb_pieces
        self.width = 5
        self.board = np.zeros((self.levels, self.width))
        
        self.coordinates = [(random.randrange(0, self.levels), random.randrange(0, self.width)) for i in range(self.nb_pieces)]
        
        for y, x in (self.coordinates):
            self.board[y, x] = 1 #assign coordinates to board
            
        self.attacker = attacker
        self.defender = defender
        self.isEnd = False
        self.boardHash = None
        
        self.turn_of = 'attacker' # init attacker plays first
        
    def getHash(self): #we want to keep track of every board state we encountered
        
        self.boardHash = str(self.board.reshape(self.levels * self.width))
        return self.boardHash
    
    def winner(self):
        
        if sum(self.board[0]) > 1: #if one or several pieces reaches the top
            self.isEnd = True
            return -1
        
        elif np.count_nonzero(self.board) == 0: #if there is no more pieces on the board
            self.isEnd = True
            return 1
        
        else:
            self.isEnd = False #not finished yet
            
        return None
        
    def updateStateAttack(self, sets_of_points):
        
        '''  
        Is it necessary ? Attacker doesn't actually changes the board
        
        '''
        return None
        
    def updateStateDefense(self, split_chosen):
        
        '''
        The defenser has two sets of points proposed, he chooses one to destroy and the other is kept, then the board is updated : every remaining point goes up

        '''
        
        for y_, x_ in (split_chosen):
            self.board[y_, x_] = 0
                    
        self.board = np.roll(self.board, -self.width)
        
    def giveReward(self):
        
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.attacker.feedReward(0)
            self.defender.feedReward(1)
        else:
            self.attacker.feedReward(1)
            self.defender.feedReward(0)
            
    def reset(self): # board reset
        
        self.board = np.zeros((self.levels, self.width))
        self.coordinates = [(random.randrange(0, self.levels), random.randrange(0, self.width)) for i in range(self.nb_pieces)]
      
        for y, x in (self.coordinates):
            self.board[y, x] = 1 #assign coordinates to board
            
        self.boardHash = None
        self.isEnd = False
        
    def play(self, rounds=100):
        
        '''
        list of actions by both the attacker and the defender
        
        '''
        return None
        
        
class Player:
    
    def __init__(self, name, exp_rate=0.3):
        
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value
        
    def getHash(self, board):
        
        boardHash = str(board.reshape(self.levels * self.width))
        return boardHash
    
    def addState(self, state):
        
        self.states.append(state)
        
    def feedReward(self, reward):
        
        for st in reversed(self.states):
            
            if self.states_value.get(st) is None:
                
                self.states_value[st] = 0
           
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
    
    def chooseAction()
    
    '''
    choose action based on current estimation of the states
    
    '''
        return None
            
