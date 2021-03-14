import re
import csv
from datetime import datetime

# need: current date in (tomorrow, next week)
# Look for day of the week separately
# dayoftheweek(DOTW), month(m) day(2;0<d<32), year(4;y>=thisyear)
# xx:xx (pm,am) (today, next week, friday..)  
# x:00(pm) time should be recorded separately
# take in the first time, first month, day, weekdate, year.
# soley weekdate 
# x(a.m.)
# x/xx/xxxx 
# month. date"th" x-x (pm)

# standalone: time(assume today), nextdate, thisdate
# couple: month,day 
# optional: pm, am, year(assume today), no need for 4 digit 
# if month/day is present, day of the week not needed.


# extracts time information from a csv file with emailbody string in one cell
class TimeExtractor:
	
	weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
	months = [	'jan' , 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
				'sep', 'oct', 'nov', 'dec']
	
	# creates list in order of [month(0),date(1),year(2),hour,minute)
	now = datetime.today().strftime("%m-%d-%y-%H-%M")
	nowsplit = now.split('-')
	nowsplit = [int(i) for i in nowsplit] 
	nowsplit[2] = 2000 + nowsplit[2]
	
	# extracted information
	exTime = []
	exMonth = 0
	exDate = 0
	exYear = 0
	
	invalidDate = 0
	newDateTime = None

	def __init__(self, fileName):
		self.fileName = fileName
	
	def extractTime(self):
		with open(self.fileName, 'r', encoding='windows-1252') as f:
			reader = csv.reader(f)
			
			mailbody = ''
			for line in reader:
				mailbody = line[1].lower()
				break #make sure to only read the first row
				
			# time of the day
			found = re.search("[0-2]?[0-9]:[0-5][0-9]", mailbody)
			if found!=None:
				found = found.group(0)
				self.exTime = found.split(':')
				self.exTime = [int(i) for i in self.exTime] 
				if re.search("(p.m.|pm)", mailbody) and self.exTime[0]<12:	# assuming only one time in email
					self.exTime[0] = self.exTime[0]+12
			
			
			# xx/xx/xxxx or x/xx/xxxx or x/x/xxxx or xx/xx  or x/x or x/xx. 
			found = re.search("[0-1]?[0-9]/[1-3]?[0-9](/20[2-9][0-9])?", mailbody)
			if found!=None:
				found = found.group(0)
				foundlist = found.split('/')
				self.exMonth = int(foundlist[0])
				self.exDate = int(foundlist[1])
				if len(foundlist)>2:
					if int(foundList[2])<self.nowsplit[2]:
						invalidDate = 1		# if year is in the past, email probably isn't a scheduling mail
					else: 					
						self.exYear = int(foundlist[2])
						
				newDateTime = self.formatDate()	
				return newDateTime
			
			
			# if month is found, look for other date information 
			found = re.search("(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", mailbody)
			if found!=None: 
				found = found.group(0)
				foundmonth = self.months.index(found)+1		
				
				bodypostmonth = mailbody[mailbody.find(found):]  #temp[temp.find("Jan"):]
				
				found = re.search("[^0-9][1-3]?[0-9][^0-9]", bodypostmonth)
				if found==None:
					invalidDate = 1		# just month and no date is invalid
					return None
				found = found.group(0)
				self.exMonth = foundmonth
				self.exDate = int(found[1:len(found)-1])
				
				found = re.search("(20)[0-9][0-9]", mailbody)
				if found!=None:
					found = found.group(0)
					if int(found)<self.nowsplit[2]:
						invalidDate = 1
						return None
					else:
						self.exYear = int(found)
						
				newDateTime = self.formatDate()
				return newDateTime
			
			
			# conventionally formatted date has not been found
			
			# tomorrow, next week (next month and year not considered)
			found = re.search("(tomorrow|next week)", mailbody)
			if found!=None:
				found = found.group(0)
				if found=="tomorrow":
					newDateTime = self.now+timedelta(days=1)
				elif found=="next week":
					newDateTime = self.now+timedelta(weeks=1)
				return newDateTime
			
			# next weekday
			found = re.search("next (mon|tue|wed|thur|fri|sat|sun)", mailbody)
			if found!=None:
				found = found.group(0)
				thisweekday = self.now.weekday()
				foundweekday = weekdays.index(found)
				
				nextweekdaydelta = 7+(foundweekday-thisweekday)
				newDateTime = self.now+timedelta(days=nextweekdaydelta)
				return newDateTime
				
			# today?
			if len(self.exTime)==0:
				return None
			else:
				self.exYear = self.nowsplit[2]
				self.exMonth = self.nowsplit[0]
				self.exDate = self.nowsplit[1]
			
			return self.formatDate()
				
				
	def formatDate(self):
		if (self.invalidDate==1):
			return None
		elif self.exYear==0 and self.invalidDate==0:
			self.exYear = self.nowsplit[2]
		
		return datetime(self.exYear, self.exMonth, self.exDate, self.exTime[0], self.exTime[1], 0, 0)
		
		
				
				
test = TimeExtractor("filtered_mail.csv")
print(test.extractTime())
