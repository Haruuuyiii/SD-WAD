from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import time
import os

app = Flask(__name__, static_folder="static")
CORS(app)

rate_limit_store = {}
RATE_LIMIT = 15
RATE_WINDOW = 60

def check_rate_limit(ip):
    now = time.time()
    history = rate_limit_store.get(ip,[])
    history = [t for t in history if now - t < RATE_WINDOW]
    
# kain lang ako tapos tulungan kita  - drei