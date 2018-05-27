import re
import sys
from datetime import datetime

from dateutil.parser import parse

from bawel.client.Kata import Kata

errorCreateUpdatePengeluaran = "coba lagi kak, coba tulis mirip gini kak 'si bawel tolong tambah/ubah pengeluaran " \
                               "<makan siang>(nama_pengeluaran) untuk acara <pergi ke jogja>(nama_acara) sebesar " \
                               "50000 oleh Kevin' hehe "
errorCreateUpdateJadwal = "coba lagi kak, coba tulis mirip gini kak 'si bawel tolong tambah/ubah jadwal pergi ke " \
                          "jogja tanggal 5 April jam 3:50 sore' yaaa "
errorIkutOrangJadwal = "siapa yang ikut kak ? coba tulis mirip gini kak 'si bawel tolong ikut acara pergi ke jogja " \
                       "oleh Kevin' hehehe "
errorIkutJadwal = "kaya gini kak 'si bawel tolong ikut acara pergi ke jogja oleh Kevin' hehe"
errorLiatJadwal = "coba tulis mirip gini kak 'si bawel lihat acara'"
errorHapusJadwal = "tolong tulis mirip gini ya kak 'si bawel hapus acara pergi ke jogja'"
errorJadwal = "ketik /jadwal ya kak"
errorPengeluaran = "ketik /pengeluaran ya kak"
errorUnknownInput = "bawel ga paham :( ketik 'si bawel tolong' atau '/help' ya kaak buat pake si bawel"


