from app.auth import bp

@bp.route('/')
def auth():
    return 'This is The auth Blueprint'

@bp.route('/strava')
def strava():
  from app.auth import strava as strava_auth
  strava_auth()
  return 'Strava Auth'