import os

from functools import wraps
from flask import make_response, request

USER = os.getenv('SITE_USER',default="Please provide a site user.")
PASS = os.getenv('SITE_PASS',default="Please provide a site password.")

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if auth and auth.username == USER and auth.password == PASS:
            return f(*args, **kwargs)
        return make_response("<h>Access Denied</h1>", 401, {'WWW-Authenticate' : 'Basic Realm="Login please"'});

    return decorated

