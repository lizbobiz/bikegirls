# Standard library imports
import json
import logging
import socket
import time
import uuid

# Third-party imports
import firebase_admin
from firebase_admin import db, credentials
from sleekxmpp.clientxmpp import ClientXMPP
from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.xpath import MatchXPath


# FCM database constants
FCM_DB_URL = 'https://usask-bikegirls.firebaseio.com'
FCM_DB_CERT_PATH = 'adminsdk.json'

# FCM server XMPP constants
FCM_SERVER_URL = 'fcm-xmpp.googleapis.com'
FCM_SERVER_PORT = 5236
FCM_SERVER_KEY = 'AAAA7um6H2g:APA91bEv-cpJzDphcno5y3jCVh0e73cI0WZZOydPZVpeMyY7Pj8gSVGZGYhmrjneAErYuk0h0CGtBHtXeMsT_qwgYTzAduNjeJkq1--lkZRrh8GaNYSfAam4k-vH-i96-NlG43phFp9o'
FCM_SENDER_ID = '1026123505512'
FCM_JID = FCM_SENDER_ID + '@gcm.googleapis.com'
FCM_SERVER_IP = socket.gethostbyname(FCM_SERVER_URL)


""" Get an authorized Firebase app instance. """
def get_fcm_app():
    return firebase_admin.initialize_app(
        credentials.Certificate(FCM_DB_CERT_PATH),
        { 'databaseURL': FCM_DB_URL })

""" Delete the given Firebase app instance. """
def delete_fcm_app(app):
    firebase_admin.delete_app(app)


class Client(ClientXMPP):
    """
    Create a new XMPP client to act as FCM app server, connect it to the FCM
    server, and begin processing the XML stream.
    """
    def __init__(self):
        # Create client with FCM server login info
        super(Client, self).__init__(
            FCM_JID,
            FCM_SERVER_KEY,
            sasl_mech='PLAIN')
        
        # Create pending command queue
        self.cmd_q = []
        
        # Create handler for received messages
        self.registerHandler(Callback(
            'FCM Message Receive',
            MatchXPath('{%s}message/{%s}gcm'% (self.default_ns, 'google:mobile:data')),
            self.recv_message))
        
        # Connect to server and begin processing XML stream
        self.auto_reconnect = False
        self.connect(
            (FCM_SERVER_IP, FCM_SERVER_PORT),
            use_tls=True,
            use_ssl=True,
            reattempt=False)
        self.process(threaded=True)
    
    """
    Client handler for received messages. Upon receiving a message, an
    acknowledgement message is sent to the client app and the command specified
    in the received message is executed.
    """
    def recv_message(self, msg):
        # Get message contents
        print '\n\n%s\n\n' % (msg.xml.find('{google:mobile:data}gcm'))
        msg_body = json.loads(msg.xml.find('{google:mobile:data}gcm').text)
        logging.debug('Received message: %s' % (json.dumps(msg_body)))
        
        if not 'category' in msg_body:
            return
        
        # Build ack message body and format as XMPP message
        ack_body = {
            'to': msg_body['from'],
            'message_id': msg_body['message_id'],
            'message_type': 'ack'
        }
        ack_msg = '<message id=""><gcm xmlns="google:mobile:data">' + json.dumps(ack_body) + '</gcm></message>'
        
        # Send ack
        self.send_raw(ack_msg)
        
        # Check command field, execute operation, and update database
        msg_data = msg_body['data']
        if 'command' in msg_data:
            if msg_data['command'] == 'TOGGLE_ARMED':
                self.cmd_q.append('TOGGLE_ARMED')
            elif msg_data['command'] == 'DISARM_ALARM':
                self.cmd_q.append('DISARM_ALARM')
    
    def send_notification(self, title, body):
        # Build notification body
        notif_body = {
            'to': db.reference('reg_id').get(),
            'message_id': uuid.uuid4().hex,
            'notification': {
                'title': str(title),
                'body': str(body)
            },
            'time_to_live': 600
        }
        notif_msg = '<message id=""><gcm xmlns="google:mobile:data">' + json.dumps(notif_body) + '</gcm></message>'
        
        # Send notification
        self.send_raw(notif_msg)
