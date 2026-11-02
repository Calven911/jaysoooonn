import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime
from models import Medicine

class MedicineInventoryWindow:
    def __init__(self, parent=None, patient_info=None):
        self.parent = parent
        self.patient_info = patient_info
        self.root = parent if parent else ctk.CTk()
        self.app = ctk.CTkScrollableFrame(self.root, fg_color="#EAF4FF")
        self.app.pack(fill="both", expand=True)

        self.root.title("School Clinic - Medicine Inventory")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        # =========================
        # THEME
        # =========================

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


        self.selected_medicine_id = None

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
            text="💊  MEDICINE INVENTORY",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        title.pack(pady=(25, 3))

        subtitle = ctk.CTkLabel(
            header,
            text="Medicine Stock Management",
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
            pady=15,
            padx=35,
            fill="x"
        )

        form_title = ctk.CTkLabel(
            form_frame,
            text="MEDICINE INFORMATION",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            pady=(15, 8)
        )

        # Medicine Name
        ctk.CTkLabel(
            form_frame,
            text="Medicine Name",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=6
        )

        self.name_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Medicine name"
        )
        self.name_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=6
        )

        # Category
        ctk.CTkLabel(
            form_frame,
            text="Category",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=2,
            padx=15,
            pady=6
        )

        self.category_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Category"
        )
        self.category_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=6
        )

        # Quantity
        ctk.CTkLabel(
            form_frame,
            text="Quantity",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=6
        )

        self.quantity_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Stock quantity"
        )
        self.quantity_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=6
        )

        # Unit
        ctk.CTkLabel(
            form_frame,
            text="Unit",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=6
        )

        self.unit_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="e.g. tablet, bottle"
        )
        self.unit_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=6
        )

        # Expiration
        ctk.CTkLabel(
            form_frame,
            text="Expiration Date",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=6
        )

        self.expiration_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="YYYY-MM-DD"
        )
        self.expiration_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=6
        )

        # =========================
        # CRUD BUTTONS
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=(10, 15)
        )

        ctk.CTkButton(
            button_frame,
            text="ADD MEDICINE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.add_medicine
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
            command=self.update_medicine
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
            command=self.delete_medicine
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
        # INVENTORY LIST
        # =========================

        list_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        list_frame.pack(
            pady=(0, 15),
            padx=35,
            fill="x"
        )

        ctk.CTkLabel(
            list_frame,
            text="CURRENT MEDICINE INVENTORY",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(12, 6))

        self.medicine_list = ctk.CTkTextbox(
            list_frame,
            height=155,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.medicine_list.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # =========================
        # SELECT MEDICINE
        # =========================

        select_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent"
        )
        select_frame.pack(pady=(5, 12))

        ctk.CTkLabel(
            select_frame,
            text="Medicine ID:",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        self.medicine_id_entry = ctk.CTkEntry(
            select_frame,
            width=170,
            height=38,
            corner_radius=8,
            placeholder_text="Medicine ID"
        )
        self.medicine_id_entry.grid(
            row=0,
            column=1,
            padx=8
        )

        ctk.CTkButton(
            select_frame,
            text="SELECT MEDICINE",
            width=170,
            height=38,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.select_medicine
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        # =========================
        # DISPENSING SECTION
        # =========================

        dispense_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        dispense_frame.pack(
            pady=(0, 15),
            padx=35,
            fill="x"
        )

        ctk.CTkLabel(
            dispense_frame,
            text="💊 DISPENSE MEDICINE",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).grid(
            row=0,
            column=0,
            columnspan=6,
            pady=(12, 8)
        )

        # Patient ID
        ctk.CTkLabel(
            dispense_frame,
            text="Patient ID",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=8
        )

        self.dispense_patient_entry = ctk.CTkEntry(
            dispense_frame,
            width=130,
            height=38,
            corner_radius=8,
            placeholder_text="Patient ID"
        )
        self.dispense_patient_entry.grid(
            row=1,
            column=1,
            padx=8,
            pady=8
        )

        if patient_info:
            self.dispense_patient_entry.insert(
                0, str(patient_info["patient_id"])
            )

        # Medicine ID
        ctk.CTkLabel(
            dispense_frame,
            text="Medicine ID",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=2,
            padx=8,
            pady=8
        )

        self.dispense_medicine_entry = ctk.CTkEntry(
            dispense_frame,
            width=130,
            height=38,
            corner_radius=8,
            placeholder_text="Medicine ID"
        )
        self.dispense_medicine_entry.grid(
            row=1,
            column=3,
            padx=8,
            pady=8
        )

        # Quantity
        ctk.CTkLabel(
            dispense_frame,
            text="Quantity",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=4,
            padx=8,
            pady=8
        )

        self.dispense_quantity_entry = ctk.CTkEntry(
            dispense_frame,
            width=130,
            height=38,
            corner_radius=8,
            placeholder_text="Quantity"
        )
        self.dispense_quantity_entry.grid(
            row=1,
            column=5,
            padx=8,
            pady=8
        )

        self.patient_name_label = ctk.CTkLabel(
            dispense_frame,
            text=(
                f"Patient ID: {patient_info['patient_id']}   |   "
                f"Name: {patient_info['first_name']} "
                f"{patient_info['last_name']}   |   "
                f"Type: {patient_info['patient_type']}   |   "
                f"Contact: {patient_info['contact_number'] or 'N/A'}"
                if patient_info else "Patient: select or enter a Patient ID"
            ),
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        )
        self.patient_name_label.grid(
            row=2,
            column=0,
            columnspan=6,
            pady=(2, 8)
        )

        ctk.CTkLabel(
            dispense_frame,
            text="Patient concern",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(row=3, column=0, columnspan=2, padx=8, pady=8)

        self.symptom_menu = ctk.CTkComboBox(
            dispense_frame,
            width=250,
            height=38,
            values=[
                "Headache",
                "Stomachache",
                "Toothache",
                "Other / describe to staff"
            ]
        )
        self.symptom_menu.grid(
            row=3,
            column=2,
            columnspan=2,
            padx=8,
            pady=8
        )
        self.symptom_menu.set("Select concern")

        # Dispense button
        ctk.CTkButton(
            dispense_frame,
            text="💊 DISPENSE",
            width=220,
            height=42,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 14, "bold"),
            command=self.dispense_medicine
        ).grid(
            row=4,
            column=0,
            columnspan=6,
            pady=(3, 15)
        )

        # Load inventory
        self.load_medicines()

        if parent is None:
            self.root.mainloop()

    def back_to_dashboard(self):
        self.app.destroy()
        if self.parent is not None:
            self.parent._show_dashboard()

    # =========================
    # ADD MEDICINE
    # =========================

    
    def add_medicine(self):
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()
        unit = self.unit_entry.get().strip()
        expiration = self.expiration_entry.get().strip()

        if not name or not quantity_text:
            messagebox.showwarning(
                "Missing Information",
                "Medicine name and quantity are required."
            )
            return

        try:
            quantity = int(quantity_text)

            if quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if expiration:
            try:
                datetime.strptime(expiration, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Expiration date must use YYYY-MM-DD format."
                )
                return

        # Create a Medicine object using OOP
        medicine = Medicine(
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            expiration_date=expiration
        )

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO medicines
                (
                    medicine_name,
                    category,
                    quantity,
                    unit,
                    expiration_date
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                medicine.name,
                medicine.category,
                medicine.quantity,
                medicine.unit,
                medicine.expiration_date
            ))

            connection.commit()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not add medicine:\n{error}"
            )
            return

        finally:
            connection.close()

        messagebox.showinfo(
            "Success",
            f"Medicine added successfully!\n\n"
            f"Name: {medicine.name}\n"
            f"Status: {medicine.get_status()}"
        )

        self.clear_fields()
        self.load_medicines()

    # =========================
    # LOAD MEDICINES
    # =========================

    def load_medicines(self):
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                medicine_id,
                medicine_name,
                category,
                quantity,
                unit,
                expiration_date
            FROM medicines
            ORDER BY medicine_id DESC
        """)

        medicines = cursor.fetchall()
        connection.close()

        self.medicine_list.delete(
            "1.0",
            "end"
        )

        if not medicines:
            self.medicine_list.insert(
                "end",
                "No medicines registered yet."
            )
            return

        for medicine in medicines:
            (
                medicine_id,
                name,
                category,
                quantity,
                unit,
                expiration
            ) = medicine

            status = self.get_status(
                quantity,
                expiration
            )

            self.medicine_list.insert(
                "end",
                f"Medicine ID: {medicine_id}\n"
                f"Name: {name}\n"
                f"Category: {category or 'N/A'}\n"
                f"Quantity: {quantity} {unit or ''}\n"
                f"Expiration: {expiration or 'N/A'}\n"
                f"Status: {status}\n"
                f"{'-' * 70}\n"
            )

    # =========================
    # STATUS CHECK
    # =========================

    def get_status(self, quantity, expiration):
        warnings = []

        if quantity <= 5:
            warnings.append("LOW STOCK")

        if expiration:
            try:
                expiration_date = datetime.strptime(
                    expiration,
                    "%Y-%m-%d"
                ).date()

                today = datetime.today().date()

                if expiration_date < today:
                    warnings.append("EXPIRED")

            except ValueError:
                warnings.append("INVALID DATE")

        if warnings:
            return " / ".join(warnings)

        return "OK"

    # =========================
    # SELECT MEDICINE
    # =========================

    def select_medicine(self):
        medicine_id = self.medicine_id_entry.get().strip()

        if not medicine_id:
            messagebox.showwarning(
                "Missing ID",
                "Please enter a Medicine ID."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                medicine_name,
                category,
                quantity,
                unit,
                expiration_date
            FROM medicines
            WHERE medicine_id = ?
        """, (medicine_id,))

        medicine = cursor.fetchone()
        connection.close()

        if medicine is None:
            messagebox.showerror(
                "Not Found",
                "Medicine ID not found."
            )
            return

        self.selected_medicine_id = medicine_id

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, medicine[0])

        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, medicine[1] or "")

        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, medicine[2])

        self.unit_entry.delete(0, "end")
        self.unit_entry.insert(0, medicine[3] or "")

        self.expiration_entry.delete(0, "end")
        self.expiration_entry.insert(
            0,
            medicine[4] or ""
        )

        messagebox.showinfo(
            "Medicine Selected",
            f"Medicine ID {medicine_id} is selected."
        )

    # =========================
    # UPDATE MEDICINE
    # =========================

    
    def update_medicine(self):
        if self.selected_medicine_id is None:
            messagebox.showwarning(
                "No Medicine Selected",
                "Please select a medicine first."
            )
            return

        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        quantity_text = self.quantity_entry.get().strip()
        unit = self.unit_entry.get().strip()
        expiration = self.expiration_entry.get().strip()

        if not name or not quantity_text:
            messagebox.showwarning(
                "Missing Information",
                "Medicine name and quantity are required."
            )
            return

        try:
            quantity = int(quantity_text)

            if quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )
            return

        if expiration:
            try:
                datetime.strptime(expiration, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Expiration date must use YYYY-MM-DD format."
                )
                return

        # Create a Medicine object using OOP
        medicine = Medicine(
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            expiration_date=expiration
        )

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE medicines
                SET medicine_name = ?,
                    category = ?,
                    quantity = ?,
                    unit = ?,
                    expiration_date = ?
                WHERE medicine_id = ?
            """, (
                medicine.name,
                medicine.category,
                medicine.quantity,
                medicine.unit,
                medicine.expiration_date,
                self.selected_medicine_id
            ))

            connection.commit()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update medicine:\n{error}"
            )
            return

        finally:
            connection.close()

        messagebox.showinfo(
            "Success",
            f"Medicine information updated successfully!\n\n"
            f"Name: {medicine.name}\n"
            f"Status: {medicine.get_status()}"
        )

        self.clear_fields()
        self.load_medicines()

    # =========================
    # DELETE MEDICINE
    # =========================

    def delete_medicine(self):
        if self.selected_medicine_id is None:
            messagebox.showwarning(
                "No Medicine Selected",
                "Please select a medicine first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this medicine?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        try:
            cursor.execute("""
                DELETE FROM medicines
                WHERE medicine_id = ?
            """, (self.selected_medicine_id,))

            connection.commit()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete medicine:\n{error}"
            )
            return

        finally:
            connection.close()

        messagebox.showinfo(
            "Deleted",
            "Medicine deleted successfully!"
        )

        self.clear_fields()
        self.load_medicines()
        
    # =========================
    # DISPENSE MEDICINE
    # =========================

    def dispense_medicine(self):
        patient_id_text = self.dispense_patient_entry.get().strip()
        medicine_id_text = self.dispense_medicine_entry.get().strip()
        quantity_text = self.dispense_quantity_entry.get().strip()

        # Check required fields
        if not patient_id_text or not medicine_id_text or not quantity_text:
            messagebox.showwarning(
                "Missing Information",
                "Patient ID, Medicine ID, and quantity are required."
            )
            return

        # Validate IDs and quantity
        try:
            patient_id = int(patient_id_text)
            medicine_id = int(medicine_id_text)
            quantity_to_dispense = int(quantity_text)

            if patient_id <= 0 or medicine_id <= 0:
                raise ValueError

            if quantity_to_dispense <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Patient ID, Medicine ID, and quantity must be positive whole numbers."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        try:
            # =========================
            # CHECK PATIENT
            # =========================

            cursor.execute("""
                SELECT
                    first_name,
                    last_name
                FROM patients
                WHERE patient_id = ?
            """, (patient_id,))

            patient = cursor.fetchone()

            if patient is None:
                messagebox.showerror(
                    "Patient Not Found",
                    "The Patient ID does not exist."
                )
                return

            patient_name = f"{patient[0]} {patient[1]}"

            # =========================
            # CHECK MEDICINE
            # =========================

            cursor.execute("""
                SELECT
                    medicine_name,
                    quantity,
                    unit,
                    expiration_date
                FROM medicines
                WHERE medicine_id = ?
            """, (medicine_id,))

            medicine = cursor.fetchone()

            if medicine is None:
                messagebox.showerror(
                    "Medicine Not Found",
                    "The Medicine ID does not exist."
                )
                return

            
            medicine_name = medicine[0]
            current_stock = medicine[1]
            unit = medicine[2] or ""
            expiration = medicine[3]

            # Create a Medicine object using OOP
            medicine_item = Medicine(
                name=medicine_name,
                category="",
                quantity=current_stock,
                unit=unit,
                expiration_date=expiration or ""
            )

            # =========================
            # CHECK EXPIRATION
            # =========================

            if expiration:
                try:
                    expiration_date = datetime.strptime(
                        expiration,
                        "%Y-%m-%d"
                    ).date()

                    today = datetime.today().date()

                    if expiration_date < today:
                        messagebox.showerror(
                            "Expired Medicine",
                            f"{medicine_name} is already expired.\n\n"
                            "The medicine cannot be dispensed."
                        )
                        return

                except ValueError:
                    messagebox.showerror(
                        "Invalid Date",
                        f"The expiration date for {medicine_name} is invalid."
                    )
                    return

            # =========================
            # CHECK STOCK
            # =========================

            if current_stock <= 0:
                messagebox.showerror(
                    "Out of Stock",
                    f"{medicine_name} is currently out of stock."
                )
                return

            if quantity_to_dispense > current_stock:
                messagebox.showerror(
                    "Insufficient Stock",
                    f"Available stock: {current_stock} {unit}\n"
                    f"Requested: {quantity_to_dispense} {unit}"
                )
                return

            # =========================
            # CALCULATE NEW STOCK
            # =========================

            new_stock = medicine_item.quantity - quantity_to_dispense

            # =========================
            # UPDATE MEDICINE STOCK
            # =========================

            cursor.execute("""
                UPDATE medicines
                SET quantity = ?
                WHERE medicine_id = ?
            """, (
                new_stock,
                medicine_id
            ))

            # =========================
            # SAVE TRANSACTION
            # =========================

            dispensing_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                INSERT INTO dispensing_transactions
                (
                    patient_id,
                    medicine_id,
                    quantity_dispensed,
                    dispensing_date
                )
                VALUES (?, ?, ?, ?)
            """, (
                patient_id,
                medicine_id,
                quantity_to_dispense,
                dispensing_date
            ))

            connection.commit()

            # =========================
            # SUCCESS MESSAGE
            # =========================

            status_message = self.get_status(
                new_stock,
                expiration
            )

            messagebox.showinfo(
                "Medicine Dispensed",
                f"Medicine dispensed successfully!\n\n"
                f"Patient: {patient_name}\n"
                f"Medicine: {medicine_name}\n"
                f"Quantity: {quantity_to_dispense} {unit}\n"
                f"Remaining Stock: {new_stock} {unit}\n\n"
                f"Status: {status_message}"
            )

            # Clear dispensing fields
            if not self.patient_info:
                self.dispense_patient_entry.delete(0, "end")
            self.dispense_medicine_entry.delete(0, "end")
            self.dispense_quantity_entry.delete(0, "end")

            # Refresh inventory
            self.load_medicines()

        except sqlite3.Error as error:
            connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"An error occurred while dispensing:\n\n{error}"
            )

        finally:
            connection.close()

    # =========================
    # CLEAR
    # =========================

    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.unit_entry.delete(0, "end")
        self.expiration_entry.delete(0, "end")
        self.medicine_id_entry.delete(0, "end")

        self.selected_medicine_id = None


if __name__ == "__main__":
    MedicineInventoryWindow()
