#!/usr/bin/env python

import time
import sys
from ReminderDaemon import RDaemon
from time_converter import TimeConverter

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

# This funciton writes to the reminder_log
# storing the message and the time
# message - what you want to be reminded about
# time - when you want to be reminded (for first run seconds til reminder)
def writeMessage(message, time, logfile):    
    file(log_file, 'a').write("%d %s\n" % (int(time),str(message)))

if __name__ == '__main__':
    timeConverter = TimeConverter()
    pid_location = '/tmp/reminder.pid'
    log_file = '/tmp/reminder_log'
    argList = sys.argv
    if len(sys.argv) == 1:
        print('no args')
        exit()
    rDaemon = RDaemon(pid_location, log_file)

    # Check if the pid exists
    try:
            pf = file(pid_location,'r')
            pid = int(pf.read().strip())
            pf.close()
    except IOError:
            pid = None

    if len(sys.argv) > 2:
        time_delimeter = getTimeIndex(argList)
        if time_delimeter is None:
            message = ' '.join(argList)
            print('Entered an invalid reminder')
            exit()

        time_str = ' '.join(argList[time_delimeter:])
        message_str = ' '.join(argList[1:time_delimeter - 1])
        delimeter = argList[time_delimeter - 1]

        if delimeter == 'in':
            total_time = timeConverter.getTotalSeconds(timeConverter.getTimePairs_in(time_str))
            writeMessage(message_str, timeConverter.getSecondsTillReminder(total_time), log_file)
            if not pid:
                rDaemon.start()
            exit()

    # Check if the command is to kill the reminder daemon
    kill = None
    if len(sys.argv) == 2 and argList[1] == 'kill':
        kill = True
    if kill:
        rDaemon.stop()
    # else:
    #     rDaemon.daemonize()
    #     rDaemon.run()        

