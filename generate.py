#!/usr/bin/env python3
import sourceparser
from python import PythonBindingsGenerator

parseresult = sourceparser.LvglSourceParser().parse_sources('lvgl')
py_gen = PythonBindingsGenerator(parseresult)
py_gen.generate()
