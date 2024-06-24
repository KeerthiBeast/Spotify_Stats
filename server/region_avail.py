import os
import requests
from dotenv import load_dotenv, dotenv_values
import urllib.parse
import json

from flask import Flask, request, redirect, jsonify, session, render_template
from flask import Blueprint
from datetime import datetime, timedelta

region = Blueprint('region', __name__)
load_dotenv()

@region.route('/search-avail', methods=['GET', 'POST'])
def search_avail():
    if request.method == 'POST':
        if 'access_token' not in session:
            return redirect('/login')

        if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh_token')
        
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        } 
        id = request.form.get('track_id')
        country = request.form.get('cc')
        print("this is country" + country)
        url = f"{os.getenv('API_BASE_URL')}tracks/{id}"
        flag = 0
        
        if country!="":
            url = f"{os.getenv('API_BASE_URL')}tracks/{id}?market={country}"
            flag = 1

        response = requests.get(url, headers=headers)
        markets = response.json()
        
        return render_template('region_results.html', data=markets, flag=flag)
    
    return render_template('region_avail.html')