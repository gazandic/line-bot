from bawel.util.TextProcessor import TextProcessor
import json
from datetime import datetime
class JsonToQuery():
    def __init__(self, _json):
        self.json = _json

    def parseJSON(self):
        obj = json.loads(self.json)
        finalResult = ""
        if obj.get('error'):
            print (obj['error'])
            return 0
        precommand = obj['command']+obj['type']
        finalResult += precommand
        data = obj['data']
        nama = data['event_name']
        print(data)
        nama = nama.replace(" ", "_")
        finalResult += ' '+nama
        if data.get('date'):
            tanggal = datetime.strptime(data['date'],"%Y-%m-%dT%H:%M:%S").strftime(" %d %m %Y %H %M")
            finalResult += tanggal
        elif data.get('amount'):
            amount = ' '+data['amount']
            finalResult += amount
        print(finalResult)


test = TextProcessor()
st = "tambah pengeluaran kerja lembur sebesar 10000"
print (st)
test.processText(st)
jtq = JsonToQuery(test.getJsonToSent())
jtq.parseJSON()
