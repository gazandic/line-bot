import requests


class GoogleMaps:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        self.params = {"query": "", "key": self.token}

    def searchLoc(self, query):
        self.params["query"] = query
        res = requests.get(self.base_url, params=self.params).json()

        try:
            geo = res['results'][0]['geometry']['location']
            return "{0},{1}".format(geo['lat'], geo['lng'])
        except (KeyError, IndexError):
            return None
