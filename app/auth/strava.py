import requests
import urllib3

from app import config_vars


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def strava_auth(config_vars=config_vars):
  print(config_vars)
  # URLs to request auth
  strava_auth_url= auth_url = 'https://www.strava.com/oauth/token'
  activites_url = 'https://www.strava.com/api/v3/athlete/activities'

  # # Strava auth payload (POST request)
  # # uses refresh token to get access token
  # payload = {
  #   'client_id': 'STRAVA_CLIENT_ID',
  #   'client_secret': 'STRAVA_CLIENT_SECERT',
  #   'refresh_token': 'STRAVA_REFRESH_TOKEN',
  #   'grant_type': "refresh_token",
  #   'f': 'json'
  # }

  # print("Requesting Token...\n")
  # res = requests.post(auth_url, data=payload, verify=False)
  # access_token = res.json()['access_token']
  # print("Access Token = {}\n".format(access_token))

  # header = {'Authorization': 'Bearer ' + access_token}
  # param = {'per_page': 200, 'page': 1}
  # my_dataset = requests.get(activites_url, headers=header, params=param).json()

  # print(my_dataset[0]["name"])
  # print(my_dataset[0]["map"]["summary_polyline"])

  


