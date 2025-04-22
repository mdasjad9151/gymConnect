from gymConnect.settings import GOOGLE_MAPS_API_KEY
import requests
API_KEY  = GOOGLE_MAPS_API_KEY

def get_lat_lon_from_address(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
   
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None