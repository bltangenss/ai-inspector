import sqlite3
import os
import logging

logger = logging.getLogger(__name__)
DB_PATH = os.environ.get("DB_PATH", "inspector.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT,
            label       TEXT,
            ai_prob     REAL,
            real_prob   REAL,
            confidence  TEXT,
            verdict     TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована.")


def save_analysis(filename: str, result: dict):
    conn = get_db()
    conn.execute(
        """INSERT INTO analyses (filename, label, ai_prob, real_prob, confidence, verdict)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (filename, result["label"], result["ai_probability"],
         result["real_probability"], result["confidence"], result["verdict"])
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 20):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM analyses ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
