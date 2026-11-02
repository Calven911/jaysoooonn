import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import date, datetime
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "clinic.db"

# Match the consultation symptom choices to the inventory categories used by
# clinic.db. Medicine selection remains limited to available, unexpired stock.
SYMPTOM_CATEGORY_KEYWORDS = {
    "headache": ("pain", "analgesic"),
    "stomachache": ("antacid", "acid reducer", "antispasmodic", "anti-gas"),
    "eye pain": ("eye care",),
    "toothache": ("pain", "analgesic"),
    "fever": ("antipyretic", "analgesic"),
    "cough": ("cough", "mucolytic", "expectorant"),
    "allergy / pangangati": ("antihistamine",),
    "sipon / baradong ilong": ("nasal care", "antihistamine"),
    "pagtatae": ("antidiarrheal", "rehydration"),
    "constipation / hirap dumumi": ("laxative",),
    "heartburn / maasim ang sikmura": ("antacid", "acid reducer"),
    "kabag": ("anti-gas", "antispasmodic"),
    "minor wound / sugat": ("first aid", "antiseptic"),
    "burn / paso": ("first aid", "skin care", "skin protectant"),
    "skin irritation / pantal": ("skin care", "skin protectant"),
    "dry / irritated eyes": ("eye care",),
    "earwax / baradong tainga": ("ear care",),
    "vitamin supplementation": ("vitamin",),
    "nutritional supplementation": ("supplement", "mineral supplement"),
    "iron supplementation": ("iron supplement",),
}


