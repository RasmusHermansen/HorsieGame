from Databinding.Connection import ServerConnection
from Databinding.Querier import Querier

## start Connection ##
conn = Querier(ServerConnection('Local'))
print("GameName:" + conn.InstantiateNewSession())
try:
    print("What up")
    
    # Close Sessions
    conn.CloseSession()
except:
    conn.CloseSession()
    