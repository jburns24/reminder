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
    timeDelimeters = ['in', 'at', 'on']
    reversed_argList = list(reversed(argList))
    ti_index = []
    if 'every' in argList:
        ti_index.append(reversed_argList.index('every'))
        if ti_index:
            return len(argList) - max(ti_index)        
    else:
        for el in timeDelimeters:
            if el in reversed_argList:
                ti_index.append(reversed_argList.index(el))
        if ti_index:
            return len(argList) - min(ti_index)

# This function takes a time string for the delimeter 'in'
# and splits it into a list of 2-tuples. Each tuple represents
# an amount of time. 
def getTimePairs_in(time_str):
    ti_list = time_str.split()
    ti_list.remove('and')
    if (len(ti_list) % 2) != 0:
        print("You had malformatted time string for in. Accept input like '1 hour and 15 min")
        exit()
    tup_list = []
    for i in range(len(ti_list) / 2):
        index = i * 2
        temp_list = [ti_list[index], ti_list[index + 1]]
        tup_list.append(tuple(temp_list))
    return tup_list

def getTotalSeconds(time_tuple):
    minutes = ['min', 'minutes', 'm']
    hours = ['hours', 'hour', 'h']
    seconds = ['seconds', 'sec', 's']
    total_time = 0
    for tu in time_tuple:
        measurment = str(tu[1]).lower()
        if measurment in minutes:
            total_time += int(tu[0]) * 60
            continue
        if measurment in hours:
            total_time += int(tu[0]) * 60 * 60
            continue
        if measurment in seconds:
            total_time += int(tu[0])
            continue
    return total_time



if __name__ == '__main__':
    curTime = time.localtime(time.time())
    numArgs = len(sys.argv)
    argList = sys.argv
    if numArgs == 0:
        print('no args')
        exit()
    time_delimeter = getTimeIndex(argList)
    if time_delimeter is None:
        message = ' '.join(argList)
        print('Entered an invalid reminder')
        exit()
    time_str = ' '.join(argList[time_delimeter:])
    message_str = ' '.join(argList[1:time_delimeter - 1])
    delimeter = argList[time_delimeter - 1]
    if delimeter == 'in':
        time_list = getTimePairs_in(time_str)
        total_time = getTotalSeconds(time_list)
        exit()
    if min:
        #time.sleep(min[0])
        Notify.init('Remind Me')
        notification = Notify.Notification.new('REMINDER', str(argList))
        notification.show()

