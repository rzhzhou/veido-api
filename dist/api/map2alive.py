import time
import requests
import threading


class MapAlive(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        login_cookie = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2l"\
            "kIjoxLCJ1c2VyX2lkIjoxLCJhX25hbWUiOiJ3dWhhbnpoaWppYW4iLCJhX3JlYWx"\
            "uYW1lIjoi566h55CG5ZGYIiwiYV9wd2QiOiI3YjNkNzgzMzFlNDQ0YzNmODBkO"\
            "Dc1Njc4YjA1ODkyYmFiMmY1MTU3IiwiYV9waG9uZSI6bnVsbCwiYV9lbWFpbCI6"\
            "Ind1aGFuemhpamlhbkBzaGVuZHUuaW5mbyIsImFfbG9nbyI6bnVsbCwic3Rh"\
            "dHVzIjoxLCJzeXN0ZW1faWQiOjEsImlzcm9vdCI6MSwiU3lzQWNjb3VudFNhbHQiO"\
            "nsic2FsdCI6ImZjMDhlNDFlZjkzZjIwYTYyYjhmY2I4ODc1ZThmNTJmZTJkZGExYTkifX0.x4IP"\
            "k4Cnka7Z2izoZ2uTMjh7lzpsrJA3zs7hWTqnhFk"
        count = 0
        print "map_alive start"
        while True:
            url = "http://192.168.0.215/api/dashboard?ed=2015-07-23&edId=9335&sd=2015-06-23&sdId=9305"
            headers = {
                "Authorization" : "Bearer "+login_cookie,
            }
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                if count > 3:
                    print "cookie fail !"
                    break
                count += 1
            print res.status_code
            time.sleep(300)
            
MapAlive().start()
    
