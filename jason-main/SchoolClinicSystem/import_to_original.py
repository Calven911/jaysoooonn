
import csv
import sqlite3
import shutil
from pathlib import Path

DB_FILE = "clinic.db"
CSV_FILE = "sample_patients_250.csv"
BACKUP_FILE = "clinic_backup_before_phone_numbers.db"


def main():
    if not Path(DB_FILE).exists():
        raise FileNotFoundError(f"Missing database: {DB_FILE}")

    if not Path(CSV_FILE).exists():
        raise FileNotFoundError(f"Missing CSV: {CSV_FILE}")

    # Preserve an existing backup; never overwrite it.
    if not Path(BACKUP_FILE).exists():
        shutil.copy2(DB_FILE, BACKUP_FILE)
        print(f"Backup created: {BACKUP_FILE}")
    else:
        print(f"Existing backup preserved: {BACKUP_FILE}")

    with open(CSV_FILE, newline="", encoding="utf-8-sig") as file:
        patients = list(csv.DictReader(file))

    conn = sqlite3.connect(DB_FILE)

    try:
        updated = 0
        unmatched = 0

        with conn:
            for row in patients:
                parts = row["patient_name"].strip().split(maxsplit=1)
                first_name = parts[0] if parts else "Sample"
                last_name = parts[1] if len(parts) > 1 else "Patient"

                matches = conn.execute(
                    """
                    SELECT patient_id, contact_number
                    FROM patients
                    WHERE first_name = ? AND last_name = ?
                    """,
                    (first_name, last_name),
                ).fetchall()

                if not matches:
                    unmatched += 1
                    continue

                for patient_id, current_phone in matches:
                    if current_phone and current_phone.strip():
                        continue

                    # Clearly fictional demo contact, not a real phone number.
                    demo_phone = f"DEMO-{patient_id:04d}"

                    conn.execute(
                        """
                        UPDATE patients
                        SET contact_number = ?
                        WHERE patient_id = ?
                          AND (contact_number IS NULL
                               OR TRIM(contact_number) = '')
                        """,
                        (demo_phone, patient_id),
                    )
                    updated += 1

        print("Update completed.")
        print(f"Patient records updated: {updated}")
        print(f"Sample names not matched: {unmatched}")
        print(
            "Existing contact entries were preserved. "
            "DEMO entries are placeholders, not usable phone numbers."
        )

    finally:
        conn.close()


if __name__ == "__main__":
    main()
