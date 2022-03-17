#!/bin/bash
#
# This script will convert a high-resolution font file to a bit-map oriented format usable by LVGL.
# For details: https://github.com/lvgl/lv_font_conv
#
# Preconditions
# Install the LVGL font conversion tool:
#    npm i lv_font_conv -g

# The NotoSans font file was downloaded from https://github.com/googlefonts/noto-cjk/tree/main/Sans/OTF/SimplifiedChinese
# Convert the whole visible Unicode range, i.e. character code positions 0x20 to 0xFFFF
# There are 2 glyphs with huge impact on the total line height, resulting in a total box height of 34 where we target around 20.
# We adopted the range to exclude U+3031 and U+3032, these are two kanji repeat characters that we can do without.
lv_font_conv --bpp 2 --size 18 --font NotoSansCJKsc-Regular.otf -r 0x20-0x3030,0x3033-0xFFFF --format lvgl --force-fast-kern-format -o noto_sans_cjk_18_2bpp.c
