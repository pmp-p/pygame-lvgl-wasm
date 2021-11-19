#!/usr/bin/env python3
import faulthandler

import lvgl
from PyQt5 import QtCore, QtGui, QtWidgets

faulthandler.enable()
app = QtWidgets.QApplication([])


class LvglWindow(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(lvgl.HOR_RES, lvgl.VER_RES)
        self.setMaximumSize(lvgl.HOR_RES, lvgl.VER_RES)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def mousePressEvent(self, evt):
        self.mouseMoveEvent(evt)

    def mouseReleaseEvent(self, evt):
        self.mouseMoveEvent(evt)

    def mouseMoveEvent(self, evt):
        pos = evt.pos()
        lvgl.send_mouse_event(pos.x(), pos.y(), evt.buttons() & QtCore.Qt.LeftButton)

    def update(self):
        # Poll lvgl and display the framebuffer
        for i in range(10):
            lvgl.poll()

        data = bytes(lvgl.framebuffer)
        img = QtGui.QImage(data, lvgl.HOR_RES, lvgl.VER_RES, QtGui.QImage.Format_RGB16)
        pm = QtGui.QPixmap.fromImage(img)

        self.setPixmap(pm)


win = LvglWindow()
win.show()


# Build a GUI
# run this script using -i to try commands interactively

class SymbolButton(lvgl.Btn):
    def __init__(self, symbol, text, *args, **kwds):
        super().__init__(*args, **kwds)
        self.symbol = lvgl.Label(self)
        self.symbol.set_text(symbol)
        # self.symbol.set_style(symbolstyle)
        self.symbol.align(self, lvgl.ALIGN.CENTER, 0, 0)

        self.label = lvgl.Label(self)
        self.label.set_text(text)
        self.label.align(self, lvgl.ALIGN.CENTER, 20, 0)


class MainMenu(lvgl.Obj):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.btnPrint = SymbolButton(lvgl.SYMBOL.PLAY, 'Print', parent=self)
        self.btnPrint.set_x(0)
        self.btnPrint.set_y(0)
        self.btnPrint.set_width(160)
        self.btnPrint.set_height(90)

        self.btnChange = SymbolButton(lvgl.SYMBOL.SHUFFLE, 'Change filament', parent=self)
        self.btnChange.set_x(160)
        self.btnChange.set_y(0)
        self.btnChange.set_width(160)
        self.btnChange.set_height(90)

        self.btnPreheat = SymbolButton(lvgl.SYMBOL.CHARGE, 'Preheat', parent=self)
        self.btnPreheat.set_x(0)
        self.btnPreheat.set_y(90)
        self.btnPreheat.set_width(160)
        self.btnPreheat.set_height(90)

        self.btnSettings = SymbolButton(lvgl.SYMBOL.SETTINGS, 'Settings', parent=self)
        self.btnSettings.set_x(160)
        self.btnSettings.set_y(90)
        self.btnSettings.set_width(160)
        self.btnSettings.set_height(90)

        self.lblStatus = lvgl.Label(self)
        self.lblStatus.set_text(lvgl.SYMBOL.CHARGE + ' heating')
        self.lblStatus.align(self, lvgl.ALIGN.IN_BOTTOM_LEFT, 5, -5)


s3 = MainMenu()
lvgl.scr_load(s3)

s3.btnPrint.set_event_cb(print)

print(s3.btnPrint.get_type())

app.exec_()
