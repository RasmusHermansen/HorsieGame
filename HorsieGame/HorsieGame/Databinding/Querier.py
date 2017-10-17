from .Connection import ServerConnection

class Querier():
    _sessId = -1
    _sessKey = ""

    def __init__(self, conn):
        assert isinstance(conn,ServerConnection), "Invalid connection supplied to Querier"
        self.conn = conn

    def IsInstantiated(self):
        return self._sessId != -1

    def InstantiateNewSession(self):
        r = self.conn.PostRequest("CreateSession", None)
        data = r.json()
        self._sessKey = data['sessionKey']
        self._sessId = data['uniqueId']
        return data['sessionName']

    def GetPlayers(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("GetAllPlayers", {'sessionId':self._sessId,'sessionKey':self._sessKey})
        return r.json()

    def SetHorseCount(self,count):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("SetHorses", {'sessionId':self._sessId,'sessionKey':self._sessKey,'horsesCount':count})
        return r.json()

    def CloseSession(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        self.conn.PostRequest("CloseSession", {'sessionId':self._sessId,'sessionKey':self._sessKey})
