import urllib
import urllib2

url = 'https://fcm.googleapis.com/v1/projects/usask-bikegirls/messages:send HTTP/1.1'
api_key = 'AAAA7um6H2g:APA91bEv-cpJzDphcno5y3jCVh0e73cI0WZZOydPZVpeMyY7Pj8gSVGZGYhmrjneAErYuk0h0CGtBHtXeMsT_qwgYTzAduNjeJkq1--lkZRrh8GaNYSfAam4k-vH-i96-NlG43phFp9o'
my_key = 'key=' + api_key

def sendDeviceStatus(reg_id):
    json_data = {
        'to': reg_id,
        'data': {
            'hello': 'world'
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': my_key
    }
    
    data = urllib.urlencode(json_data)
    req = urllib2.Request(url, data)
    req.add_header('Authorization', my_key)
    fd = urllib2.urlopen(req)
    res = f.read()
    f.close()
    
    print('DONE')


def getRegistrationToken():
    req = urllib2.Request(url)
    req.add_header('Authorization', my_key)
    res = urllib2.urlopen(req)
    reg_id = res.read()
    print(reg_id)

getRegistrationToken()
