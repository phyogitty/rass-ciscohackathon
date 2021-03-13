import re
import csv

# input: csv file with mail body and header (each row has body, header)
# regex: search for key words and numbers in email, if none exist, don't add to new file
# output: new csv file with filtered mails

class MailFilter:
	
	keywords = ['mon', 'tue', 'wed', 'thur', 'fri', 'schedule',
				'sat', 'sun', 'tomorrow', 'week', 'today', 'month', 
				'morning', 'night', 'lunch', 'meeting', 'year', 'next', 
				'evening', 'pm', 'am', 'p.m.', 'a.m.', 'dinner', 'breakfast', 
				'conference', 'time', 'agenda', 'appointment',
				'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
				'sep', 'oct', 'nov', 'dec', 'date', 'calender']
	
	def __init__(self, mailFile):
		self.mailFile = mailFile
		
	def readfile(self):

		with open(self.mailFile, 'r', encoding='windows-1252') as f:
			reader = csv.reader(f)
			
			with open('filtered_mail.csv', 'a', newline='', encoding='utf-8') as nf:  # nf for "new file"
				writer = csv.writer(nf)
				
				for line in reader:
					r_line = line[0].replace('\n', ' ');	# line[0] only read first column of row
					
					for keyword in self.keywords:
						if re.search(keyword, line[1].lower()): 
							writer.writerow(line)
							break
				
		
		
test = MailFilter('testingdata.csv');
test.readfile();
