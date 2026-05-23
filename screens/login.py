import customtkinter as ctk
from theme import *
from database import login_user


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.show_password = False

        self.container = ctk.CTkFrame(
            self,
            width=920,
            height=520,
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
            height=520,
            corner_radius=28,
            fg_color=PANEL,
            border_width=2,
            border_color=NEON_CYAN
        )
        self.left_panel.place(x=0, y=0)
        self.left_panel.pack_propagate(False)

        self.left_logo = ctk.CTkFrame(
            self.left_panel,
            width=130,
            height=130,
            corner_radius=65,
            fg_color=BG,
            border_width=3,
            border_color=NEON_CYAN
        )
        self.left_logo.place(relx=0.5, rely=0.28, anchor="center")

        self.left_logo_text = ctk.CTkLabel(
            self.left_logo,
            text="T",
            font=("Arial", 60, "bold"),
            text_color=NEON_CYAN
        )
        self.left_logo_text.place(relx=0.5, rely=0.5, anchor="center")

        self.left_title = ctk.CTkLabel(
            self.left_panel,
            text="Taskora",
            font=("Arial", 42, "bold"),
            text_color=TEXT
        )
        self.left_title.place(relx=0.5, rely=0.48, anchor="center")

        self.left_sub = ctk.CTkLabel(
            self.left_panel,
            text="Your trusted\nmicro-task marketplace",
            font=("Arial", 15),
            text_color=MUTED,
            justify="center"
        )
        self.left_sub.place(relx=0.5, rely=0.60, anchor="center")

        # ---------------- RIGHT PANEL ---------------- #
        self.right_panel = ctk.CTkFrame(
            self.container,
            width=550,
            height=520,
            corner_radius=28,
            fg_color=CARD
        )
        self.right_panel.place(x=370, y=0)
        self.right_panel.pack_propagate(False)

        self.title = ctk.CTkLabel(
            self.right_panel,
            text="Welcome Back",
            font=("Arial", 38, "bold"),
            text_color=NEON_CYAN
        )
        self.title.place(x=60, y=55)

        self.desc = ctk.CTkLabel(
            self.right_panel,
            text="Login to continue earning and leveling up.",
            font=("Arial", 14),
            text_color=MUTED
        )
        self.desc.place(x=60, y=110)

        # Phone
        self.phone_label = ctk.CTkLabel(
            self.right_panel,
            text="Phone Number",
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        self.phone_label.place(x=60, y=165)

        self.phone_entry = ctk.CTkEntry(
            self.right_panel,
            width=420,
            height=50,
            corner_radius=16,
            fg_color=INPUT,
            border_width=2,
            border_color=NEON_PURPLE,
            placeholder_text="e.g. 074 000 0000",
            text_color=TEXT,
            placeholder_text_color=MUTED
        )
        self.phone_entry.place(x=60, y=200)

        # Password
        self.pass_label = ctk.CTkLabel(
            self.right_panel,
            text="Password",
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        self.pass_label.place(x=60, y=265)

        self.password_entry = ctk.CTkEntry(
            self.right_panel,
            width=360,
            height=50,
            corner_radius=16,
            fg_color=INPUT,
            border_width=2,
            border_color=NEON_PURPLE,
            placeholder_text="Enter password",
            text_color=TEXT,
            placeholder_text_color=MUTED,
            show="●"
        )
        self.password_entry.place(x=60, y=300)

        self.eye_btn = ctk.CTkButton(
            self.right_panel,
            text="👁",
            width=55,
            height=50,
            corner_radius=16,
            fg_color=BG,
            hover_color="#141B3A",
            border_width=2,
            border_color=NEON_CYAN,
            text_color=NEON_CYAN,
            command=self.toggle_password
        )
        self.eye_btn.place(x=430, y=300)

        # Message
        self.message = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 13, "bold"),
            text_color=NEON_PINK
        )
        self.message.place(x=60, y=360)

        # Login button
        self.login_btn = ctk.CTkButton(
            self.right_panel,
            text="LOGIN →",
            width=420,
            height=55,
            corner_radius=22,
            font=("Arial", 16, "bold"),
            fg_color=NEON_CYAN,
            hover_color=NEON_PURPLE,
            text_color=BG,
            command=self.login
        )
        self.login_btn.place(x=60, y=410)

        # Signup
        self.signup_text = ctk.CTkLabel(
            self.right_panel,
            text="New user?",
            font=("Arial", 13),
            text_color=MUTED
        )
        self.signup_text.place(x=180, y=485)

        self.signup_btn = ctk.CTkButton(
            self.right_panel,
            text="Create account",
            font=("Arial", 13, "bold"),
            fg_color="transparent",
            hover_color=CARD,
            text_color=NEON_CYAN,
            width=130,
            command=self.master.show_register
        )
        self.signup_btn.place(x=245, y=482)

    def toggle_password(self):
        if self.show_password:
            self.password_entry.configure(show="●")
        else:
            self.password_entry.configure(show="")
        self.show_password = not self.show_password

    def login(self):
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()

        if phone == "" or password == "":
            self.message.configure(text="⚠ Please enter phone and password.")
            return

        try:
            user = login_user(phone, password)

            if user:
                self.master.current_user = user
                self.master.show_dashboard()
            else:
                self.message.configure(text="❌ Invalid phone number or password.")

        except Exception as e:
            self.message.configure(text="⚠ Database error. Check terminal.")
            print("LOGIN ERROR:", e)