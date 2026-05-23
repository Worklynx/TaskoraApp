import customtkinter as ctk
from theme import *
from database import register_user


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master

        # ---------------- MAIN CONTAINER ---------------- #
        self.container = ctk.CTkFrame(
            self,
            width=920,
            height=650,  # FIXED HEIGHT
            corner_radius=28,
            fg_color=CARD,
            border_width=2,
            border_color=NEON_PURPLE
        )
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        self.container.pack_propagate(False)

        # ---------------- LEFT PANEL ---------------- #
        self.left_panel = ctk.CTkFrame(
            self.container,
            width=370,
            height=650,  # FIXED HEIGHT
            corner_radius=28,
            fg_color=PANEL,
            border_width=2,
            border_color=NEON_CYAN
        )
        self.left_panel.place(x=0, y=0)
        self.left_panel.pack_propagate(False)

        self.left_title = ctk.CTkLabel(
            self.left_panel,
            text="Taskora",
            font=("Arial", 42, "bold"),
            text_color=TEXT
        )
        self.left_title.place(relx=0.5, rely=0.42, anchor="center")

        self.left_desc = ctk.CTkLabel(
            self.left_panel,
            text="Create your account\nand start earning today.",
            font=("Arial", 15),
            text_color=NEON_PINK,
            justify="center"
        )
        self.left_desc.place(relx=0.5, rely=0.56, anchor="center")

        # ---------------- RIGHT PANEL ---------------- #
        self.right_panel = ctk.CTkFrame(
            self.container,
            width=550,
            height=650,  # FIXED HEIGHT
            corner_radius=28,
            fg_color=CARD
        )
        self.right_panel.place(x=370, y=0)
        self.right_panel.pack_propagate(False)

        # ---------------- TITLE ---------------- #
        self.title = ctk.CTkLabel(
            self.right_panel,
            text="Create Account",
            font=("Arial", 34, "bold"),
            text_color=NEON_CYAN
        )
        self.title.place(x=60, y=45)

        # ---------------- INPUTS ---------------- #
        self.name_entry = self.make_entry("Full Name", 120)
        self.phone_entry = self.make_entry("Phone Number", 210)
        self.password_entry = self.make_entry("Password", 300, show="●")
        self.confirm_entry = self.make_entry("Confirm Password", 390, show="●")

        # ---------------- ROLE ---------------- #
        self.role_label = ctk.CTkLabel(
            self.right_panel,
            text="Select Role",
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        self.role_label.place(x=60, y=480)

        self.role_dropdown = ctk.CTkOptionMenu(
            self.right_panel,
            values=["Worker", "Creator"],
            width=420,
            height=45,
            corner_radius=16,
            fg_color=INPUT,
            button_color=NEON_PURPLE,
            button_hover_color=NEON_CYAN,
            dropdown_fg_color=CARD,
            dropdown_hover_color="#1B2550",
            text_color=TEXT
        )
        self.role_dropdown.place(x=60, y=510)

        # ---------------- MESSAGE ---------------- #
        self.message = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 13, "bold"),
            text_color=NEON_PINK
        )
        self.message.place(x=60, y=565)

        # ---------------- REGISTER BUTTON ---------------- #
        self.register_btn = ctk.CTkButton(
            self.right_panel,
            text="CREATE ACCOUNT →",
            width=420,
            height=55,
            corner_radius=22,
            font=("Arial", 16, "bold"),
            fg_color=NEON_CYAN,
            hover_color=NEON_PURPLE,
            text_color=BG,
            command=self.register_user
        )
        self.register_btn.place(x=60, y=595)

        # ---------------- BACK BUTTON ---------------- #
        self.login_btn = ctk.CTkButton(
            self.right_panel,
            text="← Back to Login",
            fg_color="transparent",
            hover_color=CARD,
            text_color=NEON_PINK,
            font=("Arial", 13, "bold"),
            command=self.master.show_login
        )
        self.login_btn.place(x=60, y=10)

    # ---------------- ENTRY CREATOR ---------------- #
    def make_entry(self, label_text, y, show=None):
        label = ctk.CTkLabel(
            self.right_panel,
            text=label_text,
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        label.place(x=60, y=y)

        entry = ctk.CTkEntry(
            self.right_panel,
            width=420,
            height=50,
            corner_radius=16,
            fg_color=INPUT,
            border_width=2,
            border_color=NEON_PURPLE,
            text_color=TEXT,
            placeholder_text=f"Enter {label_text.lower()}",
            placeholder_text_color=MUTED,
            show=show
        )
        entry.place(x=60, y=y + 30)

        return entry

    # ---------------- REGISTER FUNCTION ---------------- #
    def register_user(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        role = self.role_dropdown.get()

        # Empty fields
        if name == "" or phone == "" or password == "" or confirm == "":
            self.message.configure(
                text="⚠ Please fill in all fields.",
                text_color=NEON_PINK
            )
            return

        # Password mismatch
        if password != confirm:
            self.message.configure(
                text="⚠ Passwords do not match.",
                text_color=NEON_PINK
            )
            return

        try:
            register_user(name, phone, password, role)

            self.message.configure(
                text="✔ Account created successfully!",
                text_color=NEON_GREEN
            )

            self.after(1200, self.master.show_login)

        except Exception as e:
            error_text = str(e).lower()

            if "duplicate key" in error_text or "unique constraint" in error_text:
                self.message.configure(
                    text="⚠ Phone already registered.",
                    text_color=NEON_PINK
                )
            else:
                self.message.configure(
                    text="⚠ Error creating account.",
                    text_color=NEON_PINK
                )

                print("REGISTER ERROR:", e)