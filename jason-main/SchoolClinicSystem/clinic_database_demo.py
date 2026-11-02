
import sqlite3

DATABASE_NAME = "clinic_demo.db"


def connect_db():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()

        # Patient visits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_visits (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                patient_type TEXT NOT NULL
                    CHECK (patient_type IN ('Student', 'Faculty', 'Staff')),
                contact_number TEXT
            )
        """)

        # Consultation history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultation_history (
                consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                symptoms TEXT,
                diagnosis TEXT,
                treatment TEXT,
                FOREIGN KEY (patient_id)
                    REFERENCES patient_visits(patient_id)
            )
        """)

        # Medicine inventory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicine_inventory (
                medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
                    CHECK (quantity >= 0),
                unit TEXT NOT NULL,
                expiration_date TEXT NOT NULL
            )
        """)

        # Medicine history: records stock changes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicine_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id INTEGER NOT NULL,
                transaction_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                transaction_type TEXT NOT NULL,
                quantity_changed INTEGER NOT NULL,
                notes TEXT,
                FOREIGN KEY (medicine_id)
                    REFERENCES medicine_inventory(medicine_id)
            )
        """)

        # Reports log: records generated reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        """)

        conn.commit()


def add_patient(first_name, last_name, patient_type,
                contact_number=""):
    with connect_db() as conn:
        cursor = conn.execute("""
            INSERT INTO patient_visits
            (first_name, last_name, patient_type, contact_number)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, patient_type, contact_number))
        return cursor.lastrowid


def add_consultation(patient_id, date, symptoms,
                     diagnosis, treatment):
    with connect_db() as conn:
        conn.execute("""
            INSERT INTO consultation_history
            (patient_id, date, symptoms, diagnosis, treatment)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, date, symptoms, diagnosis, treatment))


def add_medicine(name, category, quantity, unit, expiration_date):
    with connect_db() as conn:
        cursor = conn.execute("""
            INSERT INTO medicine_inventory
            (medicine_name, category, quantity, unit, expiration_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, quantity, unit, expiration_date))
        return cursor.lastrowid


def get_patient_visits():
    with connect_db() as conn:
        return conn.execute("""
            SELECT patient_id, first_name, last_name,
                   patient_type, contact_number
            FROM patient_visits
            ORDER BY patient_id DESC
        """).fetchall()


def get_consultation_history():
    with connect_db() as conn:
        return conn.execute("""
            SELECT c.patient_id, c.date, c.symptoms,
                   c.diagnosis, c.treatment
            FROM consultation_history AS c
            ORDER BY c.date DESC
        """).fetchall()


def get_medicine_history():
    with connect_db() as conn:
        return conn.execute("""
            SELECT medicine_name, category, quantity,
                   unit, expiration_date
            FROM medicine_inventory
            ORDER BY medicine_name
        """).fetchall()


def main():
    create_tables()
    print(f"SQLite database ready: {DATABASE_NAME}")
    print("Tables created successfully!")


if __name__ == "__main__":
    main()