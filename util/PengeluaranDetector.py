#nyoba pytesseract
import re;
from ImageProcessor import ImageProcessor

class PengeluaranDetector(object):
	def __init__(self, imagePath):
		self.IP = ImageProcessor();
		self.imagePath = imagePath;

	def checkForTotal(self):
		totalCandidate= float();
		bersihinAngka = re.compile(r'([\.,]\d{2})\b');
		keyWordForTotal = ["jumlah","total","RP"] 
		if (self.IP.process_image(self.imagePath)):
			temp = self.IP.process_image(self.imagePath);
			lines = temp.splitlines();
			for line in lines:
				print(line);
				temp_spended = []
				for key in keyWordForTotal:
					searchSpended = re.compile(r'{0}\D*((\d[\.,]|\d)+)'.format(key), flags= re.IGNORECASE);	
					spended = searchSpended.findall(line);
					if (spended):
						for spent in spended:
							print(spent);
							spent = re.sub(r'([\.,]\d{2})\b','',spent[0]);
							spent = re.sub(r'([\.|,])', "", spent);
							print(spent);
							spent = float(spent);
							totalCandidate = spent;
						break;
			if totalCandidate == 0:
				searchSpended = re.compile(r'\D*((\d[\.,]|\d)+)', flags= re.IGNORECASE);
				spended = searchSpended.findall(line);
				if (spended):
					for spent in spended:
						print(spent);
						spent = re.sub(r'([\.,]\d{2})\b','',spent[0]);
						spent = re.sub(r'([\.|,])', "", spent);
						print(spent);
						spent = float(spent);
						totalCandidate = spent;
			print ("totalnya adalah: ", totalCandidate);

PD = PengeluaranDetector("106729.jpg");
PD.checkForTotal()
