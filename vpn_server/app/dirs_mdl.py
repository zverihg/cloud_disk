#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8

import sys
import os
import traceback
import requests
from transliterate import translit
import shutil

reload( sys )
sys.setdefaultencoding( 'utf8' )

def dlog( tgt, msg ):		# w/o print
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog_prn( tgt, msg ):	# with print
	print msg
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def elo(msg):
	print msg
	with open( '/data/hitme/logs/elo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )
	
def inflo(msg):
	print msg
	with open( '/data/hitme/logs/inflo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def lst_dir(new_dir):
	try:
		dir_lst = os.listdir('{new_dir}'.format(new_dir = new_dir))	
		dir_ext = []
		for pth in dir_lst:
			fil_pth = '{new_dir}/{pth}'.format(new_dir = new_dir, pth = pth)
			fil_nme, fil_ext = os.path.splitext(fil_pth)
			if fil_ext == '' and os.path.isdir( fil_pth ): fil_ext = 'Folder'
			dir_ext.append({'nme': pth, 'ext': fil_ext})
		return dir_ext
	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  []

def get_dfl_dir():
	try:		return lst_dir('/data/shared_disk')
	except:		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

def get_dir(dir_dta):

	try:
		now_dir = dir_dta['now_dir'][0].encode('utf-8')
		dir_nme = dir_dta['dir_nme'][0].encode('utf-8')
		dir_lst = []
		inflo(dir_nme)
		if os.path.isdir('/data/shared_disk/{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)):
			dir_new = '{now_dir}{dir_nme}/'.format(now_dir = now_dir, dir_nme = dir_nme)	
			dir_lst = lst_dir('/data/shared_disk/{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme))
		else:
			dir_lst = lst_dir('/data/shared_disk/{now_dir}'.format(now_dir = now_dir))
			dir_new = now_dir

		dta = {'dir_new': dir_new, 'dir_lst': dir_lst }

		return dta

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

def del_fil(dir_dta):

	try:
		now_dir = dir_dta['now_dir'][0].encode('utf-8')
		dir_nme = dir_dta['dir_nme'][0].encode('utf-8')
		dir_lst = []
		del_pth = '/data/shared_disk/{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)

		if os.path.isfile(del_pth): os.remove(del_pth) 
		else: shutil.rmtree(del_pth)

		dir_lst = lst_dir('/data/shared_disk/{now_dir}'.format(now_dir = now_dir))
		dir_new = now_dir

		dta = {'dir_new': dir_new, 'dir_lst': dir_lst }

		return dta

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }


def get_dir_bck(dir_dta):
	try:

		now_dir = dir_dta['now_dir'][0].encode('utf-8')
		if (now_dir != '/'):
			inflo('\n\n'+now_dir)
			inflo(os.getcwd())
			try: os.chdir('/data/shared_disk/'+now_dir)
			except: new_dir = '/data/shared_disk'
			inflo(os.getcwd())
			new_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir )+ '/'
		else: new_dir = '/data/shared_disk'
		dir_lst = lst_dir(new_dir)
		dta = {'dir_new': new_dir.replace('/data/shared_disk',''), 'dir_lst': dir_lst }

		return dta

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '/data', 'dir_lst': [] }


def rnm_fil(dir_dta):
	try:
		inflo(dir_dta)
		new_nme = dir_dta['new_nme'][0]
		old_nme = dir_dta['old_nme'][0]
		rnm_dir = dir_dta['rnm_dir'][0]


		new_nme = translit(new_nme, language_code='ru', reversed=True)


		inflo(rnm_dir + new_nme)
		inflo(rnm_dir + old_nme)


		old = '/data/shared_disk' + rnm_dir + old_nme
		new = '/data/shared_disk' + rnm_dir + new_nme


		# os.rename(rnm_dir + old_nme, rnm_dir + new_nme)
		os.rename(old, new)



	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '/data', 'dir_lst': [] }


def get_zip(fil_dct,req):
	try:

		inflo(fil_dct)
		now_dir = fil_dct['now_dir'][0]
		dir_nme = fil_dct['dir_nme'][0]
		
		new_nme = translit(dir_nme, language_code='ru', reversed=True)
		pth = '/data/shared_disk{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)
		output_filename = '/data/shared_disk{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = new_nme)

		shutil.make_archive(output_filename, 'zip', pth)

		return output_filename + '.zip'

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  0


def snt_fil_str(fil_dct,req):
	try:
	
		fil_pth = fil_dct['fil_pth'][0]
		fil_nme = fil_dct['fil_nme'][0]
		ful_pth = '/data/shared_disk{fil_pth}'.format(fil_pth = fil_pth)

		fil_req = req.files['upload_file']
		fil_req.save(os.path.join(ful_pth, fil_nme))

		return 1

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  0

