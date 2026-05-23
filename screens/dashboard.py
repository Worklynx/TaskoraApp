import customtkinter as ctk
from theme import *


class DashboardScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        user = self.master.current_user

        # ================= SIDEBAR ================= #
        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            fg_color=PANEL
        )
        self.sidebar.pack(side="left", fill="y")

        # ================= LOGO ================= #
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Taskora",
            font=("Arial", 28, "bold"),
            text_color=NEON_CYAN
        )
        self.logo.pack(pady=(30, 10))

        # ================= USER INFO ================= #
        self.rank_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Rank: {user['rank']}",
            font=("Arial", 14, "bold"),
            text_color=NEON_PINK
        )
        self.rank_label.pack(pady=(5, 0))

        self.points_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Points: {user['points']}",
            font=("Arial", 13),
            text_color=MUTED
        )
        self.points_label.pack(pady=(0, 25))

        # ================= SIDEBAR BUTTONS ================= #
        self.make_sidebar_button(
            "Browse Tasks",
            self.master.show_browse_tasks
        )

        self.make_sidebar_button(
            "My Applications",
            self.master.show_my_applications
        )

        # PROFILE BUTTON
        self.make_sidebar_button(
            "My Profile",
            self.master.show_profile
        )

        # CREATOR ONLY
        if user["role"] == "Creator":

            self.make_sidebar_button(
                "Create Task",
                self.master.show_create_task
            )

            self.make_sidebar_button(
                "My Posted Tasks",
                self.master.show_my_posted_tasks
            )

        # ================= LOGOUT ================= #
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            width=200,
            height=45,
            corner_radius=18,
            fg_color=NEON_PINK,
            hover_color=NEON_PURPLE,
            text_color=BG,
            font=("Arial", 13, "bold"),
            command=self.logout
        )
        self.logout_btn.pack(side="bottom", pady=25)

        # ================= MAIN AREA ================= #
        self.main = ctk.CTkFrame(
            self,
            fg_color=BG
        )
        self.main.pack(side="left", fill="both", expand=True)

        # ================= WELCOME ================= #
        self.title = ctk.CTkLabel(
            self.main,
            text=f"Welcome, {user['name']} 👋",
            font=("Arial", 34, "bold"),
            text_color=TEXT
        )
        self.title.pack(
            pady=(40, 5),
            padx=30,
            anchor="w"
        )

        self.subtitle = ctk.CTkLabel(
            self.main,
            text=f"You are logged in as: {user['role']}",
            font=("Arial", 14),
            text_color=NEON_GREEN
        )
        self.subtitle.pack(
            pady=(0, 25),
            padx=30,
            anchor="w"
        )

        self.info = ctk.CTkLabel(
            self.main,
            text="Use the sidebar to explore tasks, manage applications, and level up.",
            font=("Arial", 14),
            text_color=MUTED
        )
        self.info.pack(
            padx=30,
            anchor="w"
        )

    # ================= SIDEBAR BUTTON ================= #
    def make_sidebar_button(self, text, command):

        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            width=200,
            height=45,
            corner_radius=16,
            fg_color=NEON_CYAN,
            hover_color=NEON_PURPLE,
            text_color=BG,
            font=("Arial", 13, "bold"),
            command=command
        )

        btn.pack(
            pady=10,
            padx=20,
            fill="x"
        )

    # ================= LOGOUT ================= #
    def logout(self):

        self.master.current_user = None
        self.master.show_login()