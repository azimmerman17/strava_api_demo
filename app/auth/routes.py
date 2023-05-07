import requests
import urllib3
from flask import Flask


from app.auth import bp
from config import Strava_auth


@bp.route('/')
def auth():
    return 'This is The auth Blueprint'

@bp.route('/strava')
def strava(config_class=Strava_auth):
  route = Flask(__name__)
  route.config.from_object(config_class)

  print(config_class)

  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  
  # URLs to request auth
  strava_auth_url = 'https://www.strava.com/oauth/token'
  activites_url = 'https://www.strava.com/api/v3/athlete/activities'
  profile_url = 'https://www.strava.com/api/v3/athlete'

  # Strava auth payload (POST request)
  # uses refresh token to get access token
  payload = {
    'client_id': config_class.STRAVA_CLIENT_ID,
    'client_secret': config_class.STRAVA_CLIENT_SECERT,
    'refresh_token': config_class.STRAVA_REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
  }

  print("Requesting Token...\n")
  res = requests.post(strava_auth_url, data=payload, verify=False)
  access_token = res.json()['access_token']
  print("Access Token = {}\n".format(access_token))

  header = {'Authorization': 'Bearer ' + access_token}
  param = {'per_page': 10, 'page': 1}
  my_dataset = requests.get(activites_url, headers=header, params=param).json()
  print(my_dataset)

  my_profile = requests.get(profile_url, headers=header).json()

  return {
    'profile': my_profile,
    'activites': my_dataset
  }