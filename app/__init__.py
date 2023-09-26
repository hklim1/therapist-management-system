from flask import Flask, request

app = Flask(__name__)

from resources.patients import routes
from resources.interventions import routes