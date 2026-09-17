import pymysql
import pymysql.cursors
from flask import current_app, g


def get_db():
    """Open a new DB connection if none exists for the current app context."""
    if "db" not in g:
        cfg = current_app.config
        g.db = pymysql.connect(
            host=cfg["DB_HOST"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
            database=cfg["DB_NAME"],
            port=cfg["DB_PORT"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=None, fetchone=False):
    """Run a SELECT and return rows (list of dicts) or a single dict."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        if fetchone:
            return cur.fetchone()
        return cur.fetchall()


def execute(sql, params=None):
    """Run an INSERT/UPDATE/DELETE. Returns lastrowid."""
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.lastrowid


def init_app(app):
    app.teardown_appcontext(close_db)
