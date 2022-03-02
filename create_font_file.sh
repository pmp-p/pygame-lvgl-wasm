#!/bin/bash
#
# This script will convert a font file to a bit-map oriented format usable by LVGL.
# For details: https://github.com/lvgl/lv_font_conv
#
# Preconditions
# Install the font conversion tool: 
#    npm i lv_font_conv -g

# The NotoSans font file was downloaded from https://github.com/googlefonts/noto-cjk/tree/main/Sans/OTF/SimplifiedChinese
lv_font_conv --bpp 2 --size 18 --font NotoSansCJKsc-Regular.otf -r 0x20-0xFFFF --format lvgl --force-fast-kern-format -o noto_sans_cjk_18_2bpp.c
