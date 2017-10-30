import requests


class Kata:
    def __init__(self, token_kata):
        self.parameters = {'m': '', 'api_token': token_kata}

    def getEntities(self, sentence):
        self.parameters['m'] = self.preprocess(sentence)
        r = requests.get('https://api.kata.ai/v1/insights', params=self.parameters)
        result = r.json()
        return result["entities"]

    def preprocess(self, sentence):
        return sentence.lower().replace("si bawel", "")
