import firebase_admin
from firebase_admin import credentials

URL = 'https://fcm.googleapis.com/v1/projects/usask-bikegirls/messages:send HTTP/1.1'
API_KEY = 'AAAA7um6H2g:APA91bEv-cpJzDphcno5y3jCVh0e73cI0WZZOydPZVpeMyY7Pj8gSVGZGYhmrjneAErYuk0h0CGtBHtXeMsT_qwgYTzAduNjeJkq1--lkZRrh8GaNYSfAam4k-vH-i96-NlG43phFp9o'
MY_KEY = 'key=' + API_KEY

def getRegistrationToken():
   default_app = firebase_admin.initialize_app()

getRegistrationToken()
