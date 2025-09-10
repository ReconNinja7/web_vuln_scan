from flask import Flask, render_template, request, redirect, url_for, flash
from scanner.crawler import Crawler
from scanner.tests import ScannerEngine
import sqlite3
import os
from datetime import datetime

DB = "results.db"
app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret"

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE scans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target TEXT,
                        started_at TEXT
                     )''')
        c.execute('''CREATE TABLE findings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        scan_id INTEGER,
                        url TEXT,
                        param TEXT,
                        vuln_type TEXT,
                        evidence TEXT,
                        severity TEXT
                     )''')
        conn.commit()
        conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target = request.form.get("target").strip()
        max_pages = int(request.form.get("max_pages", 30))
        if not target:
            flash("Please enter a target URL (with http:// or https://)")
            return redirect(url_for("index"))

        # start scan
        started_at = datetime.utcnow().isoformat()
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO scans (target, started_at) VALUES (?, ?)", (target, started_at))
        scan_id = c.lastrowid
        conn.commit()
        conn.close()

        crawler = Crawler(target=target, max_pages=max_pages)
        pages_and_forms = crawler.crawl()
        engine = ScannerEngine()
        findings = []
        for item in pages_and_forms:
            url = item["url"]
            forms = item.get("forms", [])
            # test forms
            for form in forms:
                results = engine.test_form(url, form)
                for r in results:
                    findings.append((scan_id, url, r['param'], r['vuln'], r['evidence'], r['severity']))

        # save findings
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.executemany("INSERT INTO findings (scan_id, url, param, vuln_type, evidence, severity) VALUES (?, ?, ?, ?, ?, ?)",
                      findings)
        conn.commit()
        conn.close()

        flash(f"Scan completed: {len(findings)} findings.")
        return redirect(url_for("scan_result", scan_id=scan_id))
    return render_template("index.html")

@app.route("/scan/<int:scan_id>")
def scan_result(scan_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT target, started_at FROM scans WHERE id=?", (scan_id,))
    scan = c.fetchone()
    c.execute("SELECT url, param, vuln_type, evidence, severity FROM findings WHERE scan_id=?", (scan_id,))
    findings = c.fetchall()
    conn.close()
    return render_template("scan_result.html", scan_id=scan_id, scan=scan, findings=findings)

@app.route("/history")
def history():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, target, started_at FROM scans ORDER BY id DESC")
    scans = c.fetchall()
    conn.close()
    return render_template("scan_history.html", scans=scans)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5050)  

