import requests
import urllib3
from flask import Flask, redirect, request, url_for


from app.auth import bp
from config import Strava_auth


@bp.route('/')
def index():
    return 'This is The auth Blueprint'

@bp.route('/strava')
def strava(config_class=Strava_auth):
  args = request.args

  # checks for query string needed on the redirect back
  if args:
    refresh_token = args['params']


  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  # URLs to request auth
  strava_auth_url = 'https://www.strava.com/oauth/token'
  activities_url = 'https://www.strava.com/api/v3/athlete/activities'
  profile_url = 'https://www.strava.com/api/v3/athlete'

  try:  
    # Strava auth payload (POST request)
    # uses refresh token to get access token
    payload = {
      'client_id': config_class.STRAVA_CLIENT_ID,
      'client_secret': config_class.STRAVA_CLIENT_SECERT,
      'refresh_token': config_class.STRAVA_REFRESH_TOKEN or refresh_token,
      'grant_type': 'refresh_token',
      'f': 'json'
    }

    # POST request to get your access token 
    res = requests.post(strava_auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    # Using fetched access token use to get user profile and activities
    header = {'Authorization': 'Bearer ' + access_token}
    # see Strava documentation on param usage
    param = {
      'per_page': 10,
      'page': 1
    }
    my_activities = requests.get(activities_url, headers=header, params=param).json()

    my_profile = requests.get(profile_url, headers=header).json()

    return {
      'profile': my_profile,
      'activities': my_activities
    }

  except:
    # for new users or users that do not have a refresh token
    strava_authorize_url = 'https://www.strava.com/oauth/authorize'
    client_id = config_class.STRAVA_CLIENT_ID
    redirect_uri = 'http://localhost:8080/auth/stravareturn'
    response_type = 'code'
    scope = 'activity:read_all'
    
    return redirect(f'{strava_authorize_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&scope={scope}') 


@bp.route('/stravareturn')
def strava_return(config_class=Strava_auth):
  # Retieve the access code from the redirect page from Strava
  args = request.args

  client_id = config_class.STRAVA_CLIENT_ID
  client_secret = config_class.STRAVA_CLIENT_SECERT
  grant_type = 'authorization_code'
  
  # url request to get the refresh token
  url = f'https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={args["code"]}&grant_type={grant_type}'

  response = requests.request("POST", url).json()

  return redirect(url_for('auth.strava', param=response['refresh_token']))
