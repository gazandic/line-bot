from typing import Dict, Optional

import requests


class GoogleMaps:
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    def __init__(self, token):
        self.token = token

    def generate_payload(self, query: str) -> Dict[str, str]:
        return {"query": query, "key": self.token}

    def search_loc(self, query: str) -> Optional:
        res = requests.get(GoogleMaps.base_url, params=self.generate_payload(query)).json()

        try:
            geo = res['results'][0]['geometry']['location']
            return "{0},{1}".format(geo['lat'], geo['lng'])
        except (KeyError, IndexError):
            return None
