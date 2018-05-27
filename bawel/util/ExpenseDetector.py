import re

from bawel.processor.ImageProcessor import ImageProcessor


class ExpenseDetector:

    @staticmethod
    def check_for_total(image_path: str) -> str:
        total_candidate = float(0)
        key_word_for_total = ["jumlah", "total"]
        get_by_key_word = False
        IP = ImageProcessor()
        if IP.process_image(image_path):
            temp = IP.process_image(image_path)
            lines = temp.splitlines()
            for line in lines:
                for key in key_word_for_total:
                    search_spended = re.compile(r'{0}\D*((\d[.,]|\d)+)'.format(key), flags=re.IGNORECASE)
                    spended = search_spended.findall(line)
                    if spended:
                        for spent in spended:
                            print(spent)
                            spent = re.sub(r'([.,]\d{2})\b', '', spent[0])
                            spent = re.sub(r'([.|,])', "", spent)
                            print(spent)
                            spent = float(spent)
                            if total_candidate < spent:
                                total_candidate = spent
                            if not get_by_key_word:
                                get_by_key_word = True
                        break
                if not get_by_key_word:
                    search_spended = re.compile(r'RP\D*((\d[.,]|\d)+)', flags=re.IGNORECASE)
                    spended = search_spended.findall(line)
                    if spended:
                        for spent in spended:
                            print(spent)
                            spent = re.sub(r'([.,]\d{2})\b', '', spent[0])
                            spent = re.sub(r'([.|,])', "", spent)
                            print(spent)
                            spent = float(spent)
                            if total_candidate < spent:
                                total_candidate = spent
            return str(total_candidate)
