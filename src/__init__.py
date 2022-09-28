import os
from flask import Flask
from flask_cors import CORS #comment this on deployment
from src.api import api
from werkzeug.middleware.proxy_fix import ProxyFix
# from werkzeug.exceptions import BadRequest


# instantiate the extensions
def create_app():

    # instantiate the app
    app = Flask(__name__)
        
    # use cors to allow cross-origin requests
    CORS(app, resources={r"/*": {"origins": "*"}}, intercept_exceptions=False) #comment this on deployment

    app.wsgi_app = ProxyFix(app.wsgi_app) # fix for proxy issues - meaning that the proxy will not pass the X-Forwarded-For header to the backend

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    
    # register api
    api.init_app(app) 

    return app
