from flask import Flask, request, jsonify
import sqlite3
from flask import render_template

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("simulation.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        users INTEGER,
        stock INTEGER,
        response_time REAL,
        failure_rate REAL,
        oversell INTEGER,
        cache INTEGER,
        queue INTEGER,
        load_balancer INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/save', methods=['POST'])
def save():

    data = request.json

    conn = sqlite3.connect("simulation.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO results(
        users,
        stock,
        response_time,
        failure_rate,
        oversell,
        cache,
        queue,
        load_balancer
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data['users'],
        data['stock'],
        data['responseTime'],
        data['failureRate'],
        data['oversell'],
        int(data['cache']),
        int(data['queue']),
        int(data['loadBalancer'])
    ))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})


@app.route('/results')
def results():

    conn = sqlite3.connect("simulation.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT
        users,
        stock,
        response_time,
        failure_rate,
        oversell
    FROM results
    """)

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

@app.route('/chart')
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    app.run(debug=True)