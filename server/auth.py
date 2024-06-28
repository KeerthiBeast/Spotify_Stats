import os
import requests
from dotenv import load_dotenv, dotenv_values
import urllib.parse
import json

from flask import Blueprint
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, render_template

auth = Blueprint('auth', __name__)
load_dotenv()

@auth.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played playlist-modify-public playlist-modify-private'
    params = {
        'client_id': os.getenv('CLIENT_ID'),
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': os.getenv('REDIRECT_URL'), 
        'show_dialog': True
    }
    
    auth_url = f"{os.getenv('AUTH_URL')}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@auth.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': os.getenv('REDIRECT_URL'), 
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET')
        }
        
        response = requests.post(os.getenv('TOKEN_URL'), data=req_body)
        response.raise_for_status()

        token_info = response.json()
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        userid = f"{os.getenv('API_BASE_URL')}me"
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }

        response = requests.get(userid, headers=headers)
        response.raise_for_status()

        userid_json = response.json()
        session['id'] = userid_json['id']
        session['display_name'] = userid_json['display_name']
        session['profile_pic'] = userid_json['images'][1]['url']
        session['product'] = userid_json['product']

        if(session['product'] == 'premium'):
            session['product'] = 'Premium'
        else:
            session['product'] = 'free'

        return redirect('/')

@auth.route('/refresh-token')
def refresh_token():
    if 'refresh_token'  not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET')
        }

        response = requests.post(os.getenv('TOKEN_URL'), data=req_body)
        response.raise_for_status()
        new_token_info = response.json()

        session['access_token'] =  new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/')