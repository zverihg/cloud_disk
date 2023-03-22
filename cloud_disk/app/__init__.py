#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
from flask import Flask, request, Response, render_template, redirect, url_for, make_response, send_file
import traceback

import json
import sys
import os

from dir_api import get_dfl_dir
from dir_api import get_dir_bck
from dir_api import snt_fil_str
from dir_api import get_dir
from dir_api import del_fil
from dir_api import dwn_fil
from dir_api import chk_con
from dir_api import rnm_fil

def dlog( tgt, msg ):		# w/o print
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog_prn( tgt, msg ):	# with print
	print msg
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def inflo(msg):
	print msg
	with open ( 'data/hitme/logs/req.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def elo(msg):
	print msg
	with open ( 'data/hitme/logs/elo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def req_lo(msg):
	print msg
	with open ( 'data/hitme/logs/req_lo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

app = Flask(__name__, static_folder = '/data/hitme/static/', template_folder='templates')
app.config.update( SESSION_COOKIE_SECURE=True,SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',)

@app.route("/dir")
def dir(): return render_template('sha_dir.html')

@app.route("/dir/chk_con", methods=['POST'])
def chk_con_api():
	log = '''
		chk_con_api
		{req}
	'''.format(req = request.form)
	inflo(log)
	
	res = chk_con()
	return Response( json.dumps(res) )

@app.route("/dir/get_dfl_dir", methods=['POST'])
def get_dfl_dir_api():
	log = '''
		get_dfl_dir_api
		{req}
	'''.format(req = request.form)
	inflo(log)
	res = get_dfl_dir()
	return Response( json.dumps(res))

@app.route("/dir/get_dir", methods=['POST'])
def get_dir_api():
	try:
		log = '''
			get_dir_api
			{req}
		'''.format(req = request.form)
		inflo(log)
		dta = get_dir(request.form)
		return Response( json.dumps({"dta":str(dta).replace("'", '"')}))
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))

@app.route("/dir/rnm_fil", methods=['POST'])
def rnm_fil_api():
	try:
		dta = rnm_fil(request.form)
		return Response( json.dumps({"dta":str(dta).replace("'", '"')}))
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))

@app.route("/dir/get_dir_bck", methods=['POST'])
def get_dir_bck_api():
	try:
		log = '''
			get_dir_bck_api
			{req}
		'''.format(req = request.form)
		inflo(log)
		dta = get_dir_bck(request.form)
		return Response( json.dumps({"dta":str(dta).replace("'", '"')}))
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))

@app.route("/dir/dwn_fil", methods=['POST'])
def dwn_fil_api():
	try:
		log = '''
			dwn_fil_api
			{req}
		'''.format(req = request.form)
		inflo(log)
		pth = dwn_fil(request.form)
		return Response( json.dumps({"dta":pth }))
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))

@app.route("/dir/snt_fil", methods=['POST'])
def snt_fil_api():
	try:

		snt_fil_str(request)
		return Response( json.dumps({"dta":'ok' }))
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))

@app.route("/dir/del_fil", methods=['POST'])
def del_fil_api():
	try:

		dta = del_fil(request.form)
		return Response( json.dumps({"dta":str(dta).replace("'", '"')}))

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  Response( json.dumps({"dta":str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1]))).replace("'", '"')}))
