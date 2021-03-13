import csv

class MailContentToCSV:

	def __init__(self, filename):
		self.filename = filename
		
	def write(self, body, header):
		self.splitbody = body.split(' ')
		self.splitheader = header.split(' ')
		
		with open(self.filename, 'a', newline='') as f:
			writer = csv.writer(f)
			
			#odd row=body, even row=header
			writer.writerow(self.splitbody)
			writer.writerow(self.splitheader)
	
			
			
test = StringToCSV("test.csv")
test.write("hello james, can you send me the doc? thanks.", "document inquiry")
test.write("hello boss, when is the meeting tomorrow?", "meeting tomorrow")
test.write("long time no see! how have you been?", "what's up?")
