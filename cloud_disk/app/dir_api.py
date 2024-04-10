#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import sys
import os
import traceback
import requests
import json
from flask import Flask, request, Response, render_template, redirect, url_for, make_response
import paramiko
from transliterate import translit
import threading
import time
from multiprocessing import Process
import shutil

def dlog( tgt, msg ):		# w/o print
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def dlog_prn( tgt, msg ):	# with print
	print(msg)
	with open ( tgt, 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def inflo(msg):
	print(msg)
	with open ( '/data/hitme/logs/info.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

def elo(msg):
	print(msg)
	with open ( '/data/hitme/logs/elo.txt', 'a') as fil : fil.write( '{msg}\n'.format( msg = msg ) )

# Функция выдает список содержимого из директории new_dir
def lst_dir(new_dir):
	try:

		dir_lst = os.listdir('{new_dir}'.format(new_dir = new_dir))	# получаем список содержимого директории
		dir_ext = []

		for pth in dir_lst:
			fil_pth = '{new_dir}/{pth}'.format(new_dir = new_dir, pth = pth)
			fil_nme, fil_ext = os.path.splitext(fil_pth) # делим на имя и расширение
			
			if fil_ext == '' and os.path.isdir( fil_pth ): fil_ext = 'Folder' # Определяем что это. Файл или директория

			dir_ext.append({'nme': pth, 'ext': fil_ext}) # добавляем в список название и расширение

		return dir_ext
	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  []

# Переходим в домашнюю директорию
def get_dfl_dir():
	try:		return lst_dir('/data/shared_disk')
	except:		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

# Переход в диркторию
def get_dir(dir_dta):

	try:
		now_dir = dir_dta['now_dir']
		dir_nme = dir_dta['dir_nme']
		dir_lst = []
		if os.path.isdir('/data/shared_disk{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)):
			dir_new = '{now_dir}{dir_nme}/'.format(now_dir = now_dir, dir_nme = dir_nme)	
			dir_lst = lst_dir('/data/shared_disk{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme))
		else:
			dir_lst = lst_dir('/data/shared_disk{now_dir}'.format(now_dir = now_dir))
			dir_new = now_dir

		dta = {'dir_new': dir_new, 'dir_lst': dir_lst }

		return dta

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }

# Удаление файла
def del_fil(dir_dta):

	try:
		now_dir = dir_dta['now_dir']
		dir_nme = dir_dta['dir_nme']
		dir_lst = []
		del_pth = '/data/shared_disk/{now_dir}{dir_nme}'.format(now_dir = now_dir, dir_nme = dir_nme)

		
		if os.path.isfile(del_pth): os.remove(del_pth) # Если удалить надо файл
		else: shutil.rmtree(del_pth) # Если удалить надо директорию

		# обновляем спикок файлов пользователю
		dir_lst = lst_dir('/data/shared_disk/{now_dir}'.format(now_dir = now_dir))
		dir_new = now_dir

		dta = {'dir_new': dir_new, 'dir_lst': dir_lst }

		return dta

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': dir_new, 'dir_lst': [] }


# Сохраняем файл который прислал пользователь
def snt_fil_str(req):
	try:

		fil_req = req.files['file']
		fil_nme = fil_req.filename

		fil_nme = translit(fil_nme, language_code='ru', reversed=True) # Переводим кириллицу на латиницу
		fil_pth = req.form['fil_pth']
		fil_req.save('/data/shared_disk'+ fil_pth + fil_nme)
		
		return 0
	
	except:
		elo('FUCK')
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))

# Возвращаемся на директорию назад
def get_dir_bck(dir_dta):
	try:

		now_dir = dir_dta['now_dir']
		if (now_dir != '/'): 
			try: os.chdir('/data/shared_disk/'+now_dir)
			except: new_dir = '/data/shared_disk'
			new_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir )+ '/'
		else: new_dir = '/data/shared_disk'
		dir_lst = lst_dir(new_dir)
		dta = {'dir_new': new_dir.replace('/data/shared_disk',''), 'dir_lst': dir_lst }

		return dta, 200

	except:
		elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '/data', 'dir_lst': [] }

# Скачивание файла
def dwn_fil(dir_dta):
	try:
		now_dir = dir_dta['now_dir']
		dir_nme = dir_dta['dir_nme']
	
		return '/data/shared_disk'+now_dir+dir_nme
	except:
		elo( '{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0],b=str(sys.exc_info()[1])))
		return  {'dir_new': '', 'dir_lst': [] }


# TODO сделать скачивание 
def get_zip(fil_dct,req):
	try:

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
