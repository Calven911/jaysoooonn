import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from models import Patient

class PatientVisitsWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = parent if parent else ctk.CTk()
        self.app = ctk.CTkFrame(self.root, fg_color="#EAF4FF")
        self.app.pack(fill="both", expand=True)

        self.root.title("School Clinic - Patient Visits")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        self.selected_patient_id = None

        # =========================
        # HEADER
        # =========================

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

        title = ctk.CTkLabel(
            header,
            text="👤  PATIENT VISITS",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        title.pack(pady=(25, 3))

        subtitle = ctk.CTkLabel(
            header,
            text="Patient Visit Management",
            font=("Arial", 15),
            text_color="#DDEEFF"
        )
        subtitle.pack()

        # =========================
        # FORM CARD
        # =========================

        form_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        form_frame.pack(
            pady=20,
            padx=35,
            fill="x"
        )

        form_title = ctk.CTkLabel(
            form_frame,
            text="PATIENT INFORMATION",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            pady=(18, 10)
        )

        # First Name
        ctk.CTkLabel(
            form_frame,
            text="First Name",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=1, column=0, padx=15, pady=8)

        self.first_name_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter first name"
        )
        self.first_name_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # Last Name
        ctk.CTkLabel(
            form_frame,
            text="Last Name",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=1, column=2, padx=15, pady=8)

        self.last_name_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter last name"
        )
        self.last_name_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        # Patient Type
        ctk.CTkLabel(
            form_frame,
            text="Patient Type",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=2, column=0, padx=15, pady=8)

        self.patient_type_menu = ctk.CTkComboBox(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            values=["Student", "Faculty", "Staff"]
        )
        self.patient_type_menu.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )
        self.patient_type_menu.set("Student")

        # Contact
        ctk.CTkLabel(
            form_frame,
            text="Contact Number",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=2, column=2, padx=15, pady=8)

        self.contact_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter contact number",
            validate="key",
            validatecommand=(
                self.root.register(self.validate_contact_number),
                "%P"
            )
        )
        self.contact_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=8
        )

        # =========================
        # BUTTONS
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=(12, 20)
        )

        ctk.CTkButton(
            button_frame,
            text="ADD PATIENT",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.add_patient
        ).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            button_frame,
            text="UPDATE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.update_patient
        ).grid(row=0, column=1, padx=6)

        ctk.CTkButton(
            button_frame,
            text="DELETE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#C62828",
            hover_color="#8E0000",
            font=("Arial", 13, "bold"),
            command=self.delete_patient
        ).grid(row=0, column=2, padx=6)

        ctk.CTkButton(
            button_frame,
            text="CLEAR",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#607D8B",
            hover_color="#455A64",
            font=("Arial", 13, "bold"),
            command=self.clear_fields
        ).grid(row=0, column=3, padx=6)

        # =========================
        # PATIENT LIST CARD
        # =========================

        list_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        list_frame.pack(
            pady=(0, 20),
            padx=35,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            list_frame,
            text="REGISTERED PATIENTS",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 8))

        self.patient_list = ctk.CTkTextbox(
            list_frame,
            width=900,
            height=150,
            corner_radius=10,
            font=("Arial", 13)
        )
        self.patient_list.pack(
            padx=20,
            pady=5,
            fill="both",
            expand=True
        )

        # =========================
        # SELECT PATIENT
        # =========================

        select_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent"
        )
        select_frame.pack(pady=(5, 15))

        ctk.CTkLabel(
            select_frame,
            text="Patient ID:",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=0, column=0, padx=8)

        self.patient_id_entry = ctk.CTkEntry(
            select_frame,
            width=150,
            height=38,
            corner_radius=8,
            placeholder_text="Patient ID"
        )
        self.patient_id_entry.grid(
            row=0,
            column=1,
            padx=8
        )

        ctk.CTkButton(
            select_frame,
            text="SELECT PATIENT",
            width=160,
            height=38,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.select_patient
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        self.load_patients()

        if parent is None:
            self.root.mainloop()

    def back_to_dashboard(self):
        self.app.destroy()
        if self.parent is not None:
            self.parent._show_dashboard()

    @staticmethod
    def validate_contact_number(value):
        return value.isdigit() or value == ""

    # =========================
    # ADD PATIENT
    # =========================

    
    def add_patient(self):
        print("DEBUG: ADD PATIENT BUTTON CLICKED")

        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        patient_type = self.patient_type_menu.get()
        contact_number = self.contact_entry.get().strip()

        if not first_name or not last_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the patient's first name and last name."
            )
            return

        patient = Patient(
            patient_id=None,
            first_name=first_name,
            last_name=last_name,
            patient_type=patient_type,
            contact_number=contact_number
        )

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patients
            (first_name, last_name, patient_type, contact_number)
            VALUES (?, ?, ?, ?)
        """, (
            patient.first_name,
            patient.last_name,
            patient.patient_type,
            patient.contact_number
        ))

        patient_id = cursor.lastrowid
        connection.commit()
        connection.close()
        patient_info = {
            "patient_id": patient_id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "patient_type": patient.patient_type,
            "contact_number": patient.contact_number,
        }

        self.clear_fields()
        self.load_patients()

        if self.parent is not None:
            self.app.destroy()
            self.parent._show_consultation(patient_info)

    # =========================
    # LOAD PATIENTS
    # =========================

    def load_patients(self):
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT patient_id,
                   first_name,
                   last_name,
                   patient_type,
                   contact_number
            FROM patients
            ORDER BY patient_id DESC
        """)

        patients = cursor.fetchall()
        connection.close()

        self.patient_list.delete("1.0", "end")

        if not patients:
            self.patient_list.insert(
                "end",
                "No patients registered yet."
            )
            return

        for patient in patients:
            patient_id, first_name, last_name, patient_type, contact = patient

            self.patient_list.insert(
                "end",
                f"ID: {patient_id}\n"
                f"Name: {first_name} {last_name}\n"
                f"Type: {patient_type}\n"
                f"Contact: {contact}\n"
                f"{'-' * 60}\n"
            )

    # =========================
    # SELECT PATIENT
    # =========================

    def select_patient(self):
        patient_id = self.patient_id_entry.get().strip()

        if not patient_id:
            messagebox.showwarning(
                "Missing ID",
                "Please enter a Patient ID."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT first_name,
                   last_name,
                   patient_type,
                   contact_number
            FROM patients
            WHERE patient_id = ?
        """, (patient_id,))

        patient = cursor.fetchone()
        connection.close()

        if patient is None:
            messagebox.showerror(
                "Not Found",
                "Patient ID not found."
            )
            return

        self.selected_patient_id = patient_id

        self.first_name_entry.delete(0, "end")
        self.first_name_entry.insert(0, patient[0])

        self.last_name_entry.delete(0, "end")
        self.last_name_entry.insert(0, patient[1])

        self.patient_type_menu.set(patient[2])

        self.contact_entry.delete(0, "end")
        self.contact_entry.insert(0, patient[3] or "")

        messagebox.showinfo(
            "Patient Selected",
            f"Patient ID {patient_id} is selected."
        )

    # =========================
    # UPDATE PATIENT
    # =========================

    def update_patient(self):
        if self.selected_patient_id is None:
            messagebox.showwarning(
                "No Patient Selected",
                "Please select a patient first."
            )
            return

        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        patient_type = self.patient_type_menu.get()
        contact_number = self.contact_entry.get().strip()

        if not first_name or not last_name:
            messagebox.showwarning(
                "Missing Information",
                "First name and last name are required."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE patients
            SET first_name = ?,
                last_name = ?,
                patient_type = ?,
                contact_number = ?
            WHERE patient_id = ?
        """, (
            first_name,
            last_name,
            patient_type,
            contact_number,
            self.selected_patient_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Patient information updated successfully!"
        )

        self.clear_fields()
        self.load_patients()

    # =========================
    # DELETE PATIENT
    # =========================

    def delete_patient(self):
        if self.selected_patient_id is None:
            messagebox.showwarning(
                "No Patient Selected",
                "Please select a patient first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this patient?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM patients
            WHERE patient_id = ?
        """, (self.selected_patient_id,))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Patient deleted successfully!"
        )

        self.clear_fields()
        self.load_patients()

    # =========================
    # CLEAR
    # =========================

    def clear_fields(self):
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.contact_entry.delete(0, "end")
        self.patient_id_entry.delete(0, "end")

        self.patient_type_menu.set("Student")
        self.selected_patient_id = None


if __name__ == "__main__":
    PatientVisitsWindow()
