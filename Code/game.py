# -*- coding: utf-8 -*-
"""
@author: Junxiao Song
""" 

from __future__ import print_function
import numpy as np

class Board(object):
    """
    board for the game
    """

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 9))
        self.height = int(kwargs.get('height', 9))
        self.states = {} # board states, key:move as location on the board, value:player as pieces type
        self.n_in_row = int(kwargs.get('n_in_row', 6)) # need how many pieces in a row to win
        self.players = [1, 2] # player1 and player2
        self.hand = 0
 
        
        
    def init_board(self, start_player=0):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not less than %d' % self.n_in_row)
        self.current_player = self.players[start_player]  # start player        
        self.availables = list(range(self.width * self.height)) # available moves 
        self.states = {} # board states, key:move as location on the board, value:player as pieces type
        self.last_move = -1

    def move_to_location(self, move):
        """       
        3*3 board's moves like:
        0 1 2
        3 4 5
        6 7 8
        and move 5's location is (1,2)
        """
        h = move  // self.width
        w = move  %  self.width
        return [h, w]

    def location_to_move(self, location):
        if(len(location) != 2):
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if(move not in range(self.width * self.height)):
            return -1
        return move

    def current_state(self): 
        """return the board state from the perspective of the current player
        shape: 4*width*height"""
        
        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]                           
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0   
            square_state[2][self.last_move //self.width, self.last_move % self.height] = 1.0 # last move indication
        # denote turn
        if (len(self.states) - 1)%4 == 1 or (len(self.states) - 1)%4 == 2:
            square_state[3][:, :] = 1.0
        return square_state[:,::-1,:]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
            
        self.hand += 1
        if self.hand == 1:
            self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        elif (self.hand - 1) % 2 == 0:
            self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        
        self.last_move = move
        
#落一子必勝走步        
    def is_sure_win1(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row
        self.a = 0
        moved = list(set(range(width * height)) - set(self.availables))
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            if self.current_player == player and (self.hand - 1)%2 == 0:#我方第一步
                #活五橫
                if (w in range(width - n + 2) and
                    len(set(states.get(i, -1) for i in range(m, m + n - 1))) == 1):
                    
                    if (m - 1) in self.availables and  w > 0:
                        self.a = m - 1
                        return True, self.a
                    elif (m + n - 1) in self.availables and  w < width - n + 1:
                        self.a = m + n - 1
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 1) in self.availables:
                        self.a = m + 1
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 2) in self.availables:
                        self.a = m + 2
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 3) in self.availables:
                        self.a = m + 3
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 4) in self.availables:
                        self.a = m + 4
                        return True, self.a
                     
                #活五直
                if (h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * width, width))) == 1):
                    if (m - width) in self.availables:
                        self.a = m - width
                        return True, self.a
                    elif (m + (n - 1) * width) in self.availables:
                        self.a = m + (n - 1) * width
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*height, -1) == 1 and
                      states.get(m + 3*height, -1) == 1 and
                      states.get(m + 4*height, -1) == 1 and
                      states.get(m + 5*height, -1) == 1):
                    if (m + height) in self.availables:
                        self.a = m + height
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + height, -1) == 1 and
                      states.get(m + 3*height, -1) == 1 and
                      states.get(m + 4*height, -1) == 1 and
                      states.get(m + 5*height, -1) == 1):
                    if (m + 2*height) in self.availables:
                        self.a = m + 2*height
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + height, -1) == 1 and
                      states.get(m + 2*height, -1) == 1 and
                      states.get(m + 4*height, -1) == 1 and
                      states.get(m + 5*height, -1) == 1):
                    if (m + 3*height) in self.availables:
                        self.a = m + 3*height
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + height, -1) == 1 and
                      states.get(m + 2*height, -1) == 1 and
                      states.get(m + 3*height, -1) == 1 and
                      states.get(m + 5*height, -1) == 1):
                    if (m + 4*height) in self.availables:
                        self.a = m + 4*height
                        return True, self.a
                    
                #活五正斜率
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width + 1), width + 1))) == 1):
                    if (m - width - 1) in self.availables and w > 0:
                        self.a = m - width - 1
                        return True, self.a
                    elif (m + (n - 1) * (width + 1)) in self.availables and w < (width - n + 1):
                        self.a = m + (n - 1) * (width + 1)
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables:
                        self.a = m + width + 1
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 2*(width + 1)) in self.availables:
                        self.a = m + 2*(width + 1)
                        return True, self.a    
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 3*(width + 1)) in self.availables:
                        self.a = m + 3*(width + 1)
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 4*(width + 1)) in self.availables:
                        self.a = m + 4*(width + 1)
                        return True, self.a
                
                #活五負斜率
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width - 1), width - 1))) == 1):
                    if (m - width + 1) in self.availables and w < width - 1:
                        self.a = m - width + 1
                        return True, self.a
                    elif (m + (n - 1) * (width - 1)) in self.availables and w > n - 2:
                        self.a = m + (n - 1) * (width - 1)
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables:
                        self.a = m + width - 1
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 2*(width - 1)) in self.availables:
                        self.a = m + 2*(width - 1)
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 3*(width - 1)) in self.availables:
                        self.a = m + 3*(width - 1)
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 4*(width - 1)) in self.availables:
                        self.a = m + 4*(width - 1)
                        return True, self.a
    
