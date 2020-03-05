import numpy as np
import random
import pickle
from time import time

class Game:
    
    def __init__(self, levels, nb_pieces, init_bottom=False):
        
        self.levels = levels
        self.nb_pieces = nb_pieces
        
        self.locations = np.zeros(self.levels)
        if init_bottom:
            self.locations[self.levels-1] = self.nb_pieces
        else:
            self.locations[1::] = np.random.multinomial(nb_pieces, np.ones(levels-1)/(levels-1))
        
        assert self.locations[0]==0
        assert np.sum(self.locations) == self.nb_pieces
             
        self.isEnd = False
        self.boardHash = None
        
        #self.state = [random.randrange(1, self.levels) for i in range(self.nb_pieces)]
        
    def getHash(self): #we want to keep track of every board state we encountered
        
        self.boardHash = str(self.locations)
        return self.boardHash
    
    def set_locations(locations):
        self.locations = locations
        
    
    def winner(self):
        
        if self.locations[0] >= 1: #if one or several pieces reaches the top
            self.isEnd = True
            return 'attacker'
        
        elif np.sum(self.locations) <= 1: #if there is no more pieces on the board or one piece
            self.isEnd = True
            return 'defender'
        
        else:
            self.isEnd = False #not finished yet     
            return None
    
    

    
    def play_defender(self, split_chosen):
        
        '''
        The defenser has two sets of points proposed, he chooses one to destroy and the other is kept, then the board is updated : every remaining point goes up

        '''
        
        self.locations = np.roll(self.locations - split_chosen,-1)
        
        
            
    def reset(self, init_bottom=False): # board reset
        
        self.locations = np.zeros(self.levels)
        if init_bottom:
            self.locations[self.levels-1] = self.nb_pieces
        else:
            self.locations[1::] = np.random.multinomial(self.nb_pieces, np.ones(self.levels-1)/(self.levels-1))
        
        assert np.sum(self.locations) == self.nb_pieces
        assert self.locations[0]==0
        
        self.isEnd = False
        
        
    def play_attacker(self):
        
        loc_a = np.zeros(self.levels)
        while np.sum(loc_a)==0 or np.sum(loc_a)>=np.sum(self.locations):
            for i in range(self.levels):
                loc_a[i] = np.random.randint(self.locations[i]+1)
                
        loc_b = self.locations - loc_a
            
        assert (loc_a+loc_b == self.locations).all()
        assert (loc_a>=0).all()
        assert (loc_b>=0).all()
        assert np.sum(loc_a)>0 and np.sum(loc_a)<=np.sum(self.locations)
        assert np.sum(loc_b)>0 and np.sum(loc_b)<=np.sum(self.locations)
            
        return loc_a, loc_b
        
                
