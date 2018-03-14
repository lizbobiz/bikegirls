import logging
import socket
import uuid
import json
import firebase_admin
import time

from firebase_admin import db, credentials
from sleekxmpp.clientxmpp import ClientXMPP
from sleekxmpp.xmlstream.handler.callback import Callback
from sleekxmpp.xmlstream.matcher.xpath import MatchXPath


logging.basicConfig(level=logging.DEBUG, format='%(levelname)7s %(module)12s:%(lineno)-4s %(message)s')

def getRegistrationToken():
    # Authenticate database access
    cred = credentials.Certificate('adminsdk.json')
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://usask-bikegirls.firebaseio.com'
    })
    
    # Get registration token
    reg_id = db.reference('reg_id').get()
    print
    
    # Delete app instance
    firebase_admin.delete_app(app)
    
    return reg_id

FCM_SERVER_URL = 'fcm-xmpp.googleapis.com'
FCM_SERVER_PORT = 5236
FCM_SERVER_KEY = 'AAAA7um6H2g:APA91bEv-cpJzDphcno5y3jCVh0e73cI0WZZOydPZVpeMyY7Pj8gSVGZGYhmrjneAErYuk0h0CGtBHtXeMsT_qwgYTzAduNjeJkq1--lkZRrh8GaNYSfAam4k-vH-i96-NlG43phFp9o'
FCM_SENDER_ID = '1026123505512'
FCM_JID = FCM_SENDER_ID + '@gcm.googleapis.com'
FCM_SERVER_IP = socket.gethostbyname(FCM_SERVER_URL)

class Client(ClientXMPP):
    def __init__(self):
        ClientXMPP.__init__(self, FCM_JID, FCM_SERVER_KEY, sasl_mech='PLAIN')
        self.registerHandler(Callback(
            'FCM Message',
            MatchXPath('{%s}message/{%s}gcm' % (self.default_ns, 'google:mobile:data')),
            self.recv_message)
        )
        self.auto_reconnect = False
        self.connect((FCM_SERVER_IP, FCM_SERVER_PORT), use_tls=True, use_ssl=True, reattempt=False)
        self.process(threaded=False)
    
    def recv_message(self, msg):
        data = json.loads(msg.xml.find('{google:mobile:data}gcm').text)
        
        body = {
            'data': {
                'message': 'acknowledgement'
            },
            'to': getRegistrationToken(),
            'message_id': data['message_id'],
            'message_type': 'ack'
        }
        ack = '<message id=""><gcm xmlns="google:mobile:data">' + json.dumps(body) + '</gcm></message>'
        self.send_raw(ack)

client = Client()
client.disconnect(wait=True)
