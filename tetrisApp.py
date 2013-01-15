#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tetrisApp.py: the main class which handles the gui (drawing, events) and the instance of the tetris class"""

import numpy
import wx
import gui
import tetris
import pieces

class TetrisApp(wx.App):
    def OnInit(self):
        # generate main window and safe instance in self.frame
        frame = gui.MainFrame(None, -1, "")
        frame.Show(True)
        self.SetTopWindow(frame)
        self.frame = frame

        self.fastDown = False;

        # generate tetris instance
        self.tetris = tetris.Tetris(600)

        # bind events
        wx.EVT_MENU(self, wx.ID_EXIT, self.MenuExit)
        wx.EVT_MENU(self, wx.ID_NEW, self.NewGame)
        wx.EVT_MENU(self, self.frame.itemPause.GetId(), self.PauseGame)
        wx.EVT_PAINT(self.frame.drawPanel, self.OnPaint)
        wx.EVT_TIMER(self.frame, self.frame.timer.GetId(), self.OnTimer)
        wx.EVT_KEY_DOWN(self.frame.drawPanel, self.OnKeyDown)
        wx.EVT_KEY_UP(self.frame.drawPanel, self.OnKeyUp)

        self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL, ord('P'), self.frame.itemPause.GetId()),
                                              (wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
                                              (wx.ACCEL_NORMAL, wx.WXK_F2, wx.ID_NEW)])
        self.frame.SetAcceleratorTable(self.accel_tbl)
        return True

    # Called with events from menu and accelerator
    def MenuExit(self, event):
         self.frame.Close(True)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_LEFT:
            self.tetris.MoveLeft()
        elif keycode == wx.WXK_RIGHT:
            self.tetris.MoveRight()
        elif keycode == wx.WXK_UP:
            self.tetris.RotatePiece()
        elif keycode == wx.WXK_DOWN and not self.fastDown:
            self.fastDown = True
            self.frame.timer.Start(50)
        self.frame.Refresh()


    def OnKeyUp(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DOWN and self.fastDown:
            self.fastDown = False
            self.frame.timer.Start(self.tetris.cSpeed)
        event.Skip()
        self.frame.Refresh()


    # call from EVT_PAINT
    def OnPaint(self, event):
        dc = wx.PaintDC(self.frame.drawPanel)

        # calculate some basic variables for drawing
        boardPixelWidth, boardPixelHeight = dc.GetSize()
        pieceWidth = boardPixelWidth // self.tetris.BOARD_WIDTH
        pieceHeight = boardPixelHeight // self.tetris.BOARD_HEIGHT
        offsetX = (boardPixelWidth - pieceWidth * self.tetris.BOARD_WIDTH) // 2
        offsetY = boardPixelHeight - pieceHeight * self.tetris.BOARD_HEIGHT

        # draw board
        for (y, x), value in numpy.ndenumerate(self.tetris.board):
            if value != 0:
                self.DrawRect(dc, x, y, pieceWidth, pieceHeight, pieces.Pieces.colors[value], offsetX, offsetY)

        # draw current tile
        if self.tetris.cPiece is not None:
            for (y, x), value in numpy.ndenumerate(self.tetris.cPiece.shape):
                    if value != 0:
                        self.DrawRect(dc, x + self.tetris.cPiece.x, y + self.tetris.cPiece.y, pieceWidth, pieceHeight,
                            self.tetris.cPiece.color, offsetX, offsetY)

    # draw one rect from a piece
    def DrawRect(self, dc, x, y, pieceWidth, pieceHeight, color, offsetX, offsetY):
        cx = offsetX + x * pieceWidth
        cy = offsetY + y * pieceHeight

        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(cx, cy, pieceWidth, pieceHeight)

        dc.SetPen(wx.Pen(self.GenerateLighterColor(color), 1))
        dc.DrawLine(cx, cy, cx + pieceWidth - 2, cy)
        dc.DrawLine(cx, cy, cx, cy + pieceHeight -1)

        dc.SetPen(wx.Pen(self.GenerateDarkerColor(color), 1))
        dc.DrawLine(cx + pieceWidth - 1, cy, cx + pieceWidth - 1, cy + pieceHeight -1)
        dc.DrawLine(cx + 1, cy + pieceHeight -1, cx + pieceWidth - 1, cy + pieceHeight - 1)

        dc.SetPen(wx.Pen('white', 1))

    # returns a lighter color generated from the given one
    def GenerateLighterColor(self, color):
        r, g, b = color
        r = r if r > 205 else r + 50
        g = g if g > 205 else g + 50
        b = b if b > 205 else b + 50
        return r,g,b

    # returns a darker color generated from the given one
    def GenerateDarkerColor(self, color):
        r, g, b = color
        r = r if r < 50 else r - 50
        g = g if g < 50 else g - 50
        b = b if b < 50 else b - 50
        return r,g,b

    # starts a new game. called from the menu or keyboard shortcut
    def NewGame(self, event):
        self.tetris.NewGame()

        self.frame.frameStatusbar.SetStatusText(u'Run', 0)
        self.frame.frameStatusbar.SetStatusText(u'Next piece: ' + self.tetris.nPiece.name, 1)
        self.frame.frameStatusbar.SetStatusText(u'Points: ' + str(self.tetris.points) + u' (' + str(self.tetris.level) + u')', 2)

        self.frame.itemPause.Enable(True)
        self.frame.Refresh()

        self.frame.timer.Start(self.tetris.cSpeed)

    # called on timer event
    def OnTimer(self, event):
        if self.tetris.MoveDown():
            self.frame.frameStatusbar.SetStatusText(u'Next piece: ' + self.tetris.nPiece.name, 1)
            self.frame.frameStatusbar.SetStatusText(u'Points: ' + str(self.tetris.points) + u' (' + str(self.tetris.level) + u')', 2)
            if not self.fastDown and self.frame.timer.GetInterval != self.tetris.cSpeed:
                self.frame.timer.Start(self.tetris.cSpeed)
        else:
            self.frame.timer.Stop()
            self.frame.itemPause.Enable(False)
            self.frame.frameStatusbar.SetStatusText(u'Game over', 0)
        self.frame.Refresh()

    # pause the current game
    def PauseGame(self, event):
        if self.frame.itemPause.IsEnabled() and not self.fastDown:
            if self.frame.timer.IsRunning():
                self.frame.frameStatusbar.SetStatusText(u'Pause', 0)
                self.frame.timer.Stop()
            else:
                self.frame.frameStatusbar.SetStatusText(u'Run', 0)
                self.frame.timer.Start(self.tetris.cSpeed)

# start the app
def main():
    app = TetrisApp(0)
    app.MainLoop()

if __name__ == '__main__':
    main()