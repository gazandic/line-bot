from typing import Dict, Optional, Union

from datetime import datetime

JsonType = Dict[str, Optional[Union[int, str]]]


class JsonToQuery:
    @staticmethod
    def parse_json(json: JsonType) -> str:
        final_result = ""

        if json.get('error'):
            return str(json['error'])

        precommand = '/' + json['command'] + json['type']
        final_result += precommand
        data = json['data']
        if data.get('event_name'):
            nama = data['event_name']
            nama = nama.replace(" ", "_")
            final_result += ' '+nama

        if data.get('pengeluaran_name'):
            nama = data['pengeluaran_name']
            nama = nama.replace(" ", "_")
            final_result += ' '+nama

        if data.get('date'):
            tanggal = datetime.strptime(
                data['date'], "%Y-%m-%dT%H:%M:%S").strftime(" %d %m %Y %H %M")
            final_result += tanggal

        if data.get('persons'):
            personstring = ''
            for person in data['persons']:
                if 'bawel' not in person:
                    personstring = ' ' + person
                    break
            final_result += personstring

        if data.get('amount'):
            amount = ' '+data['amount']
            final_result += amount

        return final_result
