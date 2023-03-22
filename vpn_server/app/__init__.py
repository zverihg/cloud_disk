from flask import Flask, request, Response, render_template, redirect, url_for, make_response
import traceback
from functools import wraps
import sqlite3
import datetime as dt
import datetime
import time
import json
import sys
import os
from dirs_mdl import get_dfl_dir
from dirs_mdl import get_dir_bck
from dirs_mdl import snt_fil_str
from dirs_mdl import get_dir
from dirs_mdl import del_fil
from dirs_mdl import get_zip
from dirs_mdl import rnm_fil

app = Flask(__name__, static_folder = '/data/hitme/static/', template_folder='templates')

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

def elo(msg):
	print msg
	with open( '/data/hitme/logs/elo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def inflo(msg):
	print msg
	with open( '/data/hitme/logs/inflo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog( tgt, msg ):		# w/o print
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog_prn( tgt, msg ):	# with print
	print msg
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

@app.route('/')
def index():
	return render_template('iii.html')

@app.route("/chk_con")
def chk_con():
	return Response( json.dumps({"sta":str(True)}))

@app.route("/get_dfl_dir")
def get_dfl_dir_api():
	res = get_dfl_dir()
	return Response( json.dumps({"sta":res}))

@app.route("/get_dir_api", methods=['POST'])
def get_dir_api():
	dlog_prn('/data/dir_log.txt', dict(request.form))
	res = get_dir(dict(request.form))
	return Response( json.dumps({"sta":res}))

@app.route("/del_fil_api", methods=['POST'])
def del_fil_api():
	dlog_prn('/data/dir_log.txt', dict(request.form))
	res = del_fil(dict(request.form))
	return Response( json.dumps({"sta":res}) )


@app.route("/get_dir_bck_api", methods=['POST'])
def get_dir_bck_api():
	dlog_prn('/data/dir_log.txt', dict(request.form))
	res = get_dir_bck(dict(request.form))
	return Response( json.dumps({"sta":res}))

@app.route("/rnm_fil", methods=['POST'])
def rnm_fil_api():
	dlog_prn('/data/dir_log.txt', dict(request.form))
	res = rnm_fil(dict(request.form))
	return Response( json.dumps({"sta":res}))


@app.route("/get_zip", methods=['POST'])
def get_zip_api():
	try:
		res = get_zip(dict(request.form), request)
		return Response( json.dumps(res))
	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

@app.route("/snt_fil_str", methods=['POST'])
def snt_fil_str_api():
	try:
		res = snt_fil_str(dict(request.form), request)
		return Response( json.dumps({"sta":res}))

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))