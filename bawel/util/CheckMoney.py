from typing import Optional

import re
import math


class CheckMoney(object):
    @staticmethod
    def process_text(sentence: str) -> Optional[float]:
        check_money_re = re.compile(r"((\d[\.,]|\d)+)", flags=re.IGNORECASE)
        money_l = check_money_re.findall(sentence)
        if money_l:
            money_s = re.sub(r'([\.,]\d{2})\b', '', str(money_l[0][0]))
            money_s = re.sub(r'([\.|,])', "", money_s)
            money = float(money_s)
            if math.floor(money) > 0:
                return money
            else:
                return None
        else:
            return None
