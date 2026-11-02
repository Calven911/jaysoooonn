import sqlite3

class DatabaseManager:
    def __init__(self, db_name="clinic.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                patient_type TEXT NOT NULL,
                contact_number TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                consultation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                consultation_date TEXT NOT NULL,
                symptoms TEXT,
                diagnosis TEXT,
                treatment TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                unit TEXT,
                expiration_date TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispensing_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                medicine_id INTEGER NOT NULL,
                quantity_dispensed INTEGER NOT NULL,
                dispensing_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
            )
        """)
        
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password)
            VALUES (?, ?)
        """, ("admin", "admin123"))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    database = DatabaseManager()
    database.create_tables()
    print("Clinic database and tables created successfully!")
    
