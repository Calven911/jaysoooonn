
import csv
import sqlite3
from pathlib import Path

DB_FILE = "clinic_demo.db"
CSV_FILE = "sample_patients_250.csv"

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    patients = list(csv.DictReader(file))

if len(patients) != 250:
    raise ValueError(f"Expected 250 patients, found {len(patients)}")

with sqlite3.connect(DB_FILE) as conn:
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executemany("""
        INSERT INTO patient_visits
        (first_name, last_name, patient_type, contact_number)
        VALUES (?, ?, ?, ?)
    """, [
        (
            row["patient_name"].split(" ", 1)[0],
            row["patient_name"].split(" ", 1)[1],
            row["patient_type"],
            ""
        )
        for row in patients
    ])

    total = conn.execute(
        "SELECT COUNT(*) FROM patient_visits"
    ).fetchone()[0]

print(f"Import successful! Total patient records: {total}")