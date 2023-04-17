import requests
from django.conf import settings
from .models import Location
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
    existed_locations = {
        location.address: (location.lat, location.lon)
        for location in Location.objects.filter(address__in=addresses)
    }
    for address in addresses:
        if address in existed_locations.keys():
            continue
        coordinates = fetch_coordinates(address)
        if not coordinates:
            continue
        lon, lat = coordinates
        location = Location.objects.create(
            address=address, lon=lon, lat=lon
        )
        existed_locations[location.address] = (location.lat, location.lon)
    return existed_locations
