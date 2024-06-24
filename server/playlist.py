import os
from dotenv import load_dotenv, dotenv_values
import requests
import urllib.parse
import json

from flask import Flask, request, redirect, jsonify, session
from flask import Blueprint
from datetime import datetime, timedelta

playlist = Blueprint('playlist', __name__)
load_dotenv()

@playlist.route('/create-playlist-short')
def create_playlist_short():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}", 
        'Content-Type': 'application/json'
    }
    req_body = {
        'name': 'Favourite songs (Last 4 weeks)',
        'description': 'Create using API',
        'public': True
    }
    url = f"{os.getenv('API_BASE_URL')}users/{session['id']}/playlists"

    response = requests.post(url, headers=headers, json=req_body)
    response.raise_for_status()

    playlist_info = response.json()
    playlist_id = playlist_info['id']

    add_url = f"{os.getenv('API_BASE_URL')}playlists/{playlist_id}/tracks"
    add_body = {
        'uris': session['id_short'],
        'position': 0
    }

    response = requests.post(add_url, headers=headers, json=add_body)
    response.raise_for_status()

    return('', 204)

@playlist.route('/create-playlist-medium')
def create_playlist_medium():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}", 
        'Content-Type': 'application/json'
    }
    req_body = {
        'name': 'Favourite Songs (Last 6 months)',
        'description': 'Created using API',
        'public': True
    }
    url = f"{os.getenv('API_BASE_URL')}users/{session['id']}/playlists"

    response = requests.post(url, headers=headers, json=req_body)
    response.raise_for_status()

    playlist_info = response.json()
    playlist_id = playlist_info['id']

    add_url = f"{os.getenv('API_BASE_URL')}playlists/{playlist_id}/tracks"
    add_body = {
        'uris': session['id_medium'],
        'position': 0
    }

    response = requests.post(add_url, headers=headers, json=add_body)
    response.raise_for_status()

    return('', 204)

@playlist.route('/create-playlist-long')
def create_playlist_long():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}", 
        'Content-Type': 'application/json'
    }
    req_body = {
        'name': 'Favourite songs (Last 12 months)',
        'description': 'Created using API', 
        'public': True
    }
    url = f"{os.getenv('API_BASE_URL')}users/{session['id']}/playlists"

    response = requests.post(url, headers=headers, json=req_body)
    response.raise_for_status()

    playlist_info = response.json()
    playlist_id = playlist_info['id']

    add_url = f"{os.getenv('API_BASE_URL')}playlists/{playlist_id}/tracks"
    add_body = {
        'uris': session['id_long'],
        'position': 0
    }

    response = requests.post(add_url, headers=headers, json=add_body)
    response.raise_for_status()

    return('', 204)