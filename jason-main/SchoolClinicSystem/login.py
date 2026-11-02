import customtkinter as ctk
import sqlite3
from tkinter import messagebox


class LoginWindow:
    def __init__(self):
        self.app = ctk.CTk()

        self.app.title("School Clinic - Staff Login")
        self.app.geometry("650x600")
        self.app.resizable(False, False)
        self.app.update_idletasks()
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = (screen_width - 650) // 2
        y = (screen_height - 600) // 2
        self.app.geometry(f"650x600+{x}+{y}")

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Main background
        self.app.configure(fg_color="#EAF4FF")

        # Header
        header = ctk.CTkFrame(
            self.app,
            width=650,
            height=150,
            corner_radius=0,
            fg_color="#1565C0"
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🏥 SCHOOL CLINIC",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(
            header,
            text="Management System",
            font=("Arial", 17),
            text_color="#DDEEFF"
        )
        subtitle.pack()

        # Login card
        card = ctk.CTkFrame(
            self.app,
            width=430,
            height=320,
            corner_radius=20,
            fg_color="white"
        )
        card.pack(pady=45)
        card.pack_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        login_title = ctk.CTkLabel(
            card,
            text="STAFF LOGIN",
            font=("Arial", 24, "bold"),
            text_color="#1565C0"
        )
        login_title.grid(row=0, column=0, pady=(25, 20))

        # Username
        self.username_entry = ctk.CTkEntry(
            card,
            width=330,
            height=45,
            corner_radius=10,
            placeholder_text="Username"
        )
        self.username_entry.grid(row=1, column=0, pady=8)

        # Password
        self.password_entry = ctk.CTkEntry(
            card,
            width=330,
            height=45,
            corner_radius=10,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.grid(row=2, column=0, pady=8)

        # Login button
        login_button = ctk.CTkButton(
            card,
            text="LOGIN",
            width=330,
            height=48,
            corner_radius=10,
            font=("Arial", 15, "bold"),
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.login
        )
        login_button.grid(row=3, column=0, pady=(15, 10))

        self.app.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your username and password."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
            self.app.destroy()

            from dashboard import DashboardWindow
            DashboardWindow()

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )


if __name__ == "__main__":
    LoginWindow()
