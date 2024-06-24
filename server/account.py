import os
import requests
import urllib.parse
import json
from dotenv import load_dotenv, dotenv_values

from datetime import datetime, timedelta
from flask import Blueprint
from flask import Flask, redirect, request, jsonify, session, render_template

account = Blueprint('account', __name__)
load_dotenv()

@account.route('/account')
def view_account():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    
    data = []
    data.extend([session['id'], session['display_name'],
                 session['product'], session['profile_pic']])

    return render_template('account.html', data=data)

@account.route('/logout')
def logout():
    if 'access_token' not in session:
        return redirect('/')

    if datetime.now().timestamp() > session['expires_at']:
        session.clear()
        return redirect('/')

    session.clear()
    return redirect('/') 