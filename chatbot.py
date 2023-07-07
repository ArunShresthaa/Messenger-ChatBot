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
  "access_token": "<Your access token here>"
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
                
            
username = input('username')
password = input('password')
# Create an instance of your custom client
client = AutoReplyClient(username,password)

# Run the client indefinitely
while True:
    client.listen()