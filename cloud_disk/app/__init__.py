#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
from dir_api import rnm_fil
from dir_api import chk_con
from dir_api import dwn_fil
from dir_api import del_fil
from dir_api import get_dir
from dir_api import snt_fil_str
from dir_api import get_dir_bck
from dir_api import get_dfl_dir
from flask import Flask, request, Response, render_template, redirect, url_for, make_response, send_file
import traceback
from functools import wraps
import sqlite3
import datetime as dt

import time
import json
import sys

sys.path.append("/data/hitme/app")


def dlog(tgt, msg):		# w/o print
    with open(tgt, 'a') as fil:
        fil.write('{msg}\n'.format(msg=msg))


def dlog_prn(tgt, msg):  # with print
    print(msg)
    with open(tgt, 'a') as fil:
        fil.write('{msg}\n'.format(msg=msg))


def inflo(msg):
    print(msg)
    with open('/data/hitme/logs/req.txt', 'a') as fil:
        fil.write('{msg}\n'.format(msg=msg))


def elo(msg):
    print(msg)
    with open('/data/hitme/logs/elo.txt', 'a') as fil:
        fil.write('{msg}\n'.format(msg=msg))

def req_lo(msg):
    print(msg)
    with open('/data/hitme/logs/req_lo.txt', 'a') as fil:
        fil.write('{msg}\n'.format(msg=msg))

app = Flask(__name__, static_folder='/data/hitme/static/',
            template_folder='templates')
app.config.update(SESSION_COOKIE_SECURE=True,
                  SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',)


@app.route("/dir")
def dir(): return render_template('sha_dir.html')

# ---------------------------------- DIRS API -------------------------------------------------

# функция для проверки коннекта (устарела)
@app.route("/dir/chk_con", methods=['POST'])
def chk_con_api():
    res = chk_con()
    return Response(json.dumps(res))
# переход в домашнюю директорию
@app.route("/dir/get_dfl_dir", methods=['POST'])
def get_dfl_dir_api():

    res = get_dfl_dir()
    
    return Response(json.dumps(res))

# переход в директорию которую выбрал пользователь
@app.route("/dir/get_dir", methods=['POST'])
def get_dir_api():
    try:
        dta = get_dir(request.form)
        return Response(json.dumps({"dta": str(dta).replace("'", '"')}))
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))

# переименовать файл (TODO)
@app.route("/dir/rnm_fil", methods=['POST'])
def rnm_fil_api():
    try:
        dta = rnm_fil(request.form)
        return Response(json.dumps({"dta": str(dta).replace("'", '"')}))
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))

# перейти в директорию назад
@app.route("/dir/get_dir_bck", methods=['POST'])
def get_dir_bck_api():
    try:
        dta, stt = get_dir_bck(request.form)
        if stt == 200: return Response(json.dumps({"dta": str(dta).replace("'", '"'), "res": stt}))
        return Response('', 400)
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))

# Отдать файл пользователю
@app.route("/dir/dwn_fil", methods=['POST'])
def dwn_fil_api():
    try:
        pth = dwn_fil(request.form)
        return Response(json.dumps({"dta": pth}))
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))

# Принять файл от пользователя
@app.route("/dir/snt_fil", methods=['POST'])
def snt_fil_api():
    try:

        snt_fil_str(request)
        return Response(json.dumps({"dta": 'ok'}))
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))
# Удалить файл
@app.route("/dir/del_fil", methods=['POST'])
def del_fil_api():
    try:
        dta = del_fil(request.form)
        return Response(json.dumps({"dta": str(dta).replace("'", '"')}))
    except:
        elo('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1])))
        return Response(json.dumps({"dta": str('{a}\n{b}'.format(a=traceback.format_tb(sys.exc_info()[2])[0], b=str(sys.exc_info()[1]))).replace("'", '"')}))
