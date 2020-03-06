#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:52:54 2020

@author: slimane
"""
import numpy as np
import random
import pickle
from time import time
from ESS import Game, Player

def enumerate_parts(l):
    '''Enumerate all parts of a list'''
    if len(l)==0:
        return []
    if len(l)==1:
        return([[], [l[0]]])
    else:
        l2 = enumerate_parts(l[1::])
        l3 = []
        for element in l2:
            l3.append(element+[l[0]])
            l3.append(element)
        return l3
    
    
def enumerate_states_actions(coordinates):
    '''From one state, enumerate all possible states that can occur'''
    pass

      
        
def policy(state, split_a, split_b):
    
    if np.random.uniform()>0.5:
        return split_a
    else:
        return split_b
    

attacker = Player("A")
defender = Player("D")
game = Game(attacker, defender, 7, 8)

baseline = game.coordinates
N = 10000

V = {}
returns = {}
list_of_states = []
list_of_rewards = []
gamma = 0.9


for i in range(N):
    list_of_states = []
    list_of_rewards = []
    list_of_returns = []
    winner = None
    game.reset()
    
    #play the game
    while winner != 'attacker' and winner != 'defender':
        a,b = game.play_attacker()
        game.play_defender(policy(game.coordinates, a, b))
        list_of_states.append(game.getHash())
        winner = game.winner()
        print(winner)
        if winner =='attacker':
            list_of_rewards.append(-1)
        elif winner=='defender':
            list_of_rewards.append(1)
        else:
            list_of_rewards.append(0)
    
    #compute the returns
    n = len(list_of_states)      
    list_of_returns.append(0)
    for j in range(1,n):
        list_of_returns.append(list_of_rewards[n-j] + gamma * list_of_returns[j-1])
    list_of_returns.reverse()
    
    #add returns to dictionnary
    for i,s in enumerate(list_of_states):
        if s in returns.keys():
            returns[s].append(list_of_returns[i])
        else:
            returns[s] = [list_of_returns[i]]
            
for s in returns.keys():
    V[s] = np.mean(returns[s])

         
