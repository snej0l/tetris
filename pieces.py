#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pieces.py: 2 classes for manage pieces
Pieces class: holds information for all available pieces an hast a static method which returns a single piece
Piece class: represents a single piece"""

import numpy
import random

class Pieces():

    allPieces = numpy.array([[[0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0],
                              [0, 0, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 1, 1, 0],
                              [0, 0, 1, 0]],
                             [[0, 0, 0, 0],
                              [0, 0, 2, 0],
                              [0, 2, 2, 0],
                              [0, 2, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 3, 0, 0],
                              [0, 3, 0, 0],
                              [0, 3, 3, 0]],
                             [[0, 0, 0, 0],
                              [0, 0, 4, 0],
                              [0, 0, 4, 0],
                              [0, 4, 4, 0]],
                             [[0, 0, 5, 0],
                              [0, 0, 5, 0],
                              [0, 0, 5, 0],
                              [0, 0, 5, 0]],
                             [[0, 0, 0, 0],
                              [0, 6, 6, 0],
                              [0, 6, 6, 0],
                              [0, 0, 0, 0]],
                             [[0, 0, 0, 0],
                              [0, 7, 7, 7],
                              [0, 0, 7, 0],
                              [0, 0, 0, 0]]])
    names = ['-', 'S', 'Z', 'L', 'J', 'I', 'O', 'T']
    # colors for the pieces
    # (black, green, magenta, orange, red, yellow, blue, cyan)
    colors = [(0,0,0), (40,247,54), (253,76,252), (253,146,38), (252,42,28),
        (254,249,55), (16,63,251), (44,252,254)]

    def GetNewPiece():
        entropy = random.SystemRandom()
        pieceNumber = entropy.randrange(1, 8)
        return Piece(Pieces.names[pieceNumber], Pieces.allPieces[pieceNumber], Pieces.colors[pieceNumber])

    GetNewPiece = staticmethod(GetNewPiece)

class Piece():
    x = 0
    y = 0

    def __init__(self, pieceName, pieceShape, pieceColor):
        self.name = pieceName
        self.shape = pieceShape
        self.color = pieceColor

    # set the position of the piece
    def SetPosition(self, x, y):
        self.x = x
        self.y = y

    # move the piece one row down
    def MoveDown(self):
        self.y += 1

    # move the piece one column left
    def MoveLeft(self):
        self.x -= 1

    # move the piece one column right
    def MoveRight(self):
        self.x += 1

    # rotate the piece left (not implemented yet)
    def RotateLeft(self):
        self.shape = numpy.rot90(self.shape, 3)

    # rotate the piece right (not implemented yet)
    def RotateRight(self):
        self.shape = numpy.rot90(self.shape)