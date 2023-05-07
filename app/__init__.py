from flask import Flask

from config import Config

def create_app():
  app = Flask(__name__)
  # app.config.from_object(config_class)

  # Initialize Flask extensions here




  # migrate models
  # This Demo witl have no models

  # Register blueprints here
  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  @app.route('/test/')
  def test_page():
    return '<h1>Testing the Flask Application Factory Pattern</h1>'

  @app.route('/<path:path>')
  def catch_all(path):
    return 'Page not found'
      
  return app