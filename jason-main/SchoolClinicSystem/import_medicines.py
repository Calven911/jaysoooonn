
import csv
import sqlite3

DB_FILE = "clinic_demo.db"
CSV_FILE = "sample_medicines_250 (1).csv"

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
    medicines = list(csv.DictReader(file))

if len(medicines) != 250:
    raise ValueError(f"Expected 250 medicines, found {len(medicines)}")

with sqlite3.connect(DB_FILE) as conn:
    conn.executemany("""
        INSERT INTO medicine_inventory
        (medicine_name, category, quantity, unit, expiration_date)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (
            row["medicine_name"],
            row["category"],
            int(row["quantity"]),
            row["unit"],
            row["expiration_date"]
        )
        for row in medicines
    ])

    total = conn.execute(
        "SELECT COUNT(*) FROM medicine_inventory"
    ).fetchone()[0]

print(f"Import successful! Total medicine records: {total}")