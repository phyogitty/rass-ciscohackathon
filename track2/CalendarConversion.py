'''CONVERTING DATA FROM JSON FILE INTO ICS FILE(CALENDAR)'''
from ics import Calendar, Event, Todo
import json
from datetime import  datetime, timedelta
from dateutil import tz
class CalendarConversion():
    def __init__(self, msg):
        #states.json is an example json file
        # with open('states.json') as f:
        #     self.JsonData = json.load(f)
        self.msg = msg
        self.convertToICS()

    def convertToICS(self):
        '''
        Convert data into ics file
        '''
        importantInfor = [(date, detail) for date, detail in zip(self._getDateAndTime(), self._getDetail())]
        # print(importantInfor)
        for idx, infor in enumerate(importantInfor):
            '''
            infor[0]: (starting time, ending time)
            infor[1]: event's detail
            '''
            event = Event()
            todo = Calendar()
            event.name = "Testing with Rass"   # Header of the file
            event.begin =  infor[0][0]  # Time event starts
            event.end = infor[0][1]     # Time event ends
            event.description = infor[1] 
            todo.events.add(event)
            todo.events
            filename = "generated_calendar"    #reformat to create the file
            with open(filename+'.ics', 'w') as f:
                f.write(str(todo))

    def _getDetail(self):
        return self.msg['body']
        # return [i['detail'] for i in self.msg['body']]

    def _getDate(self):
        '''
        Year-Month-Day
        '''
        return self.msg['datetime'][0].split('-')
        # return self.msg['datetime'][0]
        # return [i['date'].split('-') for i in self.msg['email']]

    def _getTime(self):
        '''
        Created a list of time in string format
        Hour:Minute:Second
        '''
        # time = []
        # for item in self.msg['email']:
        #     temp = ['0']*3  #default time when time is None
        #     if item['time'] :
        #         temp = item['time'].split(':')
        #     time.append(temp)
        # print(time)
        # return time
        # return self.msg['datetime'][1]
        return self.msg['datetime'][1].split(':')
    
    def _getDateAndTime(self):
        '''
        Created a list of datetime objects
        By default, the event will last for 1 hour
        If time is None value, assume that event will last for a whole day
        '''
        # dateAndTime = [date+ time for date, time in zip(self._getDate(), self._getTime())]
        DateAndTime = []
        item = self._getDate()
        item.extend(self._getTime())
        # print(self._getDate(), "\n")
        # print(self._getTime())
        # print(dateAndTime, "\n******")
        # for item in dateAndTime:
            #datetime(Year, Month, Day, Hour, Minute, Second)
            # print(item)
        year, month, day, hour, minute, second = int(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]), int(item[5])
        start_time = datetime(year, month, day, hour, minute, second).astimezone(tz.tzutc())
        end_time = datetime(year, month, day, hour + 1, minute, second).astimezone(tz.tzutc())
        if hour == 0 and minute == 0 and second == 0:
            '''Handling time with None value'''
            end_time = datetime(year, month, day + 1, hour, minute, second).astimezone(tz.tzutc())  
            # DateAndTime.append((start_time, end_time))

        return [(start_time, end_time)]

#msg = {'date':'2014-20-20'}
#test = CalendarConversion(msg)
