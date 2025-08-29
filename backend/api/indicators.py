
# Place this file as backend/api/indicators.py
from flask import Blueprint, jsonify, request
import os, pymysql

bp = Blueprint('indicators', __name__, url_prefix='/api')

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

@bp.get('/subindicators/history/<code>')
def history(code):
    limit = int(request.args.get('limit', 200))
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM sub_indicator WHERE code=%s", (code,))
            si = cur.fetchone()
            if not si:
                return jsonify({'error': 'unknown code'}), 404
            cur.execute("""SELECT value, observed_at FROM sub_indicator_history
                           WHERE sub_indicator_id=%s
                           ORDER BY observed_at DESC LIMIT %s""", (si['id'], limit))
            rows = cur.fetchall()
    return jsonify(rows), 200
