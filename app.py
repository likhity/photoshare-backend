import time
from os import environ
from flask import *

app = Flask(__name__)

@app.route("/api/time")
def get_current_time():
  return { "time": time.time() }