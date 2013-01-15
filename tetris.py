#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tetris.py: the game class wich holds the bord and the game logic"""

import numpy
from pieces import Pieces

class Tetris():

    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22

    pointsPerRows = [10, 30, 100, 400]
    speedIncrease = 50
    cPiece = None

    def __init__(self, startSpeed):
        self.board = numpy.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH), numpy.int8)
        self.cSpeed = startSpeed

        # fill the board with some pieces for testing
        self.board[0, 0] = 1
        self.board[0, 1] = 2
        self.board[0, 2] = 3
        self.board[0, 3] = 4
        self.board[0, 4] = 5
        self.board[0, 5] = 6
        self.board[0, 6] = 7
        self.board[4, 7] = 1
        self.board[5, 3] = 3
        self.board[15, 9] = 1
        self.board[12, 4] = 2
        self.board[21, 0] = 3
        self.board[12, 1] = 2
        self.board[7, 3] = 3
        self.board[16, 6] = 1
        self.board[19, 2] = 3
        self.board[20, 8] = 1
        self.board[21, 6] = 2
        self.board[17, 3] = 2
        self.board[21, 9] = 3

    # called when a new game is started
    def NewGame(self):
        self.board.fill(0) # clear board
        self.points = 0 # reset points
        self.linesRemoved = 0 # counts how often lines removed not the lines itself
        self.level = 1
        self.cPiece = Pieces.GetNewPiece() # generate current piece
        self.cPiece.SetPosition(self.BOARD_WIDTH // 2 - 2, -5) # new piece start above the board
        self.nPiece = Pieces.GetNewPiece() # generate nex piece

    def MoveDown(self):
        if self.MoveDownPossible():
            self.cPiece.MoveDown() # move current piece one row down
        else:
            if self.CheckGameOver():
                return False
            self.CopyPieceToBoard()
            self.CheckFullLines()
            if self.linesRemoved > 10:
                self.cSpeed -= self.speedIncrease
                self.level += 1
                self.linesRemoved = 0
            self.cPiece = self.nPiece
            self.cPiece.SetPosition(self.BOARD_WIDTH // 2 - 2, -5) # new piece start above the board
            self.nPiece = Pieces.GetNewPiece() # generate next piece
        return True

    def MoveLeft(self):
        if self.MoveLeftPossible():
            self.cPiece.MoveLeft()

    def MoveRight(self):
        if self.MoveRightPossible():
            self.cPiece.MoveRight()

    def CheckGameOver(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            if value != 0 and self.cPiece.y + y < 0:
                    return True
        return False

    def MoveDownPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x
            ty = self.cPiece.y + 1
            if value != 0 and ty + y >= 0:
                if ty + y >= self.BOARD_HEIGHT or self.board[ty +y, tx + x] != 0:
                    return False
        return True

    def MoveLeftPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x - 1
            ty = self.cPiece.y
            if value != 0 and ty + y >= 0:
                if tx + x < 0 or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def MoveRightPossible(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            tx = self.cPiece.x + 1
            ty = self.cPiece.y
            if value != 0 and tx + x >= 0 and ty + y >= 0:
                if tx + x >= self.BOARD_WIDTH or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def RotatePieceRightPossible(self):
        return self.RotatePiecePossible(numpy.rot90(self.cPiece.shape))

    def RotatePieceLeftPossible(self):
        return self.RotatePiecePossible(numpy.rot90(self.cPiece.shape, 3))

    def RotatePiecePossible(self, shape):
        for (y, x), value in numpy.ndenumerate(shape):
            tx = self.cPiece.x
            ty = self.cPiece.y
            if value != 0 and ty + y >= 0:
                if ty + y >= self.BOARD_HEIGHT or tx + x < 0 or tx + x >= self.BOARD_WIDTH or self.board[ty + y, tx + x] != 0:
                    return False
        return True

    def RotatePiece(self):
        if self.RotatePieceRightPossible():
            self.cPiece.RotateRight()
        elif self.RotatePieceLeftPossible():
            self.cPiece.RotateLeft()

    def CopyPieceToBoard(self):
        for (y, x), value in numpy.ndenumerate(self.cPiece.shape):
            if value != 0:
                self.board[self.cPiece.y + y, self.cPiece.x + x] = value

    def CheckFullLines(self):
        removedLinesCount = numpy.count_nonzero(numpy.all(self.board != 0, 1))
        if removedLinesCount != 0:
            removedLines = self.board[numpy.all(self.board != 0, 1)]
            removedLines.fill(0)
            cleanBoard= self.board[numpy.any(self.board == 0, 1)]
            self.board = numpy.vstack((removedLines, cleanBoard))
            self.points += self.pointsPerRows[removedLinesCount - 1]
            self.linesRemoved += 1