from .Connection import ServerConnection
import os

class Querier():
    __tempSessionStorage = os.path.join(os.path.dirname(os.path.realpath(__file__)),"tmp")
    _sessId = -1
    _sessKey = ""

    def __init__(self, conn):
        assert isinstance(conn,ServerConnection), "Invalid connection supplied to Querier"
        self.conn = conn

    def IsInstantiated(self):
        return self._sessId != -1

    def TryInstantiateOldSession(self):
        oldConn = self.RecoverConn()
        print(oldConn)
        self._sessKey = oldConn[0]
        self._sessId = oldConn[1]
        return oldConn[2]

    def InstantiateNewSession(self):
        r = self.conn.PostRequest("CreateSession", None)
        data = r.json()
        self._sessKey = data['sessionKey']
        self._sessId = data['uniqueId']

        # dump connection
        self.DumpConn([self._sessKey, self._sessId, data['sessionName']])
        return data['sessionName']

    def GetPlayers(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("GetAllPlayers", {'sessionId':self._sessId,'sessionKey':self._sessKey})
        return r.json()

    def GetDrinks(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("GetDrinks", {'sessionId':self._sessId,'sessionKey':self._sessKey})
        return r.json()

    def DealDrink(self, drinkId):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("DrinksDealt", {'sessionId':self._sessId,'sessionKey':self._sessKey, 'drinkId':drinkId})

    def SetHorseCount(self,count):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("SetHorses", {'sessionId':self._sessId,'sessionKey':self._sessKey,'horsesCount':count})
        return r.json()

    def GrantPlayerFunds(self, playerId, funds):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        r = self.conn.PostRequest("AdjustPlayerFunds", {'sessionId':self._sessId,'sessionKey':self._sessKey, 'userId':playerId, 'amount':funds})

    def CloseSession(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        self.conn.PostRequest("CloseSession", {'sessionId':self._sessId,'sessionKey':self._sessKey})

    def ReportResults(self, results):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        self.conn.PostRequest("ReportResults", {'sessionId':self._sessId,'sessionKey':self._sessKey,'results':results})

    def DisableBetting(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        self.conn.PostRequest("DisableBetting", {'sessionId':self._sessId,'sessionKey':self._sessKey})

    def RaceStarting(self):
        assert self.IsInstantiated(), "Query attempted without an instantiated session"
        self.conn.PostRequest("RaceStarting", {'sessionId':self._sessId,'sessionKey':self._sessKey})

    # Reconnect dump read
    def DumpConn(self, data):
        with open(self.__tempSessionStorage, 'w') as f:
            f.writelines([str(dat) + " \n" for dat in data])

    def RecoverConn(self):
        with open(self.__tempSessionStorage, 'r') as f:
            content = f.readlines()
        return [x.strip() for x in content]

