import fbchat
import requests
from revChatGPT.V1 import Chatbot
import re
from fbchat import log, Client
from fbchat.models import *
import time

def session_factory(user_agent=None):
    session = requests.session()
    session.headers["Referer"] = "https://www.facebook.com"
    session.headers["Accept"] = "text/html"

    # TODO: Deprecate setting the user agent manually
    return session

fbchat._state.session_factory = session_factory
fbchat._state.FB_DTSG_REGEX = re.compile(r'"token":"(.*?)"')

self_tag = '@Aaron Shrestha'

chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJvbGRvbGRwaG90b3MxMjM0NTY3ODlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItRkF1WTBRQUhSRldQRXdmU2h5WFNJUG9jIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDcxOTY5Mzc3MzA1ODEzMTcyNSIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODczNTIzODAsImV4cCI6MTY4ODU2MTk4MCwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUifQ.N4rRKN6hCodomgBeAqhpkkWSbsGfyDLQSC37owmI1IkhHxyrwUf6fyJXiuQOKE6nSDEAnajoWhcw5igx7oeRlFOGyXD9JuQvhrO1yX-hsfCgp9lwzxoeRAFL2Ri77ge4EBUmKj0rTWliPL3ffMMZ_cAfgeP-T9xUCde3HH8xfn-A7m3DxT0cv8ydnGri8pLwo7YFaHeZnaJx5udu6wLUYzOWEXglZ9BpylBCAs5Q1xLBvzyRPFQ7tG4p7Nb21ju9EfKv8kZ1xXz1LMjj_kRGH88cwj_gm7fvA8xiLKXe9jHgNFirsZ6wuW-U91IpPBlST8BB-BQiJ4amGL8pCx3e4A"
})

# Subclass the `Client` class to create your own client
class AutoReplyClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        message = message_object.text
        
        if thread_type == ThreadType.GROUP:
            group_tag = message[:15]
            if group_tag != self_tag:
                return
            else:
               message = message[15:]
            
        self.markAsDelivered(thread_id, message_object.uid)  # Mark message as delivered
        self.markAsRead(thread_id)  # Mark message as read

        # Check if the message is from a user and not the client itself
        if author_id != self.uid:
            self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)

            prompt =message
            response = ""
            for data in chatbot.ask(
              prompt
            ):
                response = data["message"]

            self.setTypingStatus(TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)
            
            if thread_type == ThreadType.USER:
                self.send(Message(text = response),thread_id=thread_id,thread_type=thread_type)
            else:
                # Get the sender's name
                sender_name = self.fetchUserInfo(author_id)[author_id].name
            
                # Build the reply message with the tagged sender's name
                reply_message = f"@{sender_name}\n\n{response}"

                # Send the reply message
                self.send(
                    Message(text=reply_message, mentions=[Mention(thread_id=thread_id, offset=0, length=len(sender_name)+1)]),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                
            
# username = 'aruncresta10@gmail.com'
# password = 'arun@1234'

username = '9745979351'
password = 'arun@159'
# Create an instance of your custom client
client = AutoReplyClient(username,password)

# Run the client indefinitely
while True:
    client.listen()