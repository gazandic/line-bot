import re
import requests
import json
import os
import sys
from datetime import datetime
from dateutil.parser import parse
errorCreateUpdatePengeluaran = "coba lagi kak, coba tulis kaya gini 'si bawel tolong tambah/ubah pengeluaran makan siang untuk acara pergi ke jogja sebesar 50000 oleh gazandi' hehe"


class TextProcessor(object):
	def __init__(self):
		self.keyWordToCall  = "Si Bawel"
		self.keyWordToEvent = ["jadwal","event","acara"]
		self.keyWordPengeluaran = ["pengeluaran"]
		self.listActionDetection = ["untuk", "bagi", "buat"]
		self.listActionInEvent = {"lihat" : "lihat", "ganti" : "ubah", "buat":"tambah", "tambah":"tambah", "bikin":"tambah", "gajadi ikut":"gajadiikut","ga jadi ikut":"gajadiikut", "gak jadi ikut":"gajadiikut", "gak ikut":"gajadiikut", "ikut" : "ikut", "ubah":"ubah", "hapus":"hapus", "lapor":"report", "liat":"lihat", "report":"report", "eval":"report"}
		self.listActionInPengeluaran ={"lihat" : "lihat", "ganti" : "ubah", "buat":"tambah", "tambah":"tambah", "bikin":"tambah", "ubah":"ubah", "hapus":"hapus"}
		self.jsonToSend = None

    def isCalled(self, sentence):
        checkifCalled = re.compile(
            r'({0})'.format(
                self.keyWordToCall),
            flags=re.IGNORECASE)
        if checkifCalled.findall(sentence):
            return True
        else:
            return False

    def getCommands(self, sentence):
        getTheCommand = re.compile(
            r'{0}\b(.+)'.format(self.keyWordToCall), flags=re.IGNORECASE)
        if getTheCommand.findall(sentence):
            return(getTheCommand.findall(sentence))

    def checkPerson(self, sentence):
        sentence = sentence.replace("si bawel ", "")
        token = os.getenv('TOKEN_KATA', None)
        parameters = {'m': sentence, 'api_token': token}
        r = requests.get('https://api.kata.ai/v1/insights', params=parameters)
        result = r.json()
        entities = result["entities"]
        finalResult = []
        for entity in entities:
            if entity["entity"] == "PERSON":
                finalResult.append(entity["fragment"])
        return finalResult

    def checkAmount(self, sentence):
        keywordAmount = ["sebesar"]
        for key in keywordAmount:
            getAmount = re.compile(r'{0}\s*(\d+\.+\d+|\d+).*'.format(key))
            if (getAmount.findall(sentence)):
                return getAmount.findall(sentence)[0]
            else:
                return None

	# def json_serial(self,obj):
	# 	if isinstance(obj,datetime):
	# 		serial = obj.isoformat()
	# 		return serial
	# 	raise TypeError("Type not serializable")

	def checkActionPengeluaran(self, sentence, pengeluaranKey):
		for action in self.listActionInPengeluaran:
			isContain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
			persons = self.checkPerson(sentence)
			if isContain.findall(sentence):
				if action in ["buat", "tambah", "bikin"]:
					if self.checkAmount(sentence):
						amount = self.checkAmount(sentence)
						try:
							event_name , pengeluaran_name = None, None
							for eventkey in self.keyWordToEvent:
								for actiondetection in self.listActionDetection:
									kataKunciEvent = actiondetection + " "+ eventkey
									pengeluaran_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(pengeluaranKey, kataKunciEvent))

									event_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(kataKunciEvent, "sebesar"), flags=re.IGNORECASE)
									if (event_nameRe.findall(sentence) and pengeluaran_nameRe.findall(sentence)):
										event_name = event_nameRe.findall(sentence)[0]
										pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
										break
							self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'data':{'amount': amount,'event_name': event_name, 'pengeluaran_name': pengeluaran_name, 'persons':persons}}
						except:
							self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'error':errorCreateUpdatePengeluaran,'data':{}}
						break
					else:
						if persons:
							try:
								for eventkey in self.keyWordToEvent:
									for actiondetection in self.listActionDetection:
										kataKunciEvent = actiondetection + " "+ eventkey
										pengeluaran_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(pengeluaranKey, kataKunciEvent))

										event_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(kataKunciEvent, "oleh"), flags=re.IGNORECASE)
										if (event_nameRe.findall(sentence) and pengeluaran_nameRe.findall(sentence)):
											event_name = event_nameRe.findall(sentence)[0]
											pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
											break
								self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'data':{'amount': '-1','event_name': event_name, 'pengeluaran_name': pengeluaran_name, 'persons':persons}}
							except:
								print(sys.exc_info())
								self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'error':errorCreateUpdatePengeluaran,'data':{}}
						else:
							self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'error':errorCreateUpdatePengeluaran,'data':{}}
					break
				elif action in ["ubah", "ganti"]:
					amount = self.checkAmount(sentence)
					person = self.checkPerson(sentence)
					if amount and person :
						try:
							for eventkey in self.keyWordToEvent:
								for actiondetection in self.listActionDetection:
									kataKunciEvent = actiondetection + " "+ eventkey
									pengeluaran_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(pengeluaranKey, kataKunciEvent))

									event_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(kataKunciEvent, "seberapa"), flags=re.IGNORECASE)
									if (event_nameRe.findall(sentence) and pengeluaran_nameRe.findall(sentence)):
										event_name = event_nameRe.findall(sentence)[0]
										pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
										break
							self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'data':{'amount': amount,'event_name': event_name, 'pengeluaran_name':pengeluaran_name, 'persons':person}}
						except:
							self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'error':errorCreateUpdatePengeluaran,'data':{}}
					# elif person != None:
					# 	pengeluaran_nameRe = re.compile(r'{0}\s+(.*)\s+{1}'.format(pengeluaranKey, "oleh"), flags=re.IGNORECASE)
					# 	pengeluaran_name = 'unknown'
					# 	if (pengeluaran_nameRe.findall(sentence)):
					# 		pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
					# 		self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'data':{'persons': person,'event_name': pengeluaran_name}}
					# 	else:
					# 		self.jsonToSend = {'type': 'pengeluaran', 'command': action,'error':'unknown input'}
					# 	break
					else:
						self.jsonToSend = {'type': 'pengeluaran', 'command': action, 'error':errorCreateUpdatePengeluaran,'data':{}}
					break
				else:
					try:
						if not action in ["hapus"]:
							raise ValueError
						for eventkey in self.keyWordToEvent:
							for actiondetection in self.listActionDetection:
								kataKunciEvent = actiondetection + " "+ eventkey
								pengeluaran_nameRe = re.compile(r'{0}\s+(.+)\s+{1}'.format(pengeluaranKey, kataKunciEvent))

								event_nameRe = re.compile(r'{0}\s+(.+)'.format(kataKunciEvent), flags=re.IGNORECASE)
								if (event_nameRe.findall(sentence) and pengeluaran_nameRe.findall(sentence)):
									event_name = event_nameRe.findall(sentence)[0]
									pengeluaran_name = pengeluaran_nameRe.findall(sentence)[0]
									break
						self.jsonToSend = {'type': u'pengeluaran', 'command': action, 'data':{'event_name': event_name, 'pengeluaran_name':pengeluaran_name}}
					except:
						try :
							event_nameRe = re.compile(r'{0}\s(.+)'.format(pengeluaranKey))
							event_name = event_nameRe.findall(sentence)[0]
							self.jsonToSend = {'type': u'pengeluaran', 'command': action, 'data':{'event_name': event_name}}
						except:
							self.jsonToSend = {'type': u'pengeluaran', 'command': action, 'data':{}}

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
				try:
					if action in ["buat", "tambah", "bikin", "ubah", "ganti"]:
						event_nameRe = re.compile(r'{0}\s(.+)\s{1}'.format(eventKey, "tanggal"), flags=re.IGNORECASE)
						event_name = event_nameRe.findall(sentence)[0]
						self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'data':{'date': datetypedate,'event_name': event_name}}
						break
					else:
						if action in ["ikut", "gajadiikut", "gak ikut", "ga jadi ikut", "gajadi ikut","gak jadi ikut"]:
							persons = self.checkPerson(sentence)
							if persons :
								print(sentence)
								try:
									event_nameRe = re.compile(r'{0}\s+(.*)\s+{1}'.format(eventKey, "oleh"), flags=re.IGNORECASE)
									event_name = event_nameRe.findall(sentence)[0]
								except:
									event_nameRe = re.compile(r'{0}\s(.+)\s'.format(eventKey), flags=re.IGNORECASE)
									event_name = event_nameRe.findall(sentence)[0]
								self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'data':{'event_name': event_name, 'persons': persons}}
								break
							else:
								event_nameRe = re.compile(r'{0}\s(.+)\s'.format(eventKey), flags=re.IGNORECASE)
								event_name = event_nameRe.findall(sentence)[0]
								self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'error': ['no persons'],  'data':{'event_name': event_name}}
								break
						elif action in ["lihat","liat"]:
							self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'data':{}}
							break
						else:
							try:
								event_nameRe = re.compile(r'{0}\s(.+)'.format(eventKey), flags=re.IGNORECASE)
								event_name = event_nameRe.findall(sentence)[0]
								self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'data':{'event_name': event_name}}
							except:
								self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action], 'data':{}}
							break
				except:
					print(sys.exc_info())
					self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action] , 'error':'unknown input'}
					break
			else:
				self.jsonToSend = {'type': 'jadwal', 'error':'unknown input'}

	def checkTanggal(self, sentence):
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
			return datetypedate
		return {'error':'no date'}

    def checkWhatCommand(self, sentence):
        if (self.getCommands(sentence)):
            for command in self.getCommands(sentence):
                for key in self.keyWordPengeluaran:
                    isContain = re.compile(
                        r'\b({0})\b'.format(key), flags=re.IGNORECASE)
                    if (isContain.findall(sentence)):
                        self.checkActionPengeluaran(sentence, key)
            if (self.jsonToSend is None):
                for key in self.keyWordToEvent:
                    isContain = re.compile(
                        r'\b({0})\b'.format(key), flags=re.IGNORECASE)
                    if (isContain.findall(sentence)):
                        self.checkActionEvent(sentence, key)
            if self.jsonToSend is None:
                self.jsonToSend = {'error': 'unknown input'}
        else:
            self.jsonToSend = {'error': 'unknown input'}

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
		print(dateSentence)
		digits = takeDigitOnly.findall(dateSentence)
		print(digits)
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
			print (temp_dateSentence+temp_timeSentence)
			datestr = temp_dateSentence+temp_timeSentence
		else:
			datestr = temp_dateSentence+"00:00:00"
		date = str(datetime.strptime(datestr,"%d %m %Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"))
		return date

    def checkDate(self, sentence):
        token = os.getenv('TOKEN_KATA', None)
        parameters = {'m': sentence, 'api_token': token}
        r = requests.get('https://api.kata.ai/v1/insights', params=parameters)
        result = r.json()
        entities = result["entities"]
        # print (result)
        finalResult = None
        for entity in entities:
            if entity["entity"] == "DATE":
                finalResult = entity["fragment"]
        return finalResult

    def checkEntity(self, sentence):
        token = os.getenv('TOKEN_KATA', None)
        parameters = {'m': sentence, 'api_token': token}
        r = requests.get('https://api.kata.ai/v1/insights', params=parameters)
        result = r.json()
        entities = result["entities"]
        # print (result)
        finalResult = []
        for entity in entities:
            # if entity["entity"] == "DATE":
            finalResult.append(entity["fragment"])
        return finalResult

    def processText(self, sentence):
        sentence = sentence.replace(":", " ")
        sentence = sentence.replace("-", " ")
        sentence = sentence.replace(".", " ")
        sentence = sentence.replace(",", " ")
        if (self.isCalled(sentence)):
            self.checkWhatCommand(sentence)
        else:
            self.jsonToSend = {'error': 'unknown input'}

    def getJsonToSent(self):
        js = self.jsonToSend
        self.jsonToSend = None
        return js

TextProcessor().checkEntity("Besok pergi ke bec")