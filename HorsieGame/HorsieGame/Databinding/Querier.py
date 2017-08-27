from .Connection import ServerConnection

class Querier():
    __sessId = -1

    def __init__(self, conn):
        assert isinstance(conn,ServerConnection), "Invalid connection supplied to Querier"
        self.conn = conn

    def InstantiateNewSession(self):
        r = self.conn.PostRequest("CreateSession", None)
        data = r.json()
        self.__sessId = data['uniqueId']
        return data['sessionName']

    def __IsInstantiated(self):
        return self.sessId != -1

    def CloseSession(self):
        self.conn.PostRequest("CloseSession", {'SessionId':self.__sessId})
