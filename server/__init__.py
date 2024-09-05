import os
from flask import session
from flask import Flask, redirect, render_template
from flask import Blueprint
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this is life'
    
    @app.route('/')
    def index():
        if 'access_token' in session:
            if datetime.now().timestamp() < session['expires_at']:
               return render_template('home.html') 

        return render_template('index.html')

    @app.route('/pages')
    def pages():
        return render_template('redirect.html')
    
    from .auth import auth
    from .top import top
    from .recent import recent
    from .playlist import playlist
    from .region_avail import region
    from .account import account
    
    app.register_blueprint(auth, url_prefix='/') 
    app.register_blueprint(top, url_prefix='/top')
    app.register_blueprint(recent, url_prefix='/')
    app.register_blueprint(playlist, url_prefix='/')
    app.register_blueprint(region, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')
    
    return app 