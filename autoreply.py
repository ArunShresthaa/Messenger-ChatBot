import fbchat
import requests
import re
from fbchat import log, Client
from fbchat.models import *

def session_factory(user_agent=None):
    session = requests.session()
    session.headers["Referer"] = "https://www.facebook.com"
    session.headers["Accept"] = "text/html"

    # TODO: Deprecate setting the user agent manually
    return session

fbchat._state.session_factory = session_factory
fbchat._state.FB_DTSG_REGEX = re.compile(r'"token":"(.*?)"')
# Subclass the `Client` class to create your own client
class AutoReplyClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)  
        self.markAsRead(thread_id)  

        if author_id != self.uid:
            reply_text = "Thank you for your message!\nI am busy right now.\nWill reply ASAP. This is an automated reply."
            self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)

username = 
password = 
# Create an instance of your custom client
client = AutoReplyClient(username,password)

# Run the client indefinitely
while True:
    client.listen()
