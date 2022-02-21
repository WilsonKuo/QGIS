#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
import os 
import random
from acsprism import rtdb_init
from modebase import ModeBase

__author__ = 'Wilson Kuo'

def main():
    rtdb_init()
    m = ModeBase(0)
    for ls in m.lsSet:
        ls.pa = random.randint(100,200)
        ls.pb = random.randint(100,200)
        ls.pc = random.randint(100,200)
        ls.stastatus = 1
        ls.lsact = 0


if __name__ == "__main__":
    main()    
