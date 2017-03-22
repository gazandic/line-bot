#nyoba pytesseract
import re;
from ImageProcessor import ImageProcessor

class PengeluaranDetector(object):
	def __init__(self, imagePath):
		self.IP = ImageProcessor();
		self.imagePath = imagePath;

	def checkForTotal(self):
		totalCandidate= float();
		if (self.IP.process_image(self.imagePath)):
			temp = self.IP.process_image(self.imagePath);
			lines = temp.splitlines();
			for line in lines:
				print(line);
				searchSpended = re.compile(r'Rp.(\d+\.+\d+|\d+).*');
				spended = searchSpended.findall(line);
				if (spended):
					for spent in spended:
						spent = float(spent);
					print(spended);
					totalCandidate = max(spended);
			print totalCandidate;

PD = PengeluaranDetector("C:\\Users\\Kevin Yauris\\Documents\\Oppurtinity\\line-bot\\testingStructure.png");
PD.checkForTotal();