#落二子必勝走步      
    def is_sure_win2(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row
        self.a = 0
        self.b = 0
        moved = list(set(range(width * height)) - set(self.availables))
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            if self.current_player == player and (self.hand - 1)%2 == 0:
                #活四死四橫
                if (w in range(width - n + 3) and
                    len(set(states.get(i, -1) for i in range(m, m + n - 2))) == 1):
                    if (m - 1) in self.availables and (m + n - 2) in self.availables and  w > 0 and w < width - n + 2:
                        self.a = m - 1
                        self.b = m + n - 2
                        return True, self.a, self.b
                    elif (m + n - 2) in self.availables and (m + n - 1) in self.availables and w < width - n + 1:
                        self.a = m + n - 2
                        self.b = m + n - 1
                        return True, self.a, self.b
                    elif (m - 1) in self.availables and (m - 2) in self.availables and w > 1:   
                        self.a = m - 1
                        self.b = m - 2
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m + 1) in self.availables and (m + 5) in self.availables:
                        self.a = m + 1
                        self.b = m + 5
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 1) in self.availables and (m + 4) in self.availables:
                        self.a = m + 1
                        self.b = m + 4
                        return True, self.a, self.b
                
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 1) in self.availables and (m + 3) in self.availables:
                        self.a = m + 1
                        self.b = m + 3
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 1) in self.availables and (m + 2) in self.availables:
                        self.a = m + 1
                        self.b = m + 2
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m + 2) in self.availables and (m + 5) in self.availables:
                        self.a = m + 2
                        self.b = m + 5
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 2) in self.availables and (m + 4) in self.availables:
                        self.a = m + 2
                        self.b = m + 4
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 2) in self.availables and (m + 3) in self.availables:
                        self.a = m + 2
                        self.b = m + 3
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m + 3) in self.availables and (m + 5) in self.availables:
                        self.a = m + 3
                        self.b = m + 5
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 3) in self.availables and (m + 4) in self.availables:
                        self.a = m + 3
                        self.b = m + 4
                        return True, self.a, self.b
                    
                if (w > 0 and w in range(width - n + 2) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m - 1) in self.availables and (m + 1) in self.availables:
                        self.a = m - 1
                        self.b = m + 1
                        return True, self.a, self.b
                    
                if (w > 0 and w in range(width - n + 2) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m - 1) in self.availables and (m + 2) in self.availables:
                        self.a = m - 1
                        self.b = m + 2
                        return True, self.a, self.b
                    
                if (w > 0 and w in range(width - n + 2) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 4, -1) == 1):
                    if (m - 1) in self.availables and (m + 3) in self.availables:
                        self.a = m - 1
                        self.b = m + 3
                        return True, self.a, self.b
                    
                    
                
                    
                #活四直
                if (h in range(height - n + 3) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 2) * width, width))) == 1):
                    if (m - width) in self.availables and (m + (n - 2) * width) in self.availables:
                        self.a = m - width
                        self.b = m + (n - 2) * width
                        return True, self.a, self.b
                    elif (m + (n - 1) * width) in self.availables and (m + (n - 2) * width) in self.availables:
                        self.a = m + (n - 1) * width
                        self.b = m + (n - 2) * width
                        return True, self.a, self.b
                    elif (m - width) in self.availables and (m - 2 * width) in self.availables:
                        self.a = m - width
                        self.b = m - 2 * width
                        return True, self.a, self.b
                 
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m + width) in self.availables and (m + 5*width) in self.availables:
                        self.a = m + width
                        self.b = m + 5*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + width) in self.availables and (m + 4*width) in self.availables:
                        self.a = m + width
                        self.b = m + 4*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + width) in self.availables and (m + 3*width) in self.availables:
                        self.a = m + width
                        self.b = m + 3*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + width) in self.availables and (m + 2*width) in self.availables:
                        self.a = m + width
                        self.b = m + 2*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m + 2*width) in self.availables and (m + 5*width) in self.availables:
                        self.a = m + 2*width
                        self.b = m + 5*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 2*width) in self.availables and (m + 4*width) in self.availables:
                        self.a = m + 2*width
                        self.b = m + 4*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 2*width) in self.availables and (m + 3*width) in self.availables:
                        self.a = m + 2*width
                        self.b = m + 3*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m + 3*width) in self.availables and (m + 5*width) in self.availables:
                        self.a = m + 3*width
                        self.b = m + 5*width
                        return True, self.a, self.b
                
                if (h in range(height - n + 1) and    
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 3*width) in self.availables and (m + 4*width) in self.availables:
                        self.a = m + 3*width
                        self.b = m + 4*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 2) and
                      h > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m - width) in self.availables and (m + width) in self.availables:
                        self.a = m - width
                        self.b = m + width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 2) and
                      h > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m - width) in self.availables and (m + 2*width) in self.availables:
                        self.a = m - width
                        self.b = m + 2*width
                        return True, self.a, self.b
                    
                if (h in range(height - n + 2) and
                      h > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1):
                    if (m - width) in self.availables and (m + 3*width) in self.availables:
                        self.a = m - width
                        self.b = m + 3*width
                        return True, self.a, self.b
                    
                #活四正斜率
                if (w in range(width - n + 3) and h in range(height - n + 3) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 2) * (width + 1), width + 1))) == 1):
                    if (m - width - 1) in self.availables and (m + (n - 2) * (width + 1)) in self.availables and  w > 0 and w < (width - n + 2):
                        self.a = m - width - 1
                        self.b = m + (n - 2) * (width + 1)
                        return True, self.a, self.b
                    elif (m - width - 1) in self.availables and (m - 2*(width + 1)) in self.availables and w > 1:
                        self.a = m - width - 1
                        self.b = m - 2*(width + 1)
                        return True, self.a, self.b
                    elif (m + (n - 2) * (width + 1)) in self.availables and (m + (n - 1) * (width + 1)) in self.availables and w < width - n + 1:
                        self.a = m + (n - 2) * (width + 1)
                        self.b = m + (n - 1) * (width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables and (m + 5*(width + 1)) in self.availables:
                        self.a = m + width + 1
                        self.b = m + 5*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables and (m + 4*(width + 1)) in self.availables:
                        self.a = m + width + 1
                        self.b = m + 4*(width + 1)
                        return True, self.a, self.b  
                
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables and (m + 3*(width + 1)) in self.availables:
                        self.a = m + width + 1
                        self.b = m + 3*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables and (m + 2*(width + 1)) in self.availables:
                        self.a = m + width + 1
                        self.b = m + 2*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m + 2*(width + 1)) in self.availables and (m + 5*(width + 1)) in self.availables:
                        self.a = m + 2*(width + 1)
                        self.b = m + 5*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 2*(width + 1)) in self.availables and (m + 4*(width + 1)) in self.availables:
                        self.a = m + 2*(width + 1)
                        self.b = m + 4*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 2*(width + 1)) in self.availables and (m + 3*(width + 1)) in self.availables:
                        self.a = m + 2*(width + 1)
                        self.b = m + 3*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m + 3*(width + 1)) in self.availables and (m + 5*(width + 1)) in self.availables:
                        self.a = m + 3*(width + 1)
                        self.b = m + 5*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 3*(width + 1)) in self.availables and (m + 4*(width + 1)) in self.availables:
                        self.a = m + 3*(width + 1)
                        self.b = m + 4*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      w > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m - width - 1) in self.availables and (m + width + 1) in self.availables:
                        self.a = m - width - 1
                        self.b = m + width + 1
                        return True, self.a, self.b
                    
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      w > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m - width - 1) in self.availables and (m + 2*(width + 1)) in self.availables:
                        self.a = m - width - 1
                        self.b = m + 2*(width + 1)
                        return True, self.a, self.b
                    
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      w > 0 and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1):
                    if (m - width - 1) in self.availables and (m + 3*(width + 1)) in self.availables:
                        self.a = m - width - 1
                        self.b = m + 3*(width + 1)
                        return True, self.a, self.b
                    
                #活四負斜率
                if (w in range(n - 3, width) and h in range(height - n + 3) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 2) * (width - 1), width - 1))) == 1):
                    if (m - width + 1) in self.availables and m + (n - 2) * (width - 1) in self.availables and w < width - 1 and w > n - 3:
                        self.a = m - width + 1
                        self.b = m + (n - 2) * (width - 1)
                        return True, self.a, self.b
                    elif (m - width + 1) in self.availables and (m - 2*(width - 1)) in self.availables and w < width - 2:
                        self.a = m - width + 1
                        self.b = m - 2*(width - 1)
                        return True, self.a, self.b
                    elif (m + (n - 2) * (width - 1)) in self.availables and (m + (n - 1) * (width - 1)) in self.availables and w > n - 2:
                        self.a = m + (n - 2) * (width - 1)
                        self.b = m + (n - 1) * (width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables and (m + 5*(width - 1)) in self.availables:
                        self.a = m + width - 1
                        self.b = m + 5*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables and (m + 4*(width - 1)) in self.availables:
                        self.a = m + width - 1
                        self.b = m + 4*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables and (m + 3*(width - 1)) in self.availables:
                        self.a = m + width - 1
                        self.b = m + 3*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables and (m + 2*(width - 1)) in self.availables:
                        self.a = m + width - 1
                        self.b = m + 2*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m + 2*(width - 1)) in self.availables and (m + 5*(width - 1)) in self.availables:
                        self.a = m + 2*(width - 1)
                        self.b = m + 5*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 2*(width - 1)) in self.availables and (m + 4*(width - 1)) in self.availables:
                        self.a = m + 2*(width - 1)
                        self.b = m + 4*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 2*(width - 1)) in self.availables and (m + 3*(width - 1)) in self.availables:
                        self.a = m + 2*(width - 1)
                        self.b = m + 3*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m + 3*(width - 1)) in self.availables and (m + 5*(width - 1)) in self.availables:
                        self.a = m + 3*(width - 1)
                        self.b = m + 5*(width - 1)
                        return True, self.a, self.b
             
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 3*(width - 1)) in self.availables and (m + 4*(width - 1)) in self.availables:
                        self.a = m + 3*(width - 1)
                        self.b = m + 4*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      w < width - 1 and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m - width + 1) in self.availables and (m + width - 1) in self.availables:
                        self.a = m - width + 1
                        self.b = m + width - 1
                        return True, self.a, self.b
                    
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      w < width - 1 and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m - width + 1) in self.availables and (m + 2*(width - 1)) in self.availables:
                        self.a = m - width + 1
                        self.b = m + 2*(width - 1)
                        return True, self.a, self.b
                    
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      w < width - 1 and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1):
                    if (m - width + 1) in self.availables and (m + 3*(width - 1)) in self.availables:
                        self.a = m - width + 1
                        self.b = m + 3*(width - 1)
                        return True, self.a, self.b
                    

                    
