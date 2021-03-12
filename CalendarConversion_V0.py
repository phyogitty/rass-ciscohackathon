'''
ISSUE: ONLY THE TIME(HH:MM:SS) IN ICS FILE IS NOT WORKING PROPERLY
'''
from ics import Calendar, Event
import json
from datetime import  datetime

class CalendarConversion():
    def __init__(self):
        with open('states.json') as f:
            self.JsonData = json.load(f)
        self.convertToICS()

    def convertToICS(self):
        '''
        Convert data into ics file
        '''
        importantInfor = [(date, detail) for date, detail in zip(self._getDateAndTime(), self._getDetail())]
        for idx, infor in enumerate(importantInfor):
            event = Event()
            todo = Calendar()
            event.name = infor[1]   # Header of the file
            event.begin =  infor[0] # Time to start
            #e.description = ...    # Extra detail ?????
            todo.events.add(event)
            todo.events
            filename = infor[1].replace(" ", "")    #reformat to create the file
            with open(filename+'.ics', 'w') as f:
                f.write(str(todo))

    def _getDetail(self):
        return [i['detail'] for i in self.JsonData['email']]

    def _getDate(self):
        return [i['date'].split('-') for i in self.JsonData['email']]

    def _getTime(self):
        '''
        Created a list of time in string format
        '''
        time = []
        for item in self.JsonData['email']:
            temp = ['0']*3  #default time when time is None
            if item['time'] :
                temp = item['time'].split(':')
            time.append(temp)
        return time
    
    def _getDateAndTime(self):
        '''
        Created a list of datetime objects
        '''
        dateAndTime = [date+ time for date, time in zip(self._getDate(), self._getTime())]
        DateAndTime = []
        for item in dateAndTime:
            #datetime(Year, Month, Day, Hour, Minute, Second)
            value = datetime(int(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]), int(item[5]))
            DateAndTime.append(value)
        return DateAndTime


test = CalendarConversion()
