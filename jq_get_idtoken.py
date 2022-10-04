# -*- coding: utf-8 -*-
# 2022.10.03 coded by yo.
# MIT License
# Python 3.6.8 / centos7.4

import urllib3
import requests
import datetime
import json
##import time
import sys
from datetime import datetime as dt



# ---------------------------------------------
# 機能 : 起動したディレクトリでファイルに書き込む。
# 引数1: 出力ファイル名（string型）
# 引数2: 出力文字列（string型）
# 返値 : 無し
# ---------------------------------------------
def func_write_to_file(str_fname_output, str_text):
    try:
        with open(str_fname_output, 'w', encoding = 'utf_8') as fout:
            fout.write(str_text)     

    except IOError as e:
        print('Can not Write!!!')
        print(type(e))



# ---------------------------------------------
# 機能 : 起動したディレクトリでファイルに書き込む。
# 引数1: 出力ファイル名（string型）
# 引数2: 出力文字列（string型）
# 返値 : 無し
# ---------------------------------------------
def func_read_from_file(str_fname):
    str_read = ''
    try:
        with open(str_fname, 'r', encoding = 'utf_8') as fin:
            while True:
                line = fin.readline()
                if not len(line):
                    break
                str_read = str_read + line
        return str_read

    except IOError as e:
        print('Can not Write!!!')
        print(type(e))



# =============================================

# 機能 : 保存してあるリフレッシュトークンを使い、IDトークンを取得し保存する。
# 引数 : 無し
# 返値 : 無し
# 備考 : リフレッシュトークンのファイル名、IDトークンを保存するファイル名は適宜変更してください。
# ---------------------------------------------

# ＩＤトークン保存ファイル名
str_fname_output = 'jq_idtoken.json'

# リフレッシュトークンファイル名
str_fname_rftoken = 'jq_rftoken.json'



# リフレッシュトークンの読み出し
str_rf_json = func_read_from_file(str_fname_rftoken)
dic_rf_json = json.loads(str_rf_json)
str_rftoken = dic_rf_json.get('refreshToken')

# ＩＤトークン取得用urlの作成
str_url_auth_refresh = 'https://api.jpx-jquants.com/v1/token/auth_refresh'
##str_url_idtoken = str_url_auth_refresh + '?' + 'refreshtoken=' + str_rftoken
str_url_idtoken = str_url_auth_refresh + '?' + 'refreshtoken=' + str_rftoken


# リフレッシュトークンのタイムスタンプを取得し時間型に変換
str_time_rftoken = dic_rf_json.get('time_rftoken')
time_rftoken = dt.strptime(str_time_rftoken, '%Y-%m-%d %H:%M:%S.%f')

# リフレッシュトークンの有効期限
expire_span = datetime.timedelta(days=7)
time_expire = time_rftoken + expire_span
print('リフレッシュトークンの有効期限')
print('rftoken saved :', time_rftoken)
print('effective date:', time_expire)

time_remain = time_expire - datetime.datetime.now()
print('remaining time:', time_remain)
print('----------------------------------')
print()


# ＩＤトークンを取得した時刻を取得
time_idtoken = datetime.datetime.now()

# IDトークン取得
r_post_idtoken = requests.post(str_url_idtoken)
dic_idtoken = json.loads(r_post_idtoken.text)  # 辞書型に変換
str_idtoken = dic_idtoken.get('idToken')    # ＩＤトークンのvalueを取得
# リフレッシュトークンが正しくない場合、有効期限切れの場合
if str_idtoken is None :
    print(dic_idtoken.get('message'))
    quit()


# 取得時刻とＩＤトークンを保存
# データ形式は、{"time_idtoken":"value","idToken":"value"}
dic_json = {}
dic_json['time_idToken'] = str(time_idtoken)
dic_json['idToken'] = str_idtoken
str_json=json.dumps(dic_json)
func_write_to_file(str_fname_output, str_json)
print('ID token saved :', str_fname_output )
print('format =','{"time_idToken":"YYYY-mm-dd HH:MM:SS.ffffff","idToken":"value"}')
print()
# ＩＤトークンの取得時間を表示
print('time stamp :', time_idtoken)

# ＩＤトークンの有効期限を表示（有効期限24時間）
expire_span = datetime.timedelta(days=1)
expire_time = time_idtoken + expire_span
print('expiry date:', expire_time)
print('IDトークンの有効期間は２４時間です。')

