import requests

class ServerConnection():


    def __init__(self, url):
        if(url == 'Local'):
            self.__LocalHost()

    ## start localhost ##
    def __LocalHost(self):
        import runserver as rs
        from runserver import app
        import threading
        svr = threading.Thread(target=rs.HostLocal,args=())
        svr.start()
        while True:
            try:
                requests.get("http://localhost:5555/", timeout=0.5)
                print("Initialised localhost")
                return
            except requests.exceptions.ConnectionError:
                pass
