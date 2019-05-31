# -*- coding: UTF-8 -*-
import subprocess
import argparse
import random
import time
import os,shutil
import ctypes,sys
import heapq
import json
import re

def exec(filename, deadCodeLine, choice=1):
    f = open(filename, 'r')
    alllines = f.readlines()
    f.close()

    if choice == 1 :  # 删除所有dead code
        f = open(filename,'w+')
        for idx, line in enumerate(alllines):
            if str(idx+1) not in deadCodeLine:
                f.writelines(line)
        f.close()
    else :
        pass