#落二子唯一防禦                        
    def is_defand2(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row
        self.a = 0
        moved = list(set(range(width * height)) - set(self.availables))
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            if self.current_player != player and (self.hand - 1)%2 == 0:
                #擋橫活五
                if (w in range(width - n + 2) and
                    len(set(states.get(i, -1) for i in range(m, m + n - 1))) == 1):
                    
                    if ((m - 1) in self.availables and  w > 0 and 
                        (m + n - 1) in self.availables and w < width - n + 1):
                        self.a = m - 1
                        self.b = m + n - 1
                        return True, self.a, self.b
                #擋直活五    
                if (h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * width, width))) == 1):
                    if (m - width) in self.availables and (m + (n - 1) * width) in self.availables:
                        self.a = m - width
                        self.b = m + (n - 1) * width
                        return True, self.a, self.b
                    
                #擋正斜活五
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width + 1), width + 1))) == 1):
                    if ((m - width - 1) in self.availables and w > 0 and 
                        (m + (n - 1) * (width + 1)) in self.availables and w < (width - n + 1)):
                        self.a = m - width - 1
                        self.b = m + (n - 1) * (width + 1)
                        return True, self.a, self.b
                    
                #擋負斜活五
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width - 1), width - 1))) == 1):
                    if ((m - width + 1) in self.availables and w < width - 1 and
                        (m + (n - 1) * (width - 1)) in self.availables and w > n - 2):
                        self.a = m - width + 1
                        self.b = m + (n - 1) * (width - 1)
                        return True, self.a, self.b
                
  #落一子唯一防禦                  
    def is_defand1(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row
        self.a = 0
        moved = list(set(range(width * height)) - set(self.availables))
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]
            if self.current_player != player and (self.hand - 1)%2 == 0:
                #擋橫死五
                if (w in range(width - n + 2) and
                    len(set(states.get(i, -1) for i in range(m, m + n - 1))) == 1):
                    
                    if ((m + n - 1) in self.availables and w < width - n + 1):
                        self.a = m + n - 1
                        return True, self.a
                    elif ((m - 1) in self.availables and w < width - n + 1 and w > 0):
                        self.a = m - 1
                        return True, self.a
                
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 1) in self.availables:
                        self.a = m + 1
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 2) in self.availables:
                        self.a = m + 2
                        return True, self.a
                  
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 4, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 3) in self.availables:
                        self.a = m + 3
                        return True, self.a
                    
                if (w in range(width - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 1, -1) == 1 and
                      states.get(m + 2, -1) == 1 and
                      states.get(m + 3, -1) == 1 and
                      states.get(m + 5, -1) == 1):
                    if (m + 4) in self.availables:
                        self.a = m + 4
                        return True, self.a
                    
                #擋直死五
                if (h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * width, width))) == 1):
                    if (m - width) in self.availables:
                        self.a = m - width
                        return True, self.a
                    elif (m + (n - 1) * width) in self.availables:
                        self.a = m + (n - 1) * width
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + width) in self.availables:
                        self.a = m + width
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 2*width) in self.availables:
                        self.a = m + 2*width
                        return True, self.a
                    
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 4*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 3*width) in self.availables:
                        self.a = m + 3*width
                        return True, self.a
                   
                if (h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width, -1) == 1 and
                      states.get(m + 2*width, -1) == 1 and
                      states.get(m + 3*width, -1) == 1 and
                      states.get(m + 5*width, -1) == 1):
                    if (m + 4*width) in self.availables:
                        self.a = m + 4*width
                        return True, self.a
                    
                #擋正斜死五
                if (w in range(width - n + 2) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width + 1), width + 1))) == 1):
                    if (m - width - 1) in self.availables and w > 0:
                        self.a = m - width - 1
                        return True, self.a
                    
                    elif (m + (n - 1) * (width + 1)) in self.availables and w < (width - n + 1):
                        self.a = m + (n - 1) * (width + 1)
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + width + 1) in self.availables:
                        self.a = m + width + 1
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 2*(width + 1)) in self.availables:
                        self.a = m + 2*(width + 1)
                        return True, self.a
                
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 4*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 3*(width + 1)) in self.availables:
                        self.a = m + 3*(width + 1)
                        return True, self.a
                    
                if (w in range(width - n + 1) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width + 1, -1) == 1 and
                      states.get(m + 2*(width + 1), -1) == 1 and
                      states.get(m + 3*(width + 1), -1) == 1 and
                      states.get(m + 5*(width + 1), -1) == 1):
                    if (m + 4*(width + 1)) in self.availables:
                        self.a = m + 4*(width + 1)
                        return True, self.a
                    
                #擋負斜死五
                if (w in range(n - 2, width) and h in range(height - n + 2) and
                      len(set(states.get(i, -1) for i in range(m, m + (n - 1) * (width - 1), width - 1))) == 1):
                    if (m - width + 1) in self.availables and w < width - 1:
                        self.a = m - width + 1
                        return True, self.a
                    elif (m + (n - 1) * (width - 1)) in self.availables and w > n - 2:
                        self.a = m + (n - 1) * (width - 1)
                        return True, self.a
                
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + width - 1) in self.availables:
                        self.a = m + width - 1
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 2*(width - 1)) in self.availables:
                        self.a = m + 2*(width - 1)
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 4*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 3*(width - 1)) in self.availables:
                        self.a = m + 3*(width - 1)
                        return True, self.a
                    
                if (w in range(n - 1, width) and h in range(height - n + 1) and
                      states.get(m, -1) == 1 and
                      states.get(m + width - 1, -1) == 1 and
                      states.get(m + 2*(width - 1), -1) == 1 and
                      states.get(m + 3*(width - 1), -1) == 1 and
                      states.get(m + 5*(width - 1), -1) == 1):
                    if (m + 4*(width - 1)) in self.availables:
                        self.a = m + 4*(width - 1)
                        return True, self.a
                        
                
        
    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if(len(moved) < self.n_in_row + 2):
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            self.hand = 0
            return True, winner
        elif not len(self.availables):#
            self.hand = 0
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player


