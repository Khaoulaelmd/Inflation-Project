
# Place this file as backend/api/agents.py
from flask import Blueprint, jsonify, request
import os, json, pymysql
from datetime import datetime

bp = Blueprint('agents', __name__, url_prefix='/api/agents')

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

@bp.get('/sources')
def list_sources():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM data_source WHERE enabled=1 ORDER BY id DESC")
            rows = cur.fetchall()
    return jsonify(rows), 200

@bp.get('/subindicators')
def list_subs():
    code = request.args.get('code')
    sql = "SELECT * FROM sub_indicator WHERE enabled=1"
    params = ()
    if code:
        sql += " AND code=%s"
        params = (code,)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            subs = cur.fetchall()
            # last value
            for s in subs:
                cur.execute("""SELECT value, observed_at FROM sub_indicator_history 
                               WHERE sub_indicator_id=%s ORDER BY observed_at DESC LIMIT 1""", (s['id'],))
                last = cur.fetchone()
                s['last_value'] = last['value'] if last else None
                s['last_at'] = last['observed_at'] if last else None
    return jsonify(subs), 200

@bp.post('/run/<code>')
def run_now(code):
    # Cette route marque une exécution ad-hoc (le service agents peut surveiller 'ingest_run' pour traiter les 'queued')
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM sub_indicator WHERE code=%s AND enabled=1", (code,))
            row = cur.fetchone()
            if not row:
                return jsonify({'error': 'unknown code'}), 404
            cur.execute("""INSERT INTO ingest_run(sub_indicator_id, started_at, status, message, rows_ingested)
                           VALUES (%s, NOW(), NULL, 'queued by API', 0)""", (row['id'],))
    return jsonify({'status': 'queued'}), 202
