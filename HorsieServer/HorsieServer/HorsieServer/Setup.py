import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

## INIT APP ##

app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(
    #DEBUG= True,
    DATABASE= os.path.join(app.root_path, 'Horsie.db'),
    SECRET_KEY= 'fTcCO24fOIcMShAvHJ5v7TVEuEnKoaQPMLvX5PRw'
    ))

import HorsieServer.db as db
import HorsieServer.views
import HorsieServer.api