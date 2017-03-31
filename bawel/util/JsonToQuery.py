from datetime import datetime


class JsonToQuery():
    def __init__(self, _json):
        self.json = _json

    def parseJSON(self):
        obj = self.json
        finalResult = ""
        print(obj)
        if obj.get('error'):
            return str(obj['error'])
        precommand = '/' + obj['command'] + obj['type']
        finalResult += precommand
        data = obj['data']
        if data.get('event_name'):
            nama = data['event_name']
            nama = nama.replace(" ", "_")
            finalResult += ' '+nama

        if data.get('pengeluaran_name'):
            nama = data['pengeluaran_name']
            nama = nama.replace(" ", "_")
            finalResult += ' '+nama

        if data.get('date'):
            tanggal = datetime.strptime(
                data['date'], "%Y-%m-%dT%H:%M:%S").strftime(" %d %m %Y %H %M")
            finalResult += tanggal

        if data.get('persons'):
            personstring = ''
            for person in data['persons']:
                if 'bawel' not in person:
                    personstring = ' ' + person
                    break
            finalResult += personstring

        if data.get('amount'):
            amount = ' '+data['amount']
            finalResult += amount
        print(finalResult)
        return finalResult
