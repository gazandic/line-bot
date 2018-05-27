# from typing import I

import requests


class Kata:
    def __init__(self, token_kata):
        self.parameters = {'m': '', 'api_token': token_kata}

    def get_entities(self, sentence: str):
        self.parameters['m'] = Kata.preprocess(sentence)
        r = requests.get('https://api.kata.ai/v1/insights', params=self.parameters)
        result = r.json()
        return result["entities"]

    @staticmethod
    def preprocess(sentence: str) -> str:
        return sentence.lower().replace("si bawel", "")
