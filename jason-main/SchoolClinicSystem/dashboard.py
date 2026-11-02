
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "clinic.db"


class DashboardWindow:
    def __init__(self):
        self.app = ctk.CTk()

        self.app.title("School Clinic Management System")
        self.app.geometry("1100x700")
        self.app.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app.configure(fg_color="#EAF4FF")
        self.stat_labels = {}

        # =========================
        # GET DATABASE STATISTICS
        # =========================
        total_patients, total_consultations, total_medicines, low_stock = (
            self.get_statistics()
        )

        # =========================
        # SIDEBAR
        # =========================
        sidebar = ctk.CTkFrame(
            self.app,
            width=250,
            corner_radius=0,
            fg_color="#1565C0"
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = ctk.CTkLabel(
            sidebar,
            text="🏥",
            font=("Arial", 42)
        )
        logo.pack(pady=(45, 5))

        clinic_label = ctk.CTkLabel(
            sidebar,
            text="SCHOOL CLINIC",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        clinic_label.pack()

        system_label = ctk.CTkLabel(
            sidebar,
            text="Management System",
            font=("Arial", 13),
            text_color="#DDEEFF"
        )
        system_label.pack(pady=(0, 45))

        patient_button = ctk.CTkButton(
            sidebar,
            text="👤  Patient Visits",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_patient_visits
        )
        patient_button.pack(pady=7)

        medicine_button = ctk.CTkButton(
            sidebar,
            text="💊  Medicine Inventory",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_medicine_inventory
        )
        medicine_button.pack(pady=7)

        consultation_button = ctk.CTkButton(
            sidebar,
            text="📋  Consultation",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_consultation
        )
        consultation_button.pack(pady=7)

        report_button = ctk.CTkButton(
            sidebar,
            text="📊  Reports",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_reports
        )
        report_button.pack(pady=7)

        # =========================
        # LOG OUT BUTTON
        # =========================
        logout_button = ctk.CTkButton(
            sidebar,
            text="🚪  Log Out",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#B71C1C",
            hover_color="#8E0000",
            anchor="w",
            command=self.logout
        )
        logout_button.pack(side="bottom", pady=25)

        # =========================
        # MAIN CONTENT
        # =========================
        content = ctk.CTkFrame(
            self.app,
            corner_radius=0,
            fg_color="#EAF4FF"
        )
        content.pack(side="right", fill="both", expand=True)
        self.dashboard_frames = (sidebar, content)
        self.app._show_dashboard = self.show_dashboard
        self.app._show_medicine_inventory = self.show_medicine_inventory
        self.app._show_consultation = self.show_consultation

        welcome = ctk.CTkLabel(
            content,
            text="Welcome to the Clinic Dashboard",
            font=("Arial", 30, "bold"),
            text_color="#123B66"
        )
        welcome.pack(anchor="w", padx=45, pady=(50, 5))

        subtitle = ctk.CTkLabel(
            content,
            text=(
                "Manage patients, consultations, medicines, "
                "and clinic reports."
            ),
            font=("Arial", 16),
            text_color="#55708A"
        )
        subtitle.pack(anchor="w", padx=45, pady=(0, 35))

        # =========================
        # STATISTICS CARDS
        # =========================
        cards_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=40)

        self.create_card(
            cards_frame, "👤", str(total_patients),
            "Total Patients", 0
        )

        self.create_card(
            cards_frame, "📋", str(total_consultations),
            "Consultations", 1
        )

        self.create_card(
            cards_frame, "💊", str(total_medicines),
            "Medicines", 2
        )

        self.create_card(
            cards_frame, "⚠️", str(low_stock),
            "Low Stock", 3
        )

        # Consultation and reports are grouped here, with the latest visits
        # beside the actions for adding a consultation or opening full reports.
        records_panel = ctk.CTkFrame(
            content,
            corner_radius=18,
            fg_color="white"
        )
        records_panel.pack(fill="both", expand=True, padx=45, pady=(25, 30))

        ctk.CTkLabel(
            records_panel,
            text="CONSULTATION & REPORTS",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        records_body = ctk.CTkFrame(records_panel, fg_color="transparent")
        records_body.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        records_body.grid_columnconfigure(0, weight=3)
        records_body.grid_columnconfigure(1, weight=2)
        records_body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            records_body,
            text="Recent consultations",
            font=("Arial", 14, "bold"),
            text_color="#34536B"
        ).grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 5))

        self.recent_consultations = ctk.CTkTextbox(
            records_body, height=120, corner_radius=8, font=("Arial", 12)
        )
        self.recent_consultations.grid(
            row=1, column=0, sticky="nsew", padx=(0, 12)
        )

        actions = ctk.CTkFrame(records_body, corner_radius=10, fg_color="#F3F8FD")
        actions.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(8, 0))
        ctk.CTkLabel(
            actions,
            text="Quick actions",
            font=("Arial", 14, "bold"),
            text_color="#34536B"
        ).pack(anchor="w", padx=15, pady=(15, 8))
        ctk.CTkButton(
            actions,
            text="＋  New Consultation",
            command=self.open_consultation
        ).pack(fill="x", padx=15, pady=6)
        ctk.CTkButton(
            actions,
            text="📊  View Reports",
            command=self.open_reports
        ).pack(fill="x", padx=15, pady=6)

        self.refresh_recent_consultations()

        self.app.mainloop()

    # =========================
    # DATABASE STATISTICS
    # =========================
    def get_statistics(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM consultations")
        total_consultations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM medicines WHERE quantity <= 5"
        )
        low_stock = cursor.fetchone()[0]

        connection.close()

        return (
            total_patients,
            total_consultations,
            total_medicines,
            low_stock
        )

    def refresh_recent_consultations(self):
        connection = sqlite3.connect(DATABASE_PATH)
        try:
            records = connection.execute(
                """
                SELECT c.consultation_date, p.first_name, p.last_name,
                       c.symptoms, c.treatment
                FROM consultations c
                JOIN patients p ON p.patient_id = c.patient_id
                ORDER BY c.consultation_id DESC
                LIMIT 5
                """
            ).fetchall()
        finally:
            connection.close()

        self.recent_consultations.delete("1.0", "end")
        if not records:
            self.recent_consultations.insert("end", "No consultations recorded yet.")
            return

        for visit_date, first_name, last_name, symptoms, treatment in records:
            self.recent_consultations.insert(
                "end",
                f"{visit_date}  |  {first_name} {last_name}\n"
                f"Symptoms: {symptoms or 'N/A'}\n"
                f"Treatment: {treatment or 'N/A'}\n\n"
            )

    # =========================
    # DASHBOARD CARDS
    # =========================
    def create_card(self, parent, icon, number, title, column):
        card = ctk.CTkFrame(
            parent,
            width=150,
            height=150,
            corner_radius=18,
            fg_color="white"
        )
        card.grid(row=0, column=column, padx=6)
        card.grid_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        )
        icon_label.pack(pady=(15, 0))

        number_label = ctk.CTkLabel(
            card,
            text=number,
            font=("Arial", 26, "bold"),
            text_color="#1565C0"
        )
        number_label.pack()
        self.stat_labels[title] = number_label

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12),
            text_color="#55708A"
        )
        title_label.pack(pady=2)

    # =========================
    # NAVIGATION
    # =========================
    def open_patient_visits(self):
        from patient_visits import PatientVisitsWindow
        self.hide_dashboard()
        PatientVisitsWindow(self.app)

    def open_medicine_inventory(self):
        self.show_medicine_inventory()

    def open_consultation(self):
        self.show_consultation()

    def open_reports(self):
        from reports import ReportsWindow
        self.hide_dashboard()
        ReportsWindow(self.app)

    def hide_dashboard(self):
        for frame in self.dashboard_frames:
            frame.pack_forget()

    def show_dashboard(self):
        self.app.title("School Clinic Management System")
        stats = self.get_statistics()
        for title, value in zip(
            ("Total Patients", "Consultations", "Medicines", "Low Stock"),
            stats
        ):
            self.stat_labels[title].configure(text=str(value))
        self.refresh_recent_consultations()

        sidebar, content = self.dashboard_frames
        sidebar.pack(side="left", fill="y")
        content.pack(side="right", fill="both", expand=True)

    def show_medicine_inventory(self, patient_info=None):
        from medicine_inventory import MedicineInventoryWindow
        self.hide_dashboard()
        MedicineInventoryWindow(self.app, patient_info=patient_info)

    def show_consultation(self, patient_info=None):
        from consultation import ConsultationWindow
        self.hide_dashboard()
        ConsultationWindow(self.app, patient_info=patient_info)

    # =========================
    # LOG OUT
    # =========================
    def logout(self):
        should_logout = messagebox.askyesno(
            "Confirm Log Out",
            "Are you sure you want to log out?",
            parent=self.app
        )

        if not should_logout:
            return

        self.app.destroy()

        from login import LoginWindow
        LoginWindow()


if __name__ == "__main__":
    DashboardWindow()
