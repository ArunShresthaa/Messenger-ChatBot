import fbchat
import re
from fbchat import log, Client
from fbchat.models import *
fbchat._state.FB_DTSG_REGEX = re.compile(r'"token":"(.*?)"')
# Subclass the `Client` class to create your own client
class AutoReplyClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)  # Mark message as delivered
        self.markAsRead(thread_id)  # Mark message as read

        # log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message_object.text))

        # Check if the message is from a user and not the client itself
        if author_id != self.uid:
            reply_text = "Thank you for your message!\nI am busy right now.\nWill reply ASAP. This is an automated reply."
            self.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)

        # Continue listening for messages
        # self.listen()


username = ''
password = ''
# Create an instance of your custom client
client = AutoReplyClient(username,password)

# Run the client indefinitely
while True:
    client.listen()
