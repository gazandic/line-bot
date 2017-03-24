import re;
import requests;
import json;
import datetime;
from dateutil.parser import parse


class TextProcessor(object):
	def __init__(self):
		self.keyWordToCall  = "Si Bawel";
		self.keyWordToEvent = ["jadwal"];
		self.keyWordPengeluaran = ["pengeluaran"];
		self.listActionInEvent = {"ikut" : "ikut", "ganti" : "ubah", "buat":"tambah", "tambah":"tambah", "bikin":"tambah", "gajadiikut":"gajadiikut", "ubah":"ubah", "hapus":"hapus"};
		self.listActionInPengeluaran =["tambah", "ubah", "hapus", "lihat"];  

	def isCalled(self, sentence):
		checkifCalled = re.compile(r'({0})'.format(self.keyWordToCall), flags=re.IGNORECASE);
		if (checkifCalled.findall(sentence)):
			return True;
		else:
			return False;

	def getCommands(self, sentence):
		getTheCommand = re.compile(r'{0}\b(.+)'.format(self.keyWordToCall), flags=re.IGNORECASE);
		if(getTheCommand.findall(sentence)):
			return(getTheCommand.findall(sentence));		

	def checkAmount(self, sentence):
		keywordAmount = ["sebesar"];
		for key in keywordAmount:
			getAmount = re.compile(r'{0}\s(.+)\s'.format(key));
			if (getAmount.findall(sentence)):
				return getAmount.findall(sentence);
			else:
				return None;

	def checkActionPengeluaran(self, sentence, pengeluaranKey):
		for action in self.listActionInPengeluaran:
			isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
			if(isContain.findall(sentence)):
				if action == "tambah":	
					amount = isContain.findall(sentence)[0];
					if(self.checkAmount(sentence) != None):
						event_nameRe = re.compile(r'{0}\s(.*)\s){1}'.format(pengeluaranKey, action));
						event_name = event_nameRe.findall(sentence)[0];
						result = json.dumps({'type': 'pengeluaran', 'command': {action}, 'amount': amount,'event_name': event_name});
						break;
					else:
						print("minta jumlah duit boss")#minta jumlah duit atau bisa jadi dia mau kasi pake gambar
				else:
					event_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey));
					result = json.dump({'type': u'pengeluaran', 'command': action, 'event_name': event_name});
		return result;

	def checkActionEvent(self, sentence):
		keyTime = ["pukul", "jam"];
		temp_sentence = str(sentence);
		for key in keyTime:
			findTime = re.compile(r'{0}\W(\d+.\d+.\w+|\d+.\w+)'.format(key,));
			timeFound = findTime.findall(temp_sentence);
			if(timeFound):
				timeSentence = timeFound[0];
				timeSentenceToExclude = key +" "+ timeSentence;
				print(timeSentenceToExclude);
				excludeTimeSentence = re.compile(r'{0}'.format(timeSentenceToExclude));
				temp_sentence = excludeTimeSentence.sub('', temp_sentence);
				break;
		print temp_sentence;
		dateSentence = self.checkDate(temp_sentence);
		datetypedate =self.dateParser(dateSentence, timeSentence);
		#cara eventnamenya cuy
		for action in self.listActionInEvent:
			isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE);
			if(isContain.findall(temp_sentence)):
				if action in ["buat", "tambah", "bikin", "ubah"]:
					json.dumps({'type': 'event', 'command': {listActionInEvent[action]}, 'amount': amount,'event_name': event_name})
					

	def checkWhatCommand(self, sentence):
		if (self.getCommands(sentence)):
			for command in self.getCommands(sentence):
				for key in keyWordPengeluaran:
					isContain = re.compile(r'\b({0})\b'.format(key), flags=re.IGNORECASE);
					if (isContain.findall(sentence)):
						self.checkActionPengeluaran(sentence,key);
	
	def dateParser(self, dateSentence, timeSentence):
		bulanDetected = False;
		yearDetected = False;
		now = datetime.datetime.now()
		monthNameToNumber = {"januari": 1, "februari":2, "maret":3, "april":4, "mei":5, "juni":6, "juli":7, "agustus":8, "september":9, "oktober":10, "november":11, "desember":12};
		for monthname in monthNameToNumber:
			if (re.compile(r'\b({0})\b'.format(monthname), flags=re.IGNORECASE)):
				bulanDetected = True;
				dateSentence = re.sub(monthname, str(monthNameToNumber[monthname]), dateSentence, flags = re.IGNORECASE);
		digitSplit = re.compile(r'\W+(\d+)');
		takeDigitOnly = re.compile(r'\b(\d+)\b');
		digits = takeDigitOnly.findall(dateSentence);
		print (digits);
		temp_dateSentence = ""
		for digit in digits:
			if int(digit) > 31:
				yearDetected = True;
			temp_dateSentence = temp_dateSentence + str(digit)+ " ";
		if len(digits) > 2 :
			date = parse(temp_dateSentence);
		elif len(digits) == 2:
			if (bulanDetected):
				if (not yearDetected):
					temp_dateSentence = temp_dateSentence + " " + str(now.year); 
				else:
					temp_dateSentence = "1 " + temp_dateSentence
					#nanya tanggal
			else:
				if int(digits[1]) <= 12:
					bulanDetected = True;
				if (bulanDetected):
					 temp_dateSentence = temp_dateSentence + " " + str(now.year);
		else: #cuman 1 digit
			if yearDetected:
				temp_dateSentence = "1 "+ "1 " + temp_dateSentence;
				#nanya tanggal dan bulan
			elif bulanDetected:
				temp_dateSentence = "1 " + temp_dateSentence + " " + str(now.year);
				#nanya tanggal, tahun asumsi tahun ini
			else: #asumsi ngasih tangga doang ini
				temp_dateSentence = temp_dateSentence + " " + str(now.month) + " " + str(now.year);
		print temp_dateSentence;
		if (timeSentence):
			keteranganWaktu=["pagi", "siang", "sore", "malam"];
			temp_timeSentence = "";
			timeDigits = takeDigitOnly.findall(timeSentence);
			if len(timeDigits) ==1:
				temp_timeSentence = timeDigits[0] + ":00:00"
			elif len(timeDigits) ==2:
				temp_timeSentence = timeDigits[0] +":" +timeDigits[1]+":00";
			else:
				temp_timeSentence = timeDigits[0] +":"+timeDigits[1]+":"+timeDigits[2];
			print (temp_dateSentence+temp_timeSentence)
			date = parse(temp_dateSentence+temp_timeSentence);
		else:
			print("jam berapa mau dilakukan bos"); #ngga kedeteksi waktunya
		return date;

	def checkDate(self, sentence):
		token = "87dea5be-c26c-4bbb-afe4-adb5b982f55a"
		parameters = {'m': sentence, 'api_token': '87dea5be-c26c-4bbb-afe4-adb5b982f55a'}
		r = requests.get('https://api.kata.ai/v1/insights', params = parameters)
		result = r.json();
		entities = result["entities"];
		finalResult = None;
		for entity in entities:
			if entity["entity"] == "DATE":
				 finalResult = entity["fragment"];
		print(result);
		return finalResult;

test = TextProcessor();
test.checkDate("lari di saraga tanggal 24 Maret 1995 jam 5 pagi");
test.checkActionEvent("lari di saraga tanggal 4 April 1995 jam 5.30");
# print(test.dateParser("tanggal 24 Maret"));