class Game(object):
    """
    game server
    """

    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2):
        """
        Draw the board and show game info
        """
        width = board.width
        height = board.height

        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    print('X'.center(8), end='')
                elif p == player2:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')
            
    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """
        start a game between two players
        """
        if start_player not in (0,1):
            raise Exception('start_player should be 0 (player1 first) or 1 (player2 first)')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2:player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player)
        self.board.do_move(40) #先手天元
        while(1):
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            if self.board.is_sure_win1():
                self.board.do_move(self.board.a)
            elif self.board.is_sure_win2():
                self.board.do_move(self.board.a)
                self.board.do_move(self.board.b)
            elif self.board.is_defand2():
                self.board.do_move(self.board.a)
                self.board.do_move(self.board.b)
            elif self.board.is_defand1():
                self.board.do_move(self.board.a)
            else:
                move = player_in_turn.get_action(self.board)
                self.board.do_move(move)
            
            if is_shown:
                self.graphic(self.board, player1.player, player2.player)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner   
            
            
    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree
        store the self-play data: (state, mcts_probs, z)
        """
        self.board.init_board()        
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], [] 
        self.board.do_move(40) #先手天元
        while(1):
            if self.board.is_sure_win1():
                move_probs = np.zeros(self.board.width*self.board.height)
                move_probs[self.board.a] = 1.0
                states.append(self.board.current_state())
                mcts_probs.append(move_probs)
                current_players.append(self.board.current_player)
                self.board.do_move(self.board.a)
            elif self.board.is_sure_win2():
                move_probs = np.zeros(self.board.width*self.board.height)
                move_probs[self.board.a] = 1.0
                states.append(self.board.current_state())
                mcts_probs.append(move_probs)
                current_players.append(self.board.current_player)
                self.board.do_move(self.board.a)
                
                move_probs = np.zeros(self.board.width*self.board.height)
                move_probs[self.board.b] = 1.0
                states.append(self.board.current_state())
                mcts_probs.append(move_probs)
                current_players.append(self.board.current_player)
                self.board.do_move(self.board.b)
            else:
                move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
                # store the data
                states.append(self.board.current_state())
                mcts_probs.append(move_probs)
                current_players.append(self.board.current_player)
                # perform a move
                self.board.do_move(move)
                
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))  
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                #reset MCTS root node
                player.reset_player() 
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, list(zip(states, mcts_probs, winners_z))
