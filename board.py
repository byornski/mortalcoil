#!/usr/bin/env python
import numpy as np
import copy

class board:

    blocked_square = -1
    empty_square = -2
    
    def __init__(self,level,xSize,ySize,boardstring):
        '''Given the size, level and boardstring returns a board'''
        self.level = int(level)
        self.xSize = int(xSize)
        self.ySize = int(ySize)
        self.board = self._readString(boardstring)

    def _readString(self,string):
        '''Read the board string and convert it into an array'''
        repls = {
            '.':self.empty_square,
            'X':self.blocked_square
        }

        b =  [repls[x] for x in string]
        return np.reshape(b,(self.ySize,self.xSize))

    def __str__(self):
        '''Printable form of the current board'''
        info = "Board for level %d\nBoard is %d by %d\n" % (self.level, self.xSize, self.ySize)
        return info + str(self.board)

        
    def copy(self):
        '''Get a brand spanking new copy of the board'''
        return copy.deepcopy(self)

    def isEmpty(self,pos):
        '''Is the specified position empty?'''
        return self.inBounds(pos) and self.board[pos] == self.empty_square

    def inBounds(self,pos):
        '''Is the positon in bounds?'''
        y,x = pos
        return x in xrange(self.xSize) and y in xrange(self.ySize)

    def __setitem__(self,key,value):
        '''Allows the board to be accessed directly -- board[pos] = 2'''
        self.board[key] = value

    def __getitem__(self,key):
        '''Allows the board to be accessed directly -- print board[pos]'''
        return self.board[key]

    def reset(self,level=0):
        '''Reset anything higher than level to empty'''
        self.board[self.board > level] = self.empty_square
        #self.board = np.minimum(self.board,level)

    def finished(self):
        '''Are there empty squares?'''
        return np.any(self.board == self.empty_square)
