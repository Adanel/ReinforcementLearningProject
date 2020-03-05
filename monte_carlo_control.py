#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:49:15 2020

@author: slimane
"""

import numpy as np
import random
import pickle
from time import time
from ESS import Game

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
    
def hash_action(action):
    return str(action)
       
    
    
def enumerate_states_actions(coordinates):
    '''From one state, enumerate all possible states that can occur'''
    pass

 
        
def policy(Q, state, split_a, split_b, epsilon=0.1, play_random=False, play_optimal=False):
    
    if play_random:
        if np.random.uniform()>0.5:
            return split_a
        else:
            return split_b
        
    if play_optimal:
        weights = 0.5 ** (np.arange(len(split_a)))
        pot_a = np.sum(weights*split_a)
        pot_b = np.sum(weights*split_b)
        if pot_a>=pot_b:
            return split_a
        else:
            return split_b
    
    key_a = hash_action(split_a)
    key_b = hash_action(split_b)
    bigger = split_a
    smaller = split_b
    if np.random.uniform()>0.5:
        bigger = split_b
        smaller = split_a
    
    if state in Q.keys():
        if key_a in Q[state].keys():
            if key_b in Q[state].keys():
                if Q[state][key_a] >= Q[state][key_b]:
                    bigger = split_a
                    smaller = split_b
                else:
                    bigger = split_b
                    smaller = split_a
            else:
                bigger = split_a
                smaller = split_b
        else:
            if key_b in Q[state].keys():
                bigger = split_a
                smaller = split_b
                
                
    if np.random.uniform()>epsilon:
        return bigger
    else:
        return smaller
    
    


game = Game(4, 6)


V = {}
Q = {}
returns = {}
#policy = {}

gamma = 0.9

N = 10000


for i in range(N):
    
    if i%1000==0:
        print(i)
    list_of_states = []
    list_of_actions = []
    list_of_rewards = []
    list_of_returns = []
    winner = None
    game.reset()
    
    #play the game
    while winner != 'attacker' and winner != 'defender':
        a,b = game.play_attacker()
        action = policy(Q, game.getHash(), a, b)
        assert (action==a).all() or (action==b).all()
        list_of_states.append(game.getHash())
        list_of_actions.append(hash_action(action))
        game.play_defender(action)
        winner = game.winner()
        if winner =='attacker':
            list_of_rewards.append(-1)
        elif winner=='defender':
            list_of_rewards.append(1)
        else:
            list_of_rewards.append(0)
    
    assert len(list_of_states) == len(list_of_rewards)
    #compute the returns
    n = len(list_of_states)      
    list_of_returns.append(0)
    for j in range(1,n+1):
        list_of_returns.append(list_of_rewards[n-j] + gamma * list_of_returns[j-1])
    list_of_returns.reverse()
    
    assert len(list_of_states) == len(list_of_returns)-1
    assert list_of_returns[-1]==0
    #add returns to dictionnary
    for i,s in enumerate(list_of_states):
        a = list_of_actions[i]
        if s in returns.keys():
            if a in returns[s].keys():
                returns[s][a].append(list_of_returns[i])
            else:
                returns[s][a] = [list_of_returns[i]]
        else:
            returns[s] = {}
            returns[s][a] = [list_of_returns[i]]
            
for s in returns.keys():
    Q[s] = dict()
    for a in returns[s].keys():
        Q[s][a] = np.mean(returns[s][a])
        

## Check winning after training
        
def evaluate_policy(N=1000, random=False, optimal=False):
    pass
        
N = 1000
winner_defender_random = np.zeros(N)
winner_defender_policy = np.zeros(N)
winner_defender_optimal = np.zeros(N)


for i in range(N):
    game.reset()
    winner=None
    while winner != 'attacker' and winner != 'defender':
        a,b = game.play_attacker()
        action = policy(Q, game.getHash(), a, b, play_random=True)
        assert (action==a).all() or (action==b).all()
        game.play_defender(action)

        winner = game.winner()
        if winner=='defender':
            winner_defender_random[i] = 1
            
            
for i in range(N):
    game.reset()
    winner=None
    while winner != 'attacker' and winner != 'defender':
        a,b = game.play_attacker()
        action = policy(Q, game.getHash(), a, b)
        assert (action==a).all() or (action==b).all()
        game.play_defender(action)

        winner = game.winner()
        if winner=='defender':
            winner_defender_policy[i] = 1
            
            
for i in range(N):
    game.reset()
    winner=None
    while winner != 'attacker' and winner != 'defender':
        a,b = game.play_attacker()
        action = policy(Q, game.getHash(), a, b, play_optimal=True)
        assert (action==a).all() or (action==b).all()
        game.play_defender(action)

        winner = game.winner()
        if winner=='defender':
            winner_defender_optimal[i] = 1


print("In random case, defender wins ", np.sum(winner_defender_random)/10, "% times")  
print("After training, defender wins ", np.sum(winner_defender_policy)/10, "% times")
print("In optimal case, defender wins ", np.sum(winner_defender_optimal)/10, "% times")

            


