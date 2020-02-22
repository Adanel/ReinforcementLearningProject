import numpy as np
import random
import pickle

class State:
    
    def __init__(self, attacker, defender, levels, nb_pieces):
        
        self.levels = levels
        self.nb_pieces = nb_pieces
        self.width = 5
        self.board = np.zeros((self.levels, self.width))
        
        self.coordinates = [(random.randrange(1, self.levels), random.randrange(0, self.width)) for i in range(self.nb_pieces)]
        
        for y, x in (self.coordinates):
            self.board[y, x] = 1 #assign coordinates to board
            
        self.attacker = attacker
        self.defender = defender
        self.isEnd = False
        self.boardHash = None
        
        idxs = range(self.levels + 1)
        self.weights = np.power(2.0, [-(self.levels - i) for i in idxs])
        
    def getHash(self): #we want to keep track of every board state we encountered
        
        self.boardHash = str(self.board.reshape(self.levels * self.width))
        return self.boardHash
    
    def winner(self):
        
        if sum(self.board[0]) >= 1: #if one or several pieces reaches the top
            self.isEnd = True
            return 'attacker'
        
        elif np.count_nonzero(self.board) <= 1: #if there is no more pieces on the board or one piece
            self.isEnd = True
            return 'defender'
        
        else:
            self.isEnd = False #not finished yet     
            return None
    
    def potential_fn(self, state):
        return np.sum(state*self.weights)

    
    def updateGameState(self, split_chosen):
        
        '''
        The defenser has two sets of points proposed, he chooses one to destroy and the other is kept, then the board is updated : every remaining point goes up

        '''
        
        for y_, x_ in (split_chosen):
            self.board[y_, x_] = 0
                    
        self.board = np.roll(self.board, -self.width)
        
        self.coordinates = np.argwhere(self.board).tolist()
            
    def reset(self): # board reset
        
        self.board = np.zeros((self.levels, self.width))
        self.coordinates = [(random.randrange(1, self.levels), random.randrange(0, self.width)) for i in range(self.nb_pieces)]
      
        for y, x in (self.coordinates):
            self.board[y, x] = 1 #assign coordinates to board
            
        self.boardHash = None
        self.isEnd = False
        
    def play(self, rounds=100):
        
        '''
        list of actions by both the attacker and the defender
        
        '''
        
        attacker_reward = 0
        defenser_reward = 0
        
        while not self.isEnd:
            # Attacker
            left_split, right_split = self.attacker.chooseAttackerAction()

            # Defender
            split_chosen = self.defender.chooseDefenderAction(left_split, right_split)
            self.updateGameState(split_chosen)
            
            #board_hash = self.getHash()
            #self.defender.addState(board_hash)

            win = self.winner()
            if win is not None:

                # ended with attacker win or not
                
                if win == 'attacker':               
                    attacker_reward += 1
                    defenser_reward -= 1
                    
                else:
                    attacker_reward -= 1
                    defenser_reward += 1
                    
                #self.attacker.reset()
                #self.defender.reset()
                #self.reset()
                
                break   
        
class Player:
    
    def __init__(self, name, exp_rate=0.3):
        
        self.name = name
        self.states = []  # record all splits (for defender)
        self.game_states = [] #record state of board (for attacker)
        self.lr = 0.2
        self.exp_rate = exp_rate #30% time our agent will take a random action        
        self.decay_gamma = 0.9
        self.states_value = {}
        self.game_states_value={}
        
    def getHash(self, board):
        
        boardHash = str(board.reshape(self.levels * self.width))
        return boardHash
    
    def addState(self, left_split, righ_split):
        
        self.states.append(np.concatenate([left_split, right_split]))
            
    def reset(self):
        self.states = []
        
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file,'rb')
        self.states_value = pickle.load(fr)
        fr.close()
    
    def chooseAttackerAction(self):
    
        '''
        random attacker for now
        '''
        m = np.random.randint(low = 1, high = len(self.coordinates))
        
        coo_left = random.choices(self.coordinates, k=m)
        coo_right = [x for x in self.coordinates if x not in coo_left]
            
        return coo_left, coo_right
    
    def chooseDefenderAction(self, left_split, right_split):
    
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action - exploration
            
            k = np.random.randint(low = 0, high = 2)
            
            chosen_split = left_split if k == 0 else right_split
            
        else:        
            # compute potential for each split to evaluate the most dangerous one
            
            pot_left, pot_right = potential_fn(left_split), potential_fn(right_split)
            
            chosen_split = left_split if pot_left > pot_right else right_split #the chosen split is the split to destroy
            
        return chosen_split

            
