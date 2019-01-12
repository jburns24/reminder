import sys, time

class TimeConverter:
    def __init__(self):
        self.epoch = int(time.time())
        self.dateObj = time.localtime(time.time())

    def updateEpoch(self):
        self.epoch = int(time.time())

    def updateDateObj(self):
        self.dateObj = time.localtime(time.time())

    def getEpoch(self):
        return self.epoch

    def getDateObj(self):
        return self.dateObj

    # This function takes a time string for the delimeter 'in'
    # and splits it into a list of 2-tuples. Each tuple represents
    # an amount of time. 
    def getTimePairs_in(self, time_str):
        ti_list = time_str.split()
        if 'and' in ti_list:
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

    def getTotalSeconds(self, time_tuple):
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
    
    def getSecondsTillReminder(self, offset):
        self.updateEpoch()
        return self.getEpoch() + offset