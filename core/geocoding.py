import typing
from pprint import pprint

import requests


def geocode(name, countries=('il', 'ps')) -> typing.List[
    typing.Dict[str, typing.Any]]:
    params = {
        'q': name,
        'format': 'json',
        'limit': 25,
        'extratags': 1,
        'addressdetails': 1,
        'namedetails': 1,
        'countrycodes': ",".join(countries),

    }
    r = requests.get("https://nominatim.openstreetmap.org/search", params)
    r.raise_for_status()
    return r.json()


def lookup(osm_type, osm_id) -> typing.Dict[str, typing.Any]:
    params = {
        'osm_ids': f"{osm_type[0].upper()}{osm_id}",
        'format': 'json',
        'extratags': 1,
        'addressdetails': 1,
        'namedetails': 1,
    }
    r = requests.get("https://nominatim.openstreetmap.org/lookup", params)
    r.raise_for_status()
    return r.json()


pprint(lookup("relation", 6502363))
# pprint(lookup("way", 315867542))
# pprint(geocode("jerusalem"))
# pprint(geocode("שכם"))
