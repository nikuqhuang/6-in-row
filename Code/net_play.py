# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
""" 

from __future__ import print_function
from game import Board, Game
from policy_value_net_pytorch import PolicyValueNet
from mcts_alphaZero import MCTSPlayer
import pickle
from collections import defaultdict
    

def run():
    n = 6
    width, height = 9, 9
    model_file = 'best_policy.model'
    model_file_compare = 'compare.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)      
        
        
        try:
            policy_param = pickle.load(open(model_file, 'rb'))
            policy_param_compare = pickle.load(open(model_file_compare, 'rb'))
        except:
            policy_param = pickle.load(open(model_file, 'rb'), encoding = 'bytes')  
            policy_param_compare = pickle.load(open(model_file_compare, 'rb'), encoding = 'bytes')  # To support python3
        
        #對照組
        best_policy = PolicyValueNet(width, height, policy_param)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=800)  # set larger n_playout for better performance
        
        #實驗組
        compare = PolicyValueNet(width, height, policy_param_compare)
        mcts_player_compare = MCTSPlayer(compare.policy_value_fn, c_puct=5, n_playout=800)  # set larger n_playout for better performance 
        
        #評估勝率
        win_cnt = defaultdict(int)
        for i in range(200): #場數設定
            winner = game.start_play(mcts_player_compare, mcts_player, start_player=i%2, is_shown=1)
            win_cnt[winner] += 1
                
        print("win: {}, lose: {}, tie:{}".format(win_cnt[1], win_cnt[2], win_cnt[-1]))
     
    except KeyboardInterrupt:
        print('\n\rquit')

if __name__ == '__main__':    
    run()
   