class ConsultationWindow:
    def __init__(self, parent=None, patient_info=None):
        self.parent = parent
        self.patient_info = patient_info
        self.root = parent if parent else ctk.CTk()
        self.app = ctk.CTkFrame(self.root, fg_color="#EAF4FF")
        self.app.pack(fill="both", expand=True)

        self.root.title("School Clinic - Consultation")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        self.selected_consultation_id = None
        self.medicine_options = []

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
            text="📋  CONSULTATION",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        title.pack(pady=(25, 3))

        subtitle = ctk.CTkLabel(
            header,
            text=(
                f"Patient: {patient_info['first_name']} "
                f"{patient_info['last_name']}  |  "
                f"Type: {patient_info['patient_type']}  |  "
                f"Contact: {patient_info['contact_number'] or 'N/A'}"
                if patient_info else "Patient Consultation and Visit History"
            ),
            font=("Arial", 15),
            text_color="#DDEEFF"
        )
        subtitle.pack()

        content_frame = ctk.CTkScrollableFrame(
            self.app,
            fg_color="#EAF4FF"
        )
        content_frame.pack(fill="both", expand=True)

        # =========================
        # FORM CARD
        # =========================

        form_frame = ctk.CTkFrame(
            content_frame,
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
            text="CONSULTATION INFORMATION",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            pady=(18, 10)
        )

        self.patient_summary_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Arial", 13, "bold"),
            text_color="#34536B",
            anchor="w"
        )
        self.patient_summary_label.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=20,
            pady=(0, 8),
            sticky="ew"
        )

        # Patient ID
        ctk.CTkLabel(
            form_frame,
            text="Patient ID",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=8
        )

        self.patient_id_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter Patient ID"
        )
        self.patient_id_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        if patient_info:
            self.patient_id_entry.insert(0, str(patient_info["patient_id"]))
            self.set_patient_summary(patient_info)
        else:
            self.patient_summary_label.configure(
                text="Patient information will appear here after entering a valid Patient ID."
            )
        self.patient_id_entry.bind(
            "<FocusOut>",
            lambda _event: self.update_patient_summary(
                self.patient_id_entry.get().strip()
            )
        )

        # Date
        ctk.CTkLabel(
            form_frame,
            text="Date",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=8
        )

        self.date_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8
        )
        self.date_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=8
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )

        # Symptoms
        ctk.CTkLabel(
            form_frame,
            text="Symptoms",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=8
        )

        self.symptoms_entry = ctk.CTkComboBox(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            values=self.load_symptom_options(),
            command=self.on_symptom_selected
        )
        self.symptoms_entry.set("Select symptom")
        self.symptoms_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )

        # Treatment
        ctk.CTkLabel(
            form_frame,
            text="Treatment",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=4,
            column=0,
            padx=15,
            pady=8
        )

        self.treatment_entry = ctk.CTkComboBox(
            form_frame,
            width=450,
            height=38,
            corner_radius=8,
            values=[],
            state="readonly"
        )
        self.treatment_entry.set("Select staff-approved medicine")
        self.treatment_entry.grid(
            row=4,
            column=1,
            columnspan=3,
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            form_frame,
            text=(
                "Automatic matching uses only in-stock, unexpired medicines "
                "matched to the symptom from available, unexpired clinic stock."
            ),
            font=("Arial", 11),
            text_color="#55708A"
        ).grid(
            row=5,
            column=1,
            columnspan=3,
            padx=10,
            pady=(0, 4),
            sticky="w"
        )

        # =========================
        # BUTTONS
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=6,
            column=0,
            columnspan=4,
            pady=(12, 20)
        )

        ctk.CTkButton(
            button_frame,
            text="ADD RECORD",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.add_consultation
        ).grid(
            row=0,
            column=0,
            padx=6
        )

        ctk.CTkButton(
            button_frame,
            text="UPDATE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.update_consultation
        ).grid(
            row=0,
            column=1,
            padx=6
        )

        ctk.CTkButton(
            button_frame,
            text="DELETE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#C62828",
            hover_color="#8E0000",
            font=("Arial", 13, "bold"),
            command=self.delete_consultation
        ).grid(
            row=0,
            column=2,
            padx=6
        )

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
        ).grid(
            row=0,
            column=3,
            padx=6
        )

        # =========================
        # CONSULTATION HISTORY
        # =========================

        list_frame = ctk.CTkFrame(
            content_frame,
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
            text="CONSULTATION",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 8))

        self.consultation_list = ctk.CTkTextbox(
            list_frame,
            height=185,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.consultation_list.pack(
            padx=20,
            pady=5,
            fill="both",
            expand=True
        )

        # =========================
        # SELECT RECORD
        # =========================

        select_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent"
        )
        select_frame.pack(pady=(5, 15))

        ctk.CTkLabel(
            select_frame,
            text="Consultation ID:",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        self.consultation_id_entry = ctk.CTkEntry(
            select_frame,
            width=170,
            height=38,
            corner_radius=8,
            placeholder_text="Consultation ID"
        )
        self.consultation_id_entry.grid(
            row=0,
            column=1,
            padx=8
        )

        ctk.CTkButton(
            select_frame,
            text="SELECT RECORD",
            width=160,
            height=38,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.select_consultation
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        self.load_consultations()

        if parent is None:
            self.root.mainloop()

    def back_to_dashboard(self):
        self.app.destroy()
        if self.parent is not None:
            self.parent._show_dashboard()

    def set_patient_summary(self, patient):
        self.patient_summary_label.configure(
            text=(
                f"Patient ID: {patient['patient_id']}   |   "
                f"Name: {patient['first_name']} {patient['last_name']}   |   "
                f"Type: {patient['patient_type']}   |   "
                f"Contact: {patient['contact_number'] or 'N/A'}"
            )
        )

    def update_patient_summary(self, patient_id):
        if not patient_id:
            return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(
            """SELECT first_name, last_name, patient_type, contact_number
               FROM patients WHERE patient_id = ?""",
            (patient_id,)
        )
        patient = cursor.fetchone()
        connection.close()

        if patient:
            self.set_patient_summary({
                "patient_id": patient_id,
                "first_name": patient[0],
                "last_name": patient[1],
                "patient_type": patient[2],
                "contact_number": patient[3],
            })

    def load_medicine_options(self, selected_symptom=None):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT medicine_id, medicine_name, category, quantity, unit,
                   expiration_date
            FROM medicines
            WHERE quantity > 0
            ORDER BY medicine_name COLLATE NOCASE
        """)
        medicines = cursor.fetchall()
        connection.close()

        today = date.today()
        options = []
        for _medicine_id, name, category, quantity, unit, expiration in medicines:
            if selected_symptom:
                symptom_key = selected_symptom.strip().casefold()
                category_key = (category or "").strip().casefold()
                category_keywords = SYMPTOM_CATEGORY_KEYWORDS.get(
                    symptom_key, (symptom_key,)
                )
                if not any(keyword in category_key for keyword in category_keywords):
                    continue

            if expiration:
                try:
                    if datetime.strptime(expiration, "%Y-%m-%d").date() < today:
                        continue
                except ValueError:
                    continue

            options.append(
                f"{name} | Stock: {quantity} {unit or ''} | "
                f"Expires: {expiration or 'N/A'}"
            )

        self.medicine_options = options
        return options

    def load_symptom_options(self):
        options = [
            "Headache",
            "Stomachache",
            "Eye pain",
            "Toothache",
            "Fever",
            "Cough",
            "Allergy / Pangangati",
            "Sipon / Baradong ilong",
            "Pagtatae",
            "Constipation / Hirap dumumi",
            "Heartburn / Maasim ang sikmura",
            "Kabag",
            "Minor wound / Sugat",
            "Burn / Paso",
            "Skin irritation / Pantal",
            "Dry / Irritated eyes",
            "Earwax / Baradong tainga",
            "Vitamin supplementation",
            "Nutritional supplementation",
            "Iron supplementation",
            "Other"
        ]

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT symptoms
            FROM consultations
            WHERE symptoms IS NOT NULL AND TRIM(symptoms) != ''
            ORDER BY symptoms COLLATE NOCASE
        """)
        saved_symptoms = cursor.fetchall()
        connection.close()

        seen = {symptom.casefold() for symptom in options}
        for (symptom,) in saved_symptoms:
            symptom = symptom.strip()
            if symptom and symptom.casefold() not in seen:
                options.append(symptom)
                seen.add(symptom.casefold())

        return options

    def on_symptom_selected(self, selected_symptom):
        options = self.load_medicine_options(selected_symptom)
        if len(options) == 1:
            self.treatment_entry.configure(values=options)
            self.treatment_entry.set(options[0])
        elif options:
            self.treatment_entry.configure(values=options)
            self.treatment_entry.set(options[0])
        else:
            self.treatment_entry.configure(values=[])
            self.treatment_entry.set(
                "No matching staff-approved medicine in stock"
            )

    # =========================
    # ADD CONSULTATION
    # =========================

    def add_consultation(self):
        patient_id = self.patient_id_entry.get().strip()
        consultation_date = self.date_entry.get().strip()
        symptoms = self.symptoms_entry.get().strip()
        treatment = self.treatment_entry.get().strip()

        if not patient_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Patient ID."
            )
            return

        if not self.has_selected_symptom_and_treatment(symptoms, treatment):
            return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:
            connection.close()

            messagebox.showerror(
                "Patient Not Found",
                "The Patient ID does not exist."
            )
            return

        cursor.execute("""
            INSERT INTO consultations
            (
                patient_id,
                consultation_date,
                symptoms,
                treatment
            )
            VALUES (?, ?, ?, ?)
        """, (
            patient_id,
            consultation_date,
            symptoms,
            treatment
        ))

        connection.commit()
        connection.close()

        self.symptoms_entry.configure(values=self.load_symptom_options())

        messagebox.showinfo(
            "Success",
            "Consultation added successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # LOAD CONSULTATIONS
    # =========================

    def load_consultations(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.consultation_id,
                c.patient_id,
                p.first_name,
                p.last_name,
                c.consultation_date,
                c.symptoms,
                c.treatment
            FROM consultations c
            JOIN patients p
                ON c.patient_id = p.patient_id
            ORDER BY c.consultation_id DESC
        """)

        records = cursor.fetchall()
        connection.close()

        self.consultation_list.delete(
            "1.0",
            "end"
        )

        if not records:
            self.consultation_list.insert(
                "end",
                "No consultations yet."
            )
            return

        for record in records:
            (
                consultation_id,
                patient_id,
                first_name,
                last_name,
                consultation_date,
                symptoms,
                treatment
            ) = record

            self.consultation_list.insert(
                "end",
                f"Consultation ID: {consultation_id}\n"
                f"Patient ID: {patient_id}\n"
                f"Patient: {first_name} {last_name}\n"
                f"Date: {consultation_date}\n"
                f"Symptoms: {symptoms}\n"
                f"Treatment: {treatment}\n"
                f"{'-' * 70}\n"
            )

    # =========================
    # SELECT CONSULTATION
    # =========================

    def select_consultation(self):
        consultation_id = (
            self.consultation_id_entry
            .get()
            .strip()
        )

        if not consultation_id:
            messagebox.showwarning(
                "Missing ID",
                "Please enter a Consultation ID."
            )
            return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                patient_id,
                consultation_date,
                symptoms,
                treatment
            FROM consultations
            WHERE consultation_id = ?
        """, (consultation_id,))

        record = cursor.fetchone()
        connection.close()

        if record is None:
            messagebox.showerror(
                "Not Found",
                "Consultation ID not found."
            )
            return

        self.selected_consultation_id = consultation_id

        self.patient_id_entry.delete(0, "end")
        self.patient_id_entry.insert(0, record[0])

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, record[1])

        self.symptoms_entry.delete(0, "end")
        self.symptoms_entry.insert(0, record[2] or "")

        self.treatment_entry.delete(0, "end")
        self.treatment_entry.insert(0, record[3] or "")
        self.update_patient_summary(record[0])

        messagebox.showinfo(
            "Record Selected",
            f"Consultation ID {consultation_id} selected."
        )

    # =========================
    # UPDATE CONSULTATION
    # =========================

    def update_consultation(self):
        if self.selected_consultation_id is None:
            messagebox.showwarning(
                "No Record Selected",
                "Please select a consultation first."
            )
            return

        patient_id = self.patient_id_entry.get().strip()
        consultation_date = self.date_entry.get().strip()
        symptoms = self.symptoms_entry.get().strip()
        treatment = self.treatment_entry.get().strip()

        if not self.has_selected_symptom_and_treatment(symptoms, treatment):
            return

        if not patient_id:
            messagebox.showwarning(
                "Missing Information",
                "Patient ID is required."
            )
            return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        if cursor.fetchone() is None:
            connection.close()

            messagebox.showerror(
                "Patient Not Found",
                "The Patient ID does not exist."
            )
            return

        cursor.execute("""
            UPDATE consultations
            SET patient_id = ?,
                consultation_date = ?,
                symptoms = ?,
                treatment = ?
            WHERE consultation_id = ?
        """, (
            patient_id,
            consultation_date,
            symptoms,
            treatment,
            self.selected_consultation_id
        ))

        connection.commit()
        connection.close()

        self.symptoms_entry.configure(values=self.load_symptom_options())

        messagebox.showinfo(
            "Success",
            "Consultation updated successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # DELETE CONSULTATION
    # =========================

    def delete_consultation(self):
        if self.selected_consultation_id is None:
            messagebox.showwarning(
                "No Record Selected",
                "Please select a consultation first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this consultation?"
        )

        if not confirm:
            return

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM consultations
            WHERE consultation_id = ?
        """, (self.selected_consultation_id,))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Consultation deleted successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # CLEAR
    # =========================

    def clear_fields(self):
        self.patient_id_entry.delete(0, "end")
        self.consultation_id_entry.delete(0, "end")

        self.date_entry.delete(0, "end")
        self.date_entry.insert(
            0,
            str(date.today())
        )

        self.symptoms_entry.delete(0, "end")
        self.symptoms_entry.set("Select symptom")
        self.treatment_entry.delete(0, "end")
        self.treatment_entry.configure(values=[])
        self.treatment_entry.set("Select staff-approved medicine")
        self.patient_summary_label.configure(
            text="Patient information will appear here after entering a valid Patient ID."
        )

        self.selected_consultation_id = None

    @staticmethod
    def has_selected_symptom_and_treatment(symptoms, treatment):
        if not symptoms or symptoms == "Select symptom":
            messagebox.showwarning(
                "Missing Symptom",
                "Select or enter a symptom before saving the consultation."
            )
            return False

        if (
            not treatment
            or treatment.startswith("Select ")
            or treatment.startswith("No matching ")
        ):
            messagebox.showwarning(
                "Select Treatment",
                "Choose an in-stock medicine matched to the selected symptom."
            )
            return False

        return True


if __name__ == "__main__":
    ConsultationWindow()
