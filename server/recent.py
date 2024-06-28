import os
import requests
from dotenv import load_dotenv, dotenv_values
import urllib.parse
import json

from flask import Flask, request, redirect, jsonify, session, render_template
from flask import Blueprint
from datetime import datetime, timedelta

recent = Blueprint('recent', __name__)
load_dotenv()

@recent.route('/view-recent')
def view_recent():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    url = f"{os.getenv('API_BASE_URL')}me/player/recently-played"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tracks = json.loads(response.content)['items']

    return render_template('recent.html', data=tracks)