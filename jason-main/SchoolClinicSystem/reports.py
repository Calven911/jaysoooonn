import customtkinter as ctk
import sqlite3
import csv
from tkinter import messagebox, filedialog
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "clinic.db"


class ReportsWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = parent if parent else ctk.CTk()
        self.app = ctk.CTkFrame(self.root, fg_color="#EAF4FF")
        self.app.pack(fill="both", expand=True)

        self.root.title("School Clinic - Reports")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        header = ctk.CTkFrame(
            self.app,
            height=120,
            corner_radius=0,
            fg_color="#1565C0"
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        if parent:
            ctk.CTkButton(
                header,
                text="← Back to Dashboard",
                width=180,
                height=34,
                fg_color="#0D47A1",
                hover_color="#083675",
                command=self.back_to_dashboard
            ).place(x=24, y=18)

        ctk.CTkLabel(
            header,
            text="📊  CLINIC REPORTS",
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=(25, 3))

        ctk.CTkLabel(
            header,
            text="Patient, Consultation, and Medicine Records",
            font=("Arial", 15),
            text_color="#DDEEFF"
        ).pack()

        summary_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        summary_frame.pack(
            pady=15,
            padx=35,
            fill="x"
        )

        ctk.CTkLabel(
            summary_frame,
            text="SYSTEM SUMMARY",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 5))

        self.summary_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Arial", 14),
            text_color="#34536B",
            justify="left"
        )
        self.summary_label.pack(pady=(0, 15))

        report_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        report_frame.pack(
            pady=(0, 15),
            padx=35,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            report_frame,
            text="CLINIC RECORDS",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 5))

        self.report_text = ctk.CTkTextbox(
            report_frame,
            height=390,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.report_text.pack(
            padx=20,
            pady=5,
            fill="both",
            expand=True
        )

        button_frame = ctk.CTkFrame(
            report_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=(5, 15))

        ctk.CTkButton(
            button_frame,
            text="🔄 REFRESH REPORT",
            width=180,
            height=42,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.load_report
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            button_frame,
            text="📁 EXPORT CSV",
            width=180,
            height=42,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.export_csv
        ).grid(row=0, column=1, padx=8)

        self.load_report()

        if not parent:
            self.root.mainloop()

    def back_to_dashboard(self):
        self.app.destroy()
        if self.parent is not None:
            self.parent._show_dashboard()

    def get_data(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name,
                patient_type,
                contact_number
            FROM patients
            ORDER BY patient_id
        """)
        patients = cursor.fetchall()

        cursor.execute("""
            SELECT
                c.consultation_id,
                c.patient_id,
                p.first_name,
                p.last_name,
                c.consultation_date,
                c.symptoms,
                c.diagnosis,
                c.treatment
            FROM consultations c
            JOIN patients p ON p.patient_id = c.patient_id
            ORDER BY c.consultation_id DESC
        """)
        consultations = cursor.fetchall()

        cursor.execute("""
            SELECT
                medicine_id,
                medicine_name,
                category,
                quantity,
                unit,
                expiration_date
            FROM medicines
            ORDER BY medicine_id
        """)
        medicines = cursor.fetchall()

        connection.close()

        return patients, consultations, medicines

    def load_report(self):
        try:
            (
                patients,
                consultations,
                medicines
            ) = self.get_data()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to load report:\n\n{error}"
            )
            return

        self.summary_label.configure(
            text=(
                f"Total Patients: {len(patients)}     |     "
                f"Consultations: {len(consultations)}     |     "
                f"Medicines: {len(medicines)}"
            )
        )

        self.report_text.delete("1.0", "end")

        self.report_text.insert(
            "end",
            "=== PATIENT RECORDS ===\n\n"
        )

        if patients:
            for patient in patients:
                (
                    patient_id,
                    first_name,
                    last_name,
                    patient_type,
                    contact
                ) = patient

                self.report_text.insert(
                    "end",
                    f"Patient ID: {patient_id}\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Type: {patient_type}\n"
                    f"Contact: {contact or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No patient records found.\n"
            )

        self.report_text.insert(
            "end",
            "\n=== CONSULTATION RECORDS ===\n\n"
        )

        if consultations:
            for record in consultations:
                (
                    consultation_id,
                    patient_id,
                    first_name,
                    last_name,
                    consultation_date,
                    symptoms,
                    diagnosis,
                    treatment
                ) = record

                self.report_text.insert(
                    "end",
                    f"Consultation ID: {consultation_id}\n"
                    f"Patient: {first_name} {last_name} (ID: {patient_id})\n"
                    f"Date: {consultation_date}\n"
                    f"Symptoms: {symptoms or 'N/A'}\n"
                    f"Diagnosis: {diagnosis or 'N/A'}\n"
                    f"Treatment: {treatment or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No consultation records found.\n"
            )

        self.report_text.insert(
            "end",
            "\n=== MEDICINE INVENTORY ===\n\n"
        )

        if medicines:
            for medicine in medicines:
                (
                    medicine_id,
                    name,
                    category,
                    quantity,
                    unit,
                    expiration
                ) = medicine

                self.report_text.insert(
                    "end",
                    f"Medicine ID: {medicine_id}\n"
                    f"Medicine: {name}\n"
                    f"Category: {category or 'N/A'}\n"
                    f"Stock: {quantity} {unit or ''}\n"
                    f"Expiration: {expiration or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No medicine records found.\n"
            )

    def export_csv(self):
        try:
            (
                patients,
                consultations,
                medicines
            ) = self.get_data()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to export report:\n\n{error}"
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Clinic Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "PATIENT RECORDS"
                ])

                writer.writerow([
                    "Patient ID",
                    "First Name",
                    "Last Name",
                    "Patient Type",
                    "Contact Number"
                ])

                writer.writerows(patients)

                writer.writerow([])
                writer.writerow([
                    "CONSULTATION RECORDS"
                ])

                writer.writerow([
                    "Consultation ID",
                    "Patient ID",
                    "Patient Name",
                    "Date",
                    "Symptoms",
                    "Diagnosis",
                    "Treatment"
                ])

                for record in consultations:
                    (
                        consultation_id,
                        patient_id,
                        first_name,
                        last_name,
                        consultation_date,
                        symptoms,
                        diagnosis,
                        treatment
                    ) = record
                    writer.writerow([
                        consultation_id,
                        patient_id,
                        f"{first_name} {last_name}",
                        consultation_date,
                        symptoms,
                        diagnosis,
                        treatment
                    ])

                writer.writerow([])
                writer.writerow([
                    "MEDICINE INVENTORY"
                ])

                writer.writerow([
                    "Medicine ID",
                    "Medicine Name",
                    "Category",
                    "Quantity",
                    "Unit",
                    "Expiration Date"
                ])

                writer.writerows(medicines)

            messagebox.showinfo(
                "Export Successful",
                "Clinic report exported successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Unable to export report:\n\n{error}"
            )


if __name__ == "__main__":
    ReportsWindow()
