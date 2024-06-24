import os
import requests
import urllib.parse
import json
from dotenv import load_dotenv, dotenv_values

from datetime import datetime, timedelta
from flask import Blueprint
from flask import Flask, redirect, request, jsonify, session, render_template

top = Blueprint('top', __name__)
load_dotenv()

@top.route('/user-fav-short')
def user_fav_short():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    url = f"{os.getenv('API_BASE_URL')}me/top/tracks?time_range=short_term"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    favourite = json.loads(response.content)['items']

    fav_short_id = [] 
    for data in favourite:
        fav_short_id.append(data['uri'])
    session['id_short'] = fav_short_id

    return render_template('fav_short.html', data=favourite)

@top.route('/user-fav-medium')
def user_fav_medium():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    url = f"{os.getenv('API_BASE_URL')}me/top/tracks"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    favourite = json.loads(response.content)['items']

    fav_medium_id = []
    for data in favourite:
        fav_medium_id.append(data['uri'])
    session['id_medium'] = fav_medium_id

    return render_template('fav_medium.html', data=favourite)

@top.route('/user-fav-long')
def user_fav_long():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    url = f"{os.getenv('API_BASE_URL')}me/top/tracks?time_range=long_term"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    favourite = json.loads(response.content)['items']

    fav_long = []
    for data in favourite:
        fav_long.append(data['uri'])
    session['id_long'] = fav_long

    return render_template('fav_long.html', data=favourite)