class TextProcessor(object):
    keyWordToCall = "Si Bawel"
    keyWordToEvent = ["jadwal", "event", "acara"]
    keyWordPengeluaran = ["pengeluaran"]
    listActionDetection = ["untuk", "bagi", "buat"]
    listActionInEvent = {"lihat": "lihat", "ganti": "ubah", "buat": "tambah", "tambah": "tambah",
                         "bikin": "tambah", "gajadi ikut": "gajadiikut", "gajadiikut": "gajadiikut",
                         "ga jadi ikut": "gajadiikut", "gak jadi ikut": "gajadiikut", "gak ikut": "gajadiikut",
                         "ikut": "ikut", "ubah": "ubah", "hapus": "hapus", "lapor": "report", "liat": "lihat",
                         "report": "report", "eval": "report", "batal": "gajadiikut", "ga ikut": "gajadiikut",
                         "batal ikut": "gajadiikut"}
    listActionInPengeluaran = {"lihat": "lihat", "ganti": "ubah", "buat": "tambah", "tambah": "tambah",
                               "bikin": "tambah", "ubah": "ubah", "hapus": "hapus", "lapor": "report",
                               "liat": "lihat", "report": "report", "eval": "report"}
    listErrorInEvent = {"lihat": errorLiatJadwal, "ikut": errorIkutJadwal, "hapus": errorHapusJadwal,
                        "ubah": errorCreateUpdateJadwal, "tambah": errorCreateUpdateJadwal}
    listErrorType = {"jadwal": errorJadwal, "pengeluaran": errorPengeluaran}

    def __init__(self, token_kata):
        self.jsonToSend = None
        self.kataClient = Kata(token_kata)

    def is_called(self, sentence):
        check_if_called = re.compile(
            r'({0})'.format(
                self.keyWordToCall),
            flags=re.IGNORECASE)
        return check_if_called.findall(sentence)

    def get_commands(self, sentence):
        get_the_command = re.compile(
            r'{0}\b(.+)'.format(self.keyWordToCall), flags=re.IGNORECASE)
        if get_the_command.findall(sentence):
            return get_the_command.findall(sentence)

    def check_person(self, sentence):
        entities = self.kataClient.get_entities(sentence)
        return list(
            map(lambda entity: entity["fragment"], filter(lambda entity: entity["entity"] == "PERSON", entities)))

    @staticmethod
    def check_amount(sentence):
        keyword_amount = ["sebesar"]
        for key in keyword_amount:
            get_amount = re.compile(r'{0}\s*(\d+\.+\d+|\d+).*'.format(key))
            if get_amount.findall(sentence):
                return get_amount.findall(sentence)[0]

        return None

    @staticmethod
    def json_serial(obj):
        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    def check_action_pengeluaran(self, sentence, expense_key):
        for action in self.listActionInPengeluaran:
            is_contain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
            if is_contain.findall(sentence):
                if action in ["buat", "tambah", "bikin"]:
                    persons = self.check_person(sentence)
                    amount = self.check_amount(sentence)
                    if amount:
                        try:
                            event_name, pengeluaran_name = None, None
                            for eventkey in self.keyWordToEvent:
                                for action_detection in self.listActionDetection:
                                    kata_kunci_event = action_detection + " " + eventkey
                                    pengeluaran_name_re = re.compile(
                                        r'{0}\s+(.+)\s+{1}'.format(expense_key, kata_kunci_event))

                                    event_name_re = re.compile(r'{0}\s+(.+)\s+{1}'.format(kata_kunci_event, "sebesar"),
                                                               flags=re.IGNORECASE)

                                    if event_name_re.findall(sentence) and pengeluaran_name_re.findall(sentence):
                                        event_name = event_name_re.findall(sentence)[0]
                                        pengeluaran_name = pengeluaran_name_re.findall(sentence)[0]
                                        break
                            self.jsonToSend = {'type': 'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                               'data': {'amount': amount, 'event_name': event_name,
                                                        'pengeluaran_name': pengeluaran_name, 'persons': persons}}
                        except:
                            self.jsonToSend = {'type': 'pengeluaran', 'command': action,
                                               'error': errorCreateUpdatePengeluaran, 'data': {}}
                        break
                    else:
                        if persons:
                            try:
                                for eventkey in self.keyWordToEvent:
                                    for action_detection in self.listActionDetection:
                                        kata_kunci_event = action_detection + " " + eventkey
                                        pengeluaran_name_re = re.compile(
                                            r'{0}\s+(.+)\s+{1}'.format(expense_key, kata_kunci_event))

                                        event_name_re = re.compile(r'{0}\s+(.+)\s+{1}'.format(kata_kunci_event, "oleh"),
                                                                   flags=re.IGNORECASE)

                                        if event_name_re.findall(sentence) and pengeluaran_name_re.findall(sentence):
                                            event_name = event_name_re.findall(sentence)[0]
                                            pengeluaran_name = pengeluaran_name_re.findall(sentence)[0]
                                            break
                                self.jsonToSend = {'type': 'pengeluaran',
                                                   'command': self.listActionInPengeluaran[action],
                                                   'data': {'amount': '-1', 'event_name': event_name,
                                                            'pengeluaran_name': pengeluaran_name, 'persons': persons}}
                            except:
                                print(sys.exc_info())
                                self.jsonToSend = {'type': 'pengeluaran', 'command': action,
                                                   'error': errorCreateUpdatePengeluaran, 'data': {}}
                        else:
                            self.jsonToSend = {'type': 'pengeluaran', 'command': action,
                                               'error': errorCreateUpdatePengeluaran, 'data': {}}
                        break
                elif action in ["ubah", "ganti"]:
                    amount = self.check_amount(sentence)
                    person = self.check_person(sentence)
                    if amount and person:
                        try:
                            for eventkey in self.keyWordToEvent:
                                for action_detection in self.listActionDetection:
                                    kata_kunci_event = action_detection + " " + eventkey
                                    pengeluaran_name_re = re.compile(
                                        r'{0}\s+(.+)\s+{1}'.format(expense_key, kata_kunci_event))

                                    event_name_re = re.compile(r'{0}\s+(.+)\s+{1}'.format(kata_kunci_event, "sebesar"),
                                                               flags=re.IGNORECASE)
                                    if (event_name_re.findall(sentence) and pengeluaran_name_re.findall(sentence)):
                                        event_name = event_name_re.findall(sentence)[0]
                                        pengeluaran_name = pengeluaran_name_re.findall(sentence)[0]
                                        break
                            self.jsonToSend = {'type': 'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                               'data': {'amount': amount, 'event_name': event_name,
                                                        'pengeluaran_name': pengeluaran_name, 'persons': person}}
                        except:
                            self.jsonToSend = {'type': 'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                               'error': errorCreateUpdatePengeluaran, 'data': {}}
                    else:
                        self.jsonToSend = {'type': 'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                           'error': errorCreateUpdatePengeluaran, 'data': {}}
                    break
                else:
                    try:
                        if not action in ["hapus"]:
                            raise ValueError
                        for eventkey in self.keyWordToEvent:
                            for action_detection in self.listActionDetection:
                                kata_kunci_event = action_detection + " " + eventkey
                                pengeluaran_name_re = re.compile(
                                    r'{0}\s+(.+)\s+{1}'.format(expense_key, kata_kunci_event))

                                event_name_re = re.compile(r'{0}\s+(.+)'.format(kata_kunci_event), flags=re.IGNORECASE)
                                if event_name_re.findall(sentence) and pengeluaran_name_re.findall(sentence):
                                    event_name = event_name_re.findall(sentence)[0]
                                    pengeluaran_name = pengeluaran_name_re.findall(sentence)[0]
                                    break
                        self.jsonToSend = {'type': u'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                           'data': {'event_name': event_name, 'pengeluaran_name': pengeluaran_name}}
                        break
                    except:
                        try:
                            event_name_re = re.compile(r'{0}\s(.+)'.format(expense_key))
                            event_name = event_name_re.findall(sentence)[0]
                            self.jsonToSend = {'type': u'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                               'data': {'event_name': event_name}}
                            break
                        except:
                            self.jsonToSend = {'type': u'pengeluaran', 'command': self.listActionInPengeluaran[action],
                                               'data': {}}
                            break

    def check_action_event(self, sentence, eventKey):
        keyTime = ["pukul", "jam"]
        temp_sentence = str(sentence)
        time_sentence = None

        for key in keyTime:
            find_time = re.compile(r'{0}\W(\d+.\d+.\w+|\d+.\w+)'.format(key, flags=re.IGNORECASE))
            time_found = find_time.findall(temp_sentence)
            if time_found:
                time_sentence = time_found[0]
                time_sentence_to_exclude = key + " " + time_sentence
                # print(timeSentenceToExclude)
                exclude_time_sentence = re.compile(r'{0}'.format(time_sentence_to_exclude))
                temp_sentence = exclude_time_sentence.sub('', temp_sentence)
                break

        for action in self.listActionInEvent:
            does_contain = re.compile(r'\b({0})\b'.format(action), flags=re.IGNORECASE)
            if does_contain.findall(temp_sentence):
                try:
                    if action in ["buat", "tambah", "bikin", "ubah", "ganti"]:
                        date_sentence = self.check_date(temp_sentence)
                        if date_sentence:
                            datetypedate = self.date_parser(date_sentence, time_sentence)
                        event_name_re = re.compile(r'{0}\s(.+)\s{1}'.format(eventKey, "tanggal"), flags=re.IGNORECASE)
                        event_name = event_name_re.findall(sentence)[0]
                        self.jsonToSend = {
                            'type': 'jadwal',
                            'command': self.listActionInEvent[action],
                            'data': {
                                'date': datetypedate,
                                'event_name': event_name
                            }
                        }
                        break
                    elif action in ["ga ikut", "batal ikut", "ikut", "gajadiikut", "gak ikut", "ga jadi ikut",
                                    "gajadi ikut", "gak jadi ikut", "batal"]:
                        for action2 in ["ga ikut", "batal ikut", "gajadiikut", "gak ikut", "ga jadi ikut",
                                        "gajadi ikut", "gak jadi ikut", "batal"]:
                            does_contain = re.compile(r'\b({0})\b'.format(action2), flags=re.IGNORECASE)
                            if does_contain.findall(temp_sentence):
                                action = action2
                                break

                        persons = self.check_person(sentence)
                        if persons:
                            print(sentence)
                            try:
                                event_name_re = re.compile(r'{0}\s+(.*)\s+{1}'.format(eventKey, "oleh"),
                                                           flags=re.IGNORECASE)
                                event_name = event_name_re.findall(sentence)[0]
                            except:
                                event_name_re = re.compile(r'{0}\s(.+)\s'.format(eventKey), flags=re.IGNORECASE)
                                event_name = event_name_re.findall(sentence)[0]
                            self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action],
                                               'data': {'event_name': event_name, 'persons': persons}}
                            break
                        else:
                            event_name_re = re.compile(r'{0}\s(.+)'.format(eventKey), flags=re.IGNORECASE)
                            event_name = event_name_re.findall(sentence)[0]
                            self.jsonToSend = {'type': 'jadwal', 'command': self.listActionInEvent[action],
                                               'error': errorIkutOrangJadwal, 'data': {'event_name': event_name}}
                            break
                    elif action in ["lihat", "liat"]:
                        self.jsonToSend = {
                            'type': 'jadwal',
                            'command': self.listActionInEvent[action],
                            'data': {}
                        }
                        break
                    else:
                        try:
                            event_name_re = re.compile(r'{0}\s(.+)'.format(eventKey), flags=re.IGNORECASE)
                            event_name = event_name_re.findall(sentence)[0]
                            self.jsonToSend = {
                                'type': 'jadwal', 'command': self.listActionInEvent[action],
                                'data': {
                                    'event_name': event_name
                                }
                            }
                        except:
                            self.jsonToSend = {
                                'type': 'jadwal',
                                'command': self.listActionInEvent[action],
                                'data': {}
                            }
                        break
                except:
                    print(sys.exc_info())
                    command = self.listActionInEvent[action]
                    self.jsonToSend = {
                        'type': 'jadwal',
                        'command': command,
                        'error': self.listErrorInEvent[command]
                    }
                    break
            else:
                self.jsonToSend = {
                    'type': 'jadwal',
                    'error': self.listErrorType['jadwal']
                }

    def check_tanggal(self, sentence):
        key_time = ["pukul", "jam"]
        temp_sentence = str(sentence)
        time_sentence = None
        for key in key_time:
            find_time = re.compile(r'{0}\W(\d+.\d+.\w+|\d+.\w+)'.format(key, ))
            time_found = find_time.findall(temp_sentence)
            if time_found:
                time_sentence = time_found[0]
                time_sentence_to_exclude = key + " " + time_sentence
                # print(timeSentenceToExclude)
                exclude_time_sentence = re.compile(r'{0}'.format(time_sentence_to_exclude))
                temp_sentence = exclude_time_sentence.sub('', temp_sentence)
                break
        date_sentence = self.check_date(temp_sentence)
        if date_sentence:
            date_type_date = self.date_parser(date_sentence, time_sentence)
            return date_type_date
        return {'error': 'no date'}

    def check_what_command(self, sentence):
        if self.get_commands(sentence):
            for command in self.get_commands(sentence):
                for key in self.keyWordPengeluaran:
                    does_contain = re.compile(r'\b({0})\b'.format(key), flags=re.IGNORECASE)
                    if does_contain.findall(sentence):
                        self.check_action_pengeluaran(sentence, key)
            if self.jsonToSend is None:
                for key in self.keyWordToEvent:
                    does_contain = re.compile(r'\b({0})\b'.format(key), flags=re.IGNORECASE)
                    if does_contain.findall(sentence):
                        self.check_action_event(sentence, key)
            if self.jsonToSend is None:
                self.jsonToSend = {'error': errorUnknownInput}
        else:
            self.jsonToSend = {'error': errorUnknownInput}

    @staticmethod
    def date_parser(date_sentence, time_sentence):
        bulan_detected = False
        year_detected = False
        now = datetime.now()
        month_name_to_number = {
            "januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7,
            "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12
        }
        for monthname in month_name_to_number:
            if re.compile(r'\b({0})\b'.format(monthname), flags=re.IGNORECASE):
                bulan_detected = True
                date_sentence = re.sub(monthname, str(month_name_to_number[monthname]), date_sentence,
                                       flags=re.IGNORECASE)
        digitSplit = re.compile(r'\W+(\d+)')
        take_digit_only = re.compile(r'\b(\d+)\b')
        print(date_sentence)
        digits = take_digit_only.findall(date_sentence)
        print(digits)
        temp_date_sentence = ""
        for digit in digits:
            if int(digit) > 31:
                year_detected = True
            temp_date_sentence = temp_date_sentence + str(digit) + " "
        if len(digits) > 2:
            date = parse(temp_date_sentence)
        elif len(digits) == 2:
            if bulan_detected:
                if not year_detected:
                    temp_date_sentence = temp_date_sentence + str(now.year) + " "
                else:
                    temp_date_sentence = "1 " + temp_date_sentence
                    # nanya tanggal
            else:
                if int(digits[1]) <= 12:
                    bulan_detected = True
                if bulan_detected:
                    temp_date_sentence = temp_date_sentence + str(now.year) + " "
        else:  # cuman 1 digit
            if year_detected:
                temp_date_sentence = "1 " + "1 " + temp_date_sentence
                # nanya tanggal dan bulan
            elif bulan_detected:
                temp_date_sentence = "1 " + temp_date_sentence + str(now.year) + " "
                # nanya tanggal, tahun asumsi tahun ini
            else:  # asumsi ngasih tangga doang ini
                temp_date_sentence = temp_date_sentence + " " + str(now.month) + " " + str(now.year) + " "

        # print (temp_dateSentence)
        if time_sentence:
            keterangan_waktu = ["siang", "sore"]
            temp_time_sentence = ""
            s = time_sentence.split()
            digit = int(s[0])
            if s[len(s) - 1] == "malam" and digit <= 12 and digit >= 6 or s[
                len(s) - 1] in keterangan_waktu and digit <= 7:
                digit = digit + 12
                if digit >= 24:
                    digit -= 24
                s[0] = str(digit)
                time_sentence = ' '.join(s)
            time_digits = take_digit_only.findall(time_sentence)
            if len(time_digits) == 1:
                temp_time_sentence = time_digits[0] + ":00:00"
            elif len(time_digits) == 2:
                temp_time_sentence = time_digits[0] + ":" + time_digits[1] + ":00"
            else:
                temp_time_sentence = time_digits[0] + ":" + time_digits[1] + ":" + time_digits[2]
            print(temp_date_sentence + temp_time_sentence)
            date_str = temp_date_sentence + temp_time_sentence
        else:
            date_str = temp_date_sentence + "00:00:00"
        date = str(datetime.strptime(date_str, "%d %m %Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S"))
        return date

    def check_date(self, sentence):
        entities = self.kataClient.get_entities(sentence)
        return \
            list(map(lambda entity: entity["fragment"], filter(lambda entity: entity["entity"] == "DATE", entities)))[0]

    def process_text(self, sentence):
        sentence = sentence.replace(":", " ")
        sentence = sentence.replace("-", " ")
        sentence = sentence.replace(".", " ")
        sentence = sentence.replace(",", " ")
        if self.is_called(sentence):
            self.check_what_command(sentence)
        else:
            self.jsonToSend = {'error': errorUnknownInput}

    def get_entities(self, text):
        return self.kataClient.get_entities(text)

    def get_json_to_sent(self):
        js = self.jsonToSend
        self.jsonToSend = None
        return js
