#!/usr/bin/env python3
from time import sleep

import lvgl


"""
# Next lines replace 'import lvgl' by a mechanism with flexible path. Why can't this simpler?
# Complicating factor, it looks like a normal python import, but we import a C-module.
pylvgl_path = "."
spec = importlib.util.spec_from_file_location("lvgl", pylvgl_path)
lvgl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lvgl)
"""


# CKI: do something with lv_disp_buf_init(), it could improve display refresh speed. Now called from PyInit_lvgl in lvglmodule.c

# CKI: lv_init() and lv_disp_drv_init() are called from PyInit_lvgl in lvglmodule.c

# Build a GUI

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
        self.btnChange.set_pos(160, 0)
        self.btnChange.set_size(160, 90)

        self.btnPreheat = SymbolButton(lvgl.SYMBOL.CHARGE, 'Preheat', parent=self)
        self.btnPreheat.set_pos(0, 90)
        self.btnPreheat.set_size(160, 90)

        self.btnSettings = SymbolButton(lvgl.SYMBOL.SETTINGS, 'Settings', parent=self)
        self.btnSettings.set_pos(160, 90)
        self.btnSettings.set_size(160, 90)

        self.lblStatus = lvgl.Label(self)
        self.lblStatus.set_text(lvgl.SYMBOL.CHARGE + ' heating')
        self.lblStatus.align(self, lvgl.ALIGN.IN_BOTTOM_LEFT, 5, -5)

basic_style = lvgl.Style()
basic_style.set_bg_color(lvgl.STATE.DEFAULT, lvgl.COLOR.ORANGE.full)

s3 = MainMenu()
s3.add_style(lvgl.OBJ_PART.MAIN, basic_style)

lvgl.scr_load(s3)

s3.btnPrint.set_event_cb(print)

print(s3.btnPrint.get_type())


last_printed_time = -1
while True:
    """
    Call LVGL's task handler & make the screen sleep for 10 milliseconds.
    """
    lvgl.tick_inc(10)
    lvgl.task_handler()
    sleep(0.01)

    inactive_time = int(lvgl.disp_get_inactive_time(disp=0) / 1000)
    if last_printed_time != inactive_time:
        last_printed_time = inactive_time
        print(f"Inactive for {inactive_time} seconds")
