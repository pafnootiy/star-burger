import requests
from django.conf import settings
from location.models import Location
APIKEY = settings.YANDEX_API_KEY


def fetch_coordinates(address, apikey=APIKEY):
    url = 'https://geocode-maps.yandex.ru/1.x'
    params = {'geocode': address, 'apikey': apikey, 'format': 'json'}
    response = requests.get(url, params=params)
    response.raise_for_status()

    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lon, lat


def get_or_create_locations(*addresses):
    existing_locations = {
        location.address: (location.lat, location.lon)
        for location in Location.objects.filter(address__in=addresses)
    }

    for address in addresses:
        if address in existing_locations.keys():
            continue
        try:
            coordinates = fetch_coordinates(address)
        except Exception:
            continue

        coordinates = None, None
        lon, lat = coordinates
        location = Location.objects.create(
            address=address, lon=lon, lat=lon
        )
        existing_locations[location.address] = (location.lat, location.lon)
    return existing_locations
