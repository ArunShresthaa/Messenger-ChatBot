import json
import fbchat
import requests
import re

def session_factory(user_agent=None):
    session = requests.session()
    session.headers["Referer"] = "https://www.facebook.com"
    session.headers["Accept"] = "text/html"

    # TODO: Deprecate setting the user agent manually
    return session

fbchat._state.session_factory = session_factory
fbchat._state.FB_DTSG_REGEX = re.compile(r'"token":"(.*?)"')

cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

# Attempt a login with the session, and if it fails, just use the email & password
client = fbchat.Client('username', 'pass', session_cookies=cookies)
print('logged in')

# ... Do stuff with the client here

# Save the session again
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)