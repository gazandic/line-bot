from datetime import datetime

class JsonToQuery():
    def __init__(self, _json):
        self.json = _json


    def parseJSON(self):
        obj = self.json
        finalResult = ""
        print (obj)
        if obj.get('error'):
            return str(obj['error'])
        precommand = '/'+obj['command']+obj['type']
        finalResult += precommand
        data = obj['data']
        nama = data['event_name']
        nama = nama.replace(" ", "_")
        finalResult += ' '+nama
        if data.get('date'):
            tanggal = datetime.strptime(data['date'],"%Y-%m-%dT%H:%M:%S").strftime(" %d %m %Y %H %M")
            finalResult += tanggal
        elif data.get('amount'):
            amount = ' '+data['amount']
            finalResult += amount
        if data.get('persons'):
            personstring = ''
            for person in data['persons']:
                if not 'bawel' in person:
                    personstring = ' '+person
                    break
            finalResult += personstring
        print(finalResult)
        return finalResult
