import re
import requests
import json
import os
from datetime import datetime
from dateutil.parser import parse

class TextProcessor(object):
	def __init__(self):
		self.keyWordToCall  = "Si Bawel"
		self.keyWordToEvent = ["jadwal","event","acara"]
		self.keyWordPengeluaran = ["pengeluaran"]
		self.listActionInEvent = {"ikut" : "ikut","lihat" : "lihat", "ganti" : "ubah", "buat":"tambah", "tambah":"tambah", "bikin":"tambah", "gajadiikut":"gajadiikut", "ubah":"ubah", "hapus":"hapus"}
		self.listActionInPengeluaran ={"lihat" : "lihat", "ganti" : "ubah", "buat":"tambah", "tambah":"tambah", "bikin":"tambah", "ubah":"ubah", "hapus":"hapus"}
		self.jsonToSend = None

	def isCalled(self, sentence):
		checkifCalled = re.compile(r'({0})'.format(self.keyWordToCall), flags=re.IGNORECASE)
		if (checkifCalled.findall(sentence)):
			return True
		else:
			return False

	def getCommands(self, sentence):
		getTheCommand = re.compile(r'{0}\b(.+)'.format(self.keyWordToCall), flags=re.IGNORECASE)
		if(getTheCommand.findall(sentence)):
			return(getTheCommand.findall(sentence))

	def checkAmount(self, sentence):
		keywordAmount = ["sebesar"]
		for key in keywordAmount:
			getAmount = re.compile(r'{0}\s*(\d+\.+\d+|\d+).*'.format(key))
			if (getAmount.findall(sentence)):
				return getAmount.findall(sentence)
			else:
				return None

	def json_serial(self,obj):
		if isinstance(obj,datetime):
			serial = obj.isoformat()
			return serial
		raise TypeError("Type not serializable")

	def checkActionPengeluaran(self, sentence, pengeluaranKey):
		for action in self.listActionInPengeluaran:
			isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
			if(isContain.findall(sentence)):
				if action in ["buat", "tambah", "bikin", "ubah", "ganti"]:
					if(self.checkAmount(sentence) != None):
						amount = self.checkAmount(sentence)
						pengeluaran_nameRe = re.compile(r'{0}\s+(.*)\s+{1}'.format(pengeluaranKey, "sebesar"), flags=re.IGNORECASE)
						pengeluaran_name = 'unknown'
						if (pengeluaran_nameRe.findall(sentence)):
							pengeluaran_name = pengeluaran_nameRe.findall(sentence)
						self.jsonToSend = json.dumps({'type': 'pengeluaran', 'command': action, 'data':{'amount': amount,'pengeluaran_name': pengeluaran_name}})
						break
					else:
						pengeluaran_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey))
						pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
						self.jsonToSend = json.dumps({'type': 'pengeluaran', 'command': action, 'data':{'amount': 0,'pengeluaran_name': pengeluaran_name}})
				else:
					pengeluaran_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey))
					pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
					self.jsonToSend = json.dumps({'type': u'pengeluaran', 'command': action, 'data':{'pengeluaran_name': pengeluaran_name}})

	# def checkActionPengeluaran(self, sentence, pengeluaranKey):
	# 	for action in self.listActionInPengeluaran:
	# 		isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
	# 		if(isContain.findall(sentence)):
	# 			if action in ["buat", "tambah", "bikin", "ubah", "ganti"]:
	# 				amount = isContain.findall(sentence)[0]
	# 				if(self.checkAmount(sentence) != None):
	# 					pengeluaran_nameRe = re.compile(r'{0}\s(.*)\s){1}'.format(pengeluaranKey, action))
	# 					pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
	# 					self.jsonToSend = json.dumps({'type': 'pengeluaran', 'command': self.listActionInEvent[action], 'data':{'amount': amount,'pengeluaran_name': pengeluaran_name}})
	# 					break
	# 				else:
	# 					pengeluaran_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey))
	# 					pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
	# 					self.jsonToSend = json.dumps({'type': 'pengeluaran', 'command': self.listActionInEvent[action], 'data':{'pengeluaran_name': pengeluaran_name}})
	#
	# 			else:
	# 				pengeluaran_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey))
	# 				pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
	# 				self.jsonToSend = json.dumps({'type': 'pengeluaran', 'command': self.listActionInEvent[action], 'data':{'pengeluaran_name': pengeluaran_name}})

	def checkActionEvent(self, sentence, eventKey):
		keyTime = ["pukul", "jam"]
		temp_sentence = str(sentence)
		timeSentence = None
		for key in keyTime:
			findTime = re.compile(r'{0}\W(\d+.\d+.\w+|\d+.\w+)'.format(key,))
			timeFound = findTime.findall(temp_sentence)
			if(timeFound):
				timeSentence = timeFound[0]
				timeSentenceToExclude = key +" "+ timeSentence
				# print(timeSentenceToExclude)
				excludeTimeSentence = re.compile(r'{0}'.format(timeSentenceToExclude))
				temp_sentence = excludeTimeSentence.sub('', temp_sentence)
				break
		dateSentence = self.checkDate(temp_sentence)
		if dateSentence :
			datetypedate =self.dateParser(dateSentence, timeSentence)
		for action in self.listActionInEvent:
			isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
			if(isContain.findall(temp_sentence)):
				if action in ["buat", "tambah", "bikin", "ubah", "ganti"]:
					event_nameRe = re.compile(r'{0}\s(.+)\s{1}'.format(eventKey, "tanggal"), flags=re.IGNORECASE)
					event_name = event_nameRe.findall(sentence)[0]
					self.jsonToSend = json.dumps({'type': 'event', 'command': self.listActionInEvent[action], 'data':{'date': self.json_serial(datetypedate),'event_name': event_name}})
				else:
					event_nameRe = re.compile(r'{0}\s(.+)\s'.format(eventKey), flags=re.IGNORECASE)
					event_name = event_nameRe.findall(sentence)[0]
					self.jsonToSend = json.dumps({'type': 'event', 'command': self.listActionInEvent[action], 'data':{'event_name': event_name}})

	def checkWhatCommand(self, sentence):
		if (self.getCommands(sentence)):
			for command in self.getCommands(sentence):
				for key in self.keyWordPengeluaran:
					isContain = re.compile(r'\b({0})\b'.format(key), flags=re.IGNORECASE)
					if (isContain.findall(sentence)):
						self.checkActionPengeluaran(sentence,key)
			if (self.jsonToSend == None):
				for key in self.keyWordToEvent:
					isContain = re.compile(r'\b({0})\b'.format(key), flags=re.IGNORECASE)
					if (isContain.findall(sentence)):
						self.checkActionEvent(sentence,key)
		else:
			#commandnya ngga ketangkep
			print("aku ra ngerti")

	def dateParser(self, dateSentence, timeSentence):
		bulanDetected = False
		yearDetected = False
		now = datetime.now()
		monthNameToNumber = {"januari": 1, "februari":2, "maret":3, "april":4, "mei":5, "juni":6, "juli":7, "agustus":8, "september":9, "oktober":10, "november":11, "desember":12}
		for monthname in monthNameToNumber:
			if (re.compile(r'\b({0})\b'.format(monthname), flags=re.IGNORECASE)):
				bulanDetected = True
				dateSentence = re.sub(monthname, str(monthNameToNumber[monthname]), dateSentence, flags = re.IGNORECASE)
		digitSplit = re.compile(r'\W+(\d+)')
		takeDigitOnly = re.compile(r'\b(\d+)\b')
		digits = takeDigitOnly.findall(dateSentence)
		temp_dateSentence = ""
		for digit in digits:
			if int(digit) > 31:
				yearDetected = True
			temp_dateSentence = temp_dateSentence + str(digit)+ " "
		if len(digits) > 2 :
			date = parse(temp_dateSentence)
		elif len(digits) == 2:
			if (bulanDetected):
				if (not yearDetected):
					temp_dateSentence = temp_dateSentence + str(now.year) + " "
				else:
					temp_dateSentence = "1 " + temp_dateSentence
					#nanya tanggal
			else:
				if int(digits[1]) <= 12:
					bulanDetected = True
				if (bulanDetected):
					 temp_dateSentence = temp_dateSentence + str(now.year)+ " "
		else: #cuman 1 digit
			if yearDetected:
				temp_dateSentence = "1 "+ "1 " + temp_dateSentence
				#nanya tanggal dan bulan
			elif bulanDetected:
				temp_dateSentence = "1 " + temp_dateSentence + str(now.year) + " "
				#nanya tanggal, tahun asumsi tahun ini
			else: #asumsi ngasih tangga doang ini
				temp_dateSentence = temp_dateSentence + " " + str(now.month) + " " + str(now.year)+ " "

		# print (temp_dateSentence)
		if (timeSentence):
			keteranganWaktu=["siang", "sore"]
			temp_timeSentence = ""
			s = timeSentence.split()
			digit = int(s[0])
			if s[len(s)-1] == "malam" and digit <= 12 and digit >= 6 or s[len(s)-1] in keteranganWaktu and digit <= 7:
				digit = digit +12
				if digit >= 24:
					digit -= 24
				s[0] = str(digit)
				timeSentence = ' '.join(s)
			timeDigits = takeDigitOnly.findall(timeSentence)
			if len(timeDigits) ==1:
				temp_timeSentence = timeDigits[0] + ":00:00"
			elif len(timeDigits) ==2:
				temp_timeSentence = timeDigits[0] +":" +timeDigits[1]+":00"
			else:
				temp_timeSentence = timeDigits[0] +":"+timeDigits[1]+":"+timeDigits[2]
			# print (temp_dateSentence+temp_timeSentence)
			date = parse(temp_dateSentence+temp_timeSentence)
		else:
			date = parse(temp_dateSentence+"00:00:00")
		return date

	def checkDate(self, sentence):
		token = os.getenv('TOKEN_KATA', None)
		parameters = {'m': sentence, 'api_token': token}
		r = requests.get('https://api.kata.ai/v1/insights', params = parameters)
		result = r.json()
		entities = result["entities"]
		# print (result)
		finalResult = None
		for entity in entities:
			if entity["entity"] == "DATE":
				 finalResult = entity["fragment"]
		return finalResult

	def processText(self,sentence):
		if (self.isCalled(sentence)):
			sentence = sentence.replace(":", " ")
			self.checkWhatCommand(sentence)
		else:
			#ngga dipanggil
			print("ngga dipanggil")

	def getJsonToSent(self):
		js = self.jsonToSend
		self.jsonToSend = None
		return js

# test = TextProcessor()
# # # test.processText("si bawel bikin jadwal kerja lembur tanggal 25/03/2017 jam 15.10")
#
# test.processText("si bawel bikin jadwal kerja lembur tanggal 30 April")
# tex = str(test.getJsonToSent())
# print(tex)
# test.processText("si bawel tambah pengeluaran makan ayam goreng bareng")
# tex = str(test.getJsonToSent())
# print(tex)
# print(test.checkDate("si bawel bikin jadwal hari jumat minggu ini"))
