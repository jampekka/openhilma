#!/usr/bin/env python3

from flask import Flask
from eve import Eve
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

api = Eve()
static = Flask(__name__)
app = DispatcherMiddleware(static, {'/api': api})

if __name__ == '__main__':
    run_simple('0.0.0.0', 23058, app, use_reloader=True, use_debugger=True)
