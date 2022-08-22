import numpy as np # numbers
import time # timing
import sys
from time import time as gt # for "get time"
from time import sleep # Usually not a good thing to use
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def flinput(prompt): # get input as a floating-point number
    return float(input(prompt))
def print_bold(text): # print text in bold
    print('\033[1m' + text + '\033[0m')

def excelFormat(string):
    # add .xlsx to the end of a string
    # (if it doesn't already end in .xlsx)
    if string[-5:]==".xlsx":
        return string
    return string + ".xlsx"

def timeFormat(s):
    # convert seconds to min:sec
    text = "{mins:n}:{secs:02.0f}"
    return text.format(mins=s//60,secs=s%60)

def sigfigs1(n, figs=2):
    # round to significant figures
    if n < 0:
        neg = True
        n *= -1
    else: neg = False
    if n == 0:
        return 0
    try:
        log_remainder = (np.log(n)/np.log(10)%1)
    except: 
        return 0
    starts_with_1 = log_remainder < (np.log(2)/np.log(10)%1)
    if starts_with_1 and figs==1:
        figs = 2
    digits = np.floor(np.log(n)/np.log(10))+1
    rounded = np.round(n, figs - int(digits))
    if neg:
        rounded *= -1
    return rounded

def to_num(string):
    # convert a string to a number
        # int if an integer
        # float if a decimal
        # np.nan if not a number
    try:
        n = float(string)
    except:
        return np.nan
    if n % 1 == 0:
        return int(n)
    return n

def current_time():
    # current time as hr:min:sec
    t = time.localtime(time.time())
    [h, m, s] = t[3:6]
    ampm = " am"
    if h>12:
        h = h % 12
        ampm = " pm"
    text = "{hrs:n}:{mins:02n}:{secs:02.0f}"
    return text.format(hrs=h,mins=m,secs=s)+ampm

def mysleep(t):
    t0 = gt()
    while gt()<t0+t:
        pass

"""
Turns a string into a number
    - integers turn into ints
    - other numbers turn into floats
    - non-numbers turn into np.nan
"""
def to_num(string):
    try:
        n = float(string)
    except:
        return np.nan
    if n % 1 == 0:
        return int(n)
    return n

# There can't be multiple QApplications at once, so this function opens one but makes sure it's the only one
def qap():
    if not QApplication.instance():
        return QApplication(sys.argv)
        # return QApplication([]) 
            # if there's no chance of command-line arguments
    else:
        return QApplication.instance()


# code from the internet, used to get the position of the mouse
from ctypes import windll, Structure, c_long, byref
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y
def getval():
    x,y = queryMousePosition()
    return 1-y/912  #+ random.random()*0.1-0.05