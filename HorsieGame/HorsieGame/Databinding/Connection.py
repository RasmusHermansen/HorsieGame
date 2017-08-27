import requests

class ServerConnection():
    _url = ""

    def __init__(self, url):
        if(url == 'Local'):
            self.__LocalHost()
        elif(self.__ValidConnection(url)):
            self._url = url
        else:
            raise ConnectionError("Unabled to establish connection to Server at: {0}".format(url))
        self._url = self._url + "/Game/api/v1.0/"

    def __ValidConnection(self, url):
        try:
            requests.get("http://localhost:5555/", timeout=0.5)
            return True
        except requests.exceptions.ConnectionError:
            return False

    def PostRequest(self, target, data):
        return requests.post(self._url + target, json = data)


    ## start localhost ##
    def __LocalHost(self):
        import runserver as rs
        from runserver import app
        import threading
        print("Initializing local instance of server")
        svr = threading.Thread(target=rs.HostLocal,args=())
        svr.start()
        while not self.__ValidConnection("http://localhost:5555/"):
            pass
        self._url = "http://localhost:5555"
        print("Initialised local instance at http://localhost:5555/")