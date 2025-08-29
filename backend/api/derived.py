
# Place this file as backend/api/derived.py
from flask import Blueprint, jsonify, request
import os, pymysql
from datetime import datetime

bp = Blueprint('derived', __name__, url_prefix='/api/derived')

def parse_mysql_url(url: str):
    assert url.startswith('mysql+pymysql://')
    body = url[len('mysql+pymysql://'):]
    userpass, hostdb = body.split('@', 1)
    if ':' in userpass:
        user, password = userpass.split(':', 1)
    else:
        user, password = userpass, ''
    if '/' in hostdb:
        hostport, dbname_qs = hostdb.split('/', 1)
    else:
        hostport, dbname_qs = hostdb, 'inflation_db'
    if '?' in dbname_qs:
        dbname, _ = dbname_qs.split('?', 1)
    else:
        dbname = dbname_qs
    if ':' in hostport:
        host, port = hostport.split(':', 1)
        port = int(port)
    else:
        host, port = hostport, 3306
    return {'user': user, 'password': password, 'host': host, 'port': int(port), 'db': dbname}

def get_conn():
    DB = parse_mysql_url(os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/inflation_db'))
    return pymysql.connect(host=DB['host'], port=DB['port'], user=DB['user'], password=DB['password'],
                           database=DB['db'], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

@bp.get('/<code>')
def get_latest(code):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT code, value, observed_at
                            FROM derived_indicator
                            WHERE code=%s
                            ORDER BY observed_at DESC LIMIT 1""", (code,))
            row = cur.fetchone() or {}
    return jsonify(row), 200

@bp.get('/')
def list_codes():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT code, MAX(observed_at) AS last_at
                            FROM derived_indicator
                            GROUP BY code
                            ORDER BY code""")
            rows = cur.fetchall()
    return jsonify(rows), 200
