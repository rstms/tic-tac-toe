#!/usr/bin/env python

#--------------------------------------------
#
# tic tac toe
#
# Copyright (C) 2017 Reliance Systems, Inc.
#
# Author: Matt Krueger <mkrueger@rstms.net>
# Date: 2017-08-24
# http://www.rstms.net
#
#--------------------------------------------

from random import choice

class Board(object):
    def __init__(self):
        self.winner = 0
        self.cells=[]
        for row in range(3):
            self.cells.append([0, 0, 0])

    def row_chars(self, row):
        """return array of chars representing row state"""
        c = ['X', ' ', 'O']
        return [c[row[r]+1] for r in range(3)]

    def row_str(self, r):
        """return row of board graph"""
        c = [r+1]
        c.extend(self.row_chars(self.cells[r]))
        return '%d  %c | %c | %c ' % tuple(c)

    def print(self, msg):
        """display board state"""
        print()
        if msg:
            print('%s\n' % msg)
        print('   A   B   C ')
        print('             ')
        print(self.row_str(0))
        print('  ---+---+---') 
        print(self.row_str(1))
        print('  ---+---+---')
        print(self.row_str(2))
        print()

    def apply_move(self, row, col, value):
        self.cells[row][col] = value

    def check_win_set(self, values):
        """return true if values contain a winning set"""
        s = sum(values)
        if s < -2:
            self.winner = -1
        elif s > 2:
            self.winner = 1
        return self.winner != 0

    def make_set(self, pairs):
        """return a set of cell values for a given set of index pairs"""
        return [self.cells[t[0]][t[1]] for t in pairs]

    def check_win(self):
        """check for end of game condition"""
        #print('check_win cells: %s' % repr(self.cells))
        for iset in self.generate_set_indices():
            if self.check_win_set(self.make_set(iset)):
                return True
        return self.check_tie() 

    def check_tie(self):
        """ check for all squares filled """
        full = 0
        for iset in self.generate_set_indices()[0:3]:
            s = self.make_set(iset)
            if not 0 in s:
                full += 1
        return full > 2

    def generate_set_indices(self):
        """ generate array of index pairs of rows columns and diagonals"""
        #print('check_win cells: %s' % repr(self.cells))
        isets = []
        for row in range(3):
            isets.append([(row, col) for col in range(3)])
        for col in range(3):
            isets.append([(row, col) for row in range(3)])
        isets.append([(0,0), (1,1), (2,2)])
        isets.append([(0,2), (1,1), (2,0)])
        return isets

    def find_win_move(self, player):
        """ return move that completes 3 in a row"""
        for iset in self.generate_set_indices():
            s = self.make_set(iset)
            if s.count(0) == 1 and s.count(player) == 2:
                #print('found win: %s %s' % (s, iset))
                pos = s.index(0)
                return self.make_move(iset[pos][0], iset[pos][1])
        return None

    def find_block_move(self, player):
        """return move that blocks opponents 3 in a row"""
        return self.find_win_move(player * -1)

    def find_possible_win_move(self, player):
        """return move that is in a winnable row"""
        for iset in self.generate_set_indices():
            s = self.make_set(iset)
            if s.count(player * -1) == 0:
                pos = s.index(0)
                row = iset[pos][0]
                col = iset[pos][1]
                #print('found possible_win: %s %s %d %d %d' % (s, iset, pos, row, col))
                return self.make_move(row, col)
        return None

    def make_move(self, row, col):
        return '%c,%c' % (str(row+1), chr(ord('A')+col))

    def find_possible_block_move(self, player):
        return self.find_possible_win_move(player * -1)

    def find_random_move(self):
        moves = []
        for iset in self.generate_set_indices():
            s = self.make_set(iset)
            for i in range(3):
                if s[i] == 0:
                    moves.append((iset[i][0], iset[i][1]))
        move = choice(moves)
        #print('random_move %s %s' % (moves, move))
        return self.make_move(move[0],move[1])


class Game(object):
    def __init__(self):
        self.board = Board()
        self.round = 1

    def instructions(self):
        print('Enter your move in row,column format: example: "2,b" to choose the center square.')
        print()

    def run(self):
        """game logic loop, run until game over"""
        self.instructions()
        my_move = 1
        while not self.board.check_win():
            self.board.print('Round %d' % self.round)
            my_move *= -1
            if my_move>0:
              move = self.calculate_move(my_move)
            else:
              move = self.prompt_move()
            row, col = self.parse_move(move)
            self.board.apply_move(row, col, my_move)
            if my_move:
                self.round += 1

        if self.board.winner == -1:
            winner = 'X'
        elif self.board.winner == 1:
            winner = 'O'
        else:
            winner = 'nobody'

        self.board.print('%s wins!' % winner)

    def prompt_move(self):
        """prompt and apply move"""
        move=None
        while not move:
            move = self.validate_input(input('Your move, X [row,column]: '))
            row, col = self.parse_move(move)
            if not self.validate_move(row, col):
                move = None
        return move

    def parse_move(self, resp):
        """convert input to row,col integers"""
        if resp:
            row, col = resp.split(',')
            row = int(row)-1
            col = ord(col)-ord('A')
        else:
            row = -1
            col = -1
        #print('parse_move(%s) returning %s, %s' % (resp, row, col))
        return row,col

    def validate_input(self, resp):
        """detect and reject improperly formatted input"""
        msg = None
        ret = None
        resp = resp.strip().upper()
        if len(resp) == 2:
            l = list(resp)
            l.insert(1,',')
            resp=''.join(l)
        if len(resp) != 3:
            msg = 'input must be exactly 3 characters'
        elif not resp[0].isnumeric():
            msg = 'input must begin with a number'
        elif not resp[1] == ',':
            msg = 'input must be in the form of NUMBER,LETTER'
        elif not resp[-1].isalpha():
            msg = 'input must end with a letter'
        else:
            ret = resp
        if msg:
            print('Error: %s' % msg)
        #print('validate_input returning %s' % ret)
        return ret

    def validate_move(self, row, col):
        """make sure move is on the board and the target cell is empty"""
        valid = False
        if 0 <= row <= 2 and 0 <= col <= 2:
            if self.board.cells[row][col] == 0:
                valid = True
        #print('validate_move(%d,%d) returning %s)' % (row, col, valid))
        return valid

    def calculate_move(self, player):
        """calculate an AI tic-tac-toe move"""
        #move = self.prompt_move()
        move = self.board.find_win_move(player) or \
            self.board.find_block_move(player) or \
            self.board.find_possible_win_move(player) or \
            self.board.find_possible_block_move(player) or  \
            self.board.find_random_move()
        print('O\'s move: %s' % move)
        return move


if __name__ == '__main__':
    print()
    print('Welcome to tic-tac-toe!')
    print('-----------------------')
    Game().run()
