import time
import os
from flask import *

app = Flask(__name__)

@app.route("/api/time")
def get_current_time():
  return { "time": time.time() }