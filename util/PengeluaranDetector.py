#nyoba pytesseract
import re;
from ImageProcessor import ImageProcessor;

class PengeluaranDetector(object):
	def __init__(self, imagePath):
		self.IP = ImageProcessor();
		self.imagePath = imagePath;

	def checkForTotal(self):
		totalCandidate= float(0);
		bersihinAngka = re.compile(r'([\.,]\d{2})\b');
		keyWordForTotal = ["jumlah","total"] 
		getByKeyWord = False;
		if (self.IP.process_image(self.imagePath)):
			temp = self.IP.process_image(self.imagePath);
			lines = temp.splitlines();
			totalCandidate =0;
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
							if (totalCandidate < spent) :
								totalCandidate = spent;
							if (not getByKeyWord):
								getByKeyWord = True;
						break;
				if not getByKeyWord:
					searchSpended = re.compile(r'RP\D*((\d[\.,]|\d)+)', flags= re.IGNORECASE);
					spended = searchSpended.findall(line);
					print(spended);
					if (spended):
						for spent in spended:
							print(spent);
							spent = re.sub(r'([\.,]\d{2})\b','',spent[0]);
							spent = re.sub(r'([\.|,])', "", spent);
							print(spent);
							spent = float(spent);
							if totalCandidate < spent :
								totalCandidate = spent;
			print ("totalnya adalah: ", totalCandidate);

PD= PengeluaranDetector("contohgaz.jpg");
PD.checkForTotal();
