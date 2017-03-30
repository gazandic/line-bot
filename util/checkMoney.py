import re;
import math;

class checkMoney(object):
	def processText(self, sentence):
		checkMoneyRe = re.compile(r"((\d[\.,]|\d)+)", flags= re.IGNORECASE);
		moneyL = checkMoneyRe.findall(sentence);
		if (moneyL):
			moneyS = re.sub(r'([\.,]\d{2})\b','',str(moneyL[0][0]));
			moneyS = re.sub(r'([\.|,])', "", moneyS);
			money = float(moneyS);
			if math.floor(money) > 0:
				return money;
			else:
				return None;
		else:
			return None;