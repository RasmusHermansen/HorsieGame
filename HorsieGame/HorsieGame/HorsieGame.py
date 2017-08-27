from Databinding.Connection import ServerConnection
from Databinding.Querier import Querier

## start Connection ##
conn = Querier(ServerConnection('Local'))
print("GameName:" + conn.InstantiateNewSession())
try:

    input("Interact as client, press enter (in terminal) to close session...")

    # Close Sessions
    conn.CloseSession()
except:
    conn.CloseSession()
    