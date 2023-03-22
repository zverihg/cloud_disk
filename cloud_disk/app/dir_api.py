#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import sys
import os
import traceback
import requests
import json
from flask import Flask, request, Response, render_template, redirect, url_for, make_response
from transliterate import translit
import time
import threading
import time
from multiprocessing import Process

reload( sys )
sys.setdefaultencoding( 'utf8' )

def dlog( tgt, msg ):		# w/o print
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog_prn( tgt, msg ):	# with print
	print msg
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def inflo(msg):
	print msg
	with open ( 'data/hitme/logs/info.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def elo(msg):
	print msg
	with open ( 'data/hitme/logs/elo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def onbin( a ): return ' '.join( format( ord(x), 'b') for x in ''.join( json.dumps( a ) ) )
def unbin( a ):	return json.loads( ''.join( unichr( int( x, 2 ) ) for x in a.split(' ') ) )

def chk_con():
	try:
		url = 'http://10.8.0.2/chk_con'
		try:	res = requests.get(url = url , timeout=2)
		except:	return 0
		inflo( res )
		return 1
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return 0

def get_dfl_dir():

	url = 'http://10.8.0.2/get_dfl_dir'
	res = requests.get(url = url)
	inflo( res.content)
	return res.content

def get_dir_2(dir_dta):

	try:
		now_dir = dir_dta['now_dir'][0]
		dir_nme = dir_dta['dir_nme'][0]
		
		dir_new = '{now_dir}{dir_nme}/'.format(now_dir = now_dir, dir_nme = dir_nme)

		dlog_prn('/data/dir_log.txt', dir_new)

		dir_lst = os.listdir('./{now_dir}/{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme))	

		dta = {'dir_new': dir_new, 'dir_lst': dir_lst }
		
		return dta

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

def get_dir(dir_dta):
	try:
		url = 'http://10.8.0.2/get_dir_api'
		res = requests.post(url = url, data = dir_dta)
		inflo( res.content)
		return res.content

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

def del_fil(dir_dta):
	try:
		url = 'http://10.8.0.2/del_fil_api'
		res = requests.post(url = url, data = dir_dta)
		inflo( res.content)
		return res.content

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

def snt_fil_str_old(req):
	try:
		fil_req = req.files['file']
		fil_nme = fil_req.filename
		fil_req.save(os.path.join('/data/hitme/static/files', fil_nme))

		fil_pth = req.form['fil_pth']

		with open('/data/hitme/static/files/' + fil_nme, 'rb') as fil: fil_str = fil.read() 

		inflo(len(fil_str))
		inflo(fil_str[0])

		data = 	{ 'fil_nme': fil_nme, 'fil_pth': fil_pth}#, 'fil_str': fil_str }

		files = {'upload_file': open('/data/hitme/static/files/' + fil_nme,'rb')}
		values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

		url = 'http://10.8.0.2/snt_fil_str'
		res = requests.post(url, files=files, data=data)

		inflo(res.content)

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

def snt_fil_str(req):
	try:
		fil_req = req.files['file']
		fil_nme = fil_req.filename

		fil_nme = translit(fil_nme, language_code='ru', reversed=True)

		fil_req.save(os.path.join('/data/hitme/static/files', fil_nme))
		fil_pth = req.form['fil_pth']

		host = "10.8.0.2"
		port = 22
		transport = paramiko.Transport((host, port))

		password	= your_password
		username	= your_login

		transport.connect(username = username, password = password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		path = '/data/shared_disk/' + fil_pth + fil_nme
		inflo(fil_pth)
		localpath = '/data/hitme/static/files/' + fil_nme
		sftp.put(localpath, path)

		sftp.close()
		transport.close()

		os.remove(localpath)


	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

def get_dir_bck(dir_dta):
	try:
		url = 'http://10.8.0.2/get_dir_bck_api'
		res = requests.post(url = url, data = dir_dta)
		inflo( res.content)
		return res.content
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

def dwn_fil(dir_dta):
	try:

		now_dir = dir_dta['now_dir']
		dir_nme = dir_dta['dir_nme']
		ext = dir_dta['ext']

		dta = {'dir_nme': dir_nme, 'now_dir' : now_dir }

		if ext == "Folder":

			url = 'http://10.8.0.2/get_zip'
			res = requests.post(url = url, data = dta)

			host = "10.8.0.2"
			port = 22
			transport = paramiko.Transport((host, port))

			password	= your_password
			username	= your_login

			transport.connect(username = username, password = password)

			sftp = paramiko.SFTPClient.from_transport(transport)

			remotepath = res.content[1:-1]

			localpath = '/data/hitme/static/files/' + dir_nme + '.zip'

			inflo(remotepath)
			inflo(localpath)

			res = sftp.get(remotepath = remotepath, localpath = localpath)
			inflo(res)

			sftp.close()
			transport.close()

		else:
			host		= "10.8.0.2"
			port		= 22
			transport	= paramiko.Transport((host, port))
			password	= your_password
			username	= your_login

			transport.connect(username = username, password = password)

			sftp = paramiko.SFTPClient.from_transport(transport)

			remotepath = '/data/shared_disk{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)

			localpath = '/data/hitme/static/files/' + dir_nme

			inflo(remotepath)
			inflo(localpath)

			res = sftp.get(remotepath = remotepath, localpath = localpath)
			inflo(res)

			sftp.close()
			transport.close()

		return localpath

	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '', 'dir_lst': [] }

	finally:
		try:
			p = Process(target=clr_dir, args=(localpath,))
			p.start()
			# p.join()
		except:
			elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
			return  {'dir_new': '', 'dir_lst': [] }

def clr_dir(localpath):
	try:
		time.sleep(60)
		os.remove(localpath)
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '', 'dir_lst': [] }

def rnm_fil(dir_dta):
	try:

		url = 'http://10.8.0.2/rnm_fil'
		res = requests.post(url = url, data = dir_dta)
		inflo( res.content)
		return res.content
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '', 'dir_lst': [] }
