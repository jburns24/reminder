#!/usr/bin/env python3

import time
import gi
import sys
gi.require_version('Notify', '0.7')
from gi.repository import Notify

def cleanUp():
    Notify.uninit()

# this funciton returns an index that corresponds to where
# in the argList that the time object begins.
# It is also known that the index returned -1 is where the
# time delimiter is located so the message we want to 
# remind the user about is located from arglist[1: index -1]
def getTimeIndex(argList):
    timeDelimeters = ["in", "at", "on"]
    reversed_argList = list(reversed(argList))
    ti_index = []
    if "every" in argList:
        ti_index.append(reversed_argList.index("every"))
        if ti_index:
            return len(argList) - max(ti_index)        
    else:
        for el in timeDelimeters:
            if el in reversed_argList:
                ti_index.append(reversed_argList.index(el))
        if ti_index:
            return len(argList) - min(ti_index)

def getTimePairs(time_str):
    print(time_str)


if __name__ == '__main__':
    curTime = time.localtime(time.time())
    numArgs = len(sys.argv)
    argList = sys.argv
    if numArgs == 0:
        print("no args")
        exit()
    time_delimeter = getTimeIndex(argList)
    if time_delimeter is None:
        message = " ".join(argList)
        print(f'"{message}" is an invalid reminder')
        exit()
    time_str = " ".join(argList[time_delimeter:])
    message_str = " ".join(argList[1:time_delimeter - 1])
    delimeter = argList[time_delimeter - 1]
    if delimeter = 'on':
        getTimePairs(time_str)
        exit()    
    if min:
        #time.sleep(min[0])
        Notify.init("Remind Me")
        notification = Notify.Notification.new("REMINDER", str(argList))
        notification.show()

