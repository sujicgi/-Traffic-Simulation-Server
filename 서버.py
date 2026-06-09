from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('simulation.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        height REAL,
        case_name TEXT,
        impact_energy REAL
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/save', methods=['POST'])
def save():

    data = request.json

    conn = sqlite3.connect('simulation.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO results(height, case_name, impact_energy) VALUES (?, ?, ?)",
        (
            data['height'],
            data['case_name'],
            data['impact_energy']
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"ok"})


@app.route('/results')
def results():

    conn = sqlite3.connect('simulation.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT height, case_name, impact_energy FROM results"
    )

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)