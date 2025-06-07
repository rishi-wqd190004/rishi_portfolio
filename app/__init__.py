from flask import Flask
import yaml
import os, json
import csv
from app.models import db, TimelinePost
from app.userinfo import userinfo # load userinfo

app = Flask(__name__, static_folder='static')

# Load project/user info from YAML file
with open(os.path.join(os.path.dirname(__file__), 'static/data/projects.yaml')) as f:
    projects = yaml.safe_load(f)

# Initialize DB
db.connect()
db.create_tables([TimelinePost])

# Store in app config for access in routes
app.config['USERINFO'] = userinfo
app.config['PROJECTS'] = projects

# Import routes after app and config are set up
from app import routes
