import customtkinter as ctk
from theme import *
from database import get_applications_by_worker


class MyApplicationsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.user = self.master.current_user

        # ---------------- TOP BAR ---------------- #
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=25, pady=(15, 5))

        back_btn = ctk.CTkButton(
            top,
            text="← Back",
            width=90,
            height=36,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#141B3A",
            text_color=NEON_PINK,
            font=("Arial", 14, "bold"),
            command=self.master.show_dashboard
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            top,
            text="My Applications",
            font=("Arial", 30, "bold"),
            text_color=NEON_CYAN
        )
        title.pack(side="left", padx=20)

        subtitle = ctk.CTkLabel(
            self,
            text="Track the tasks you applied for and their status.",
            font=("Arial", 14),
            text_color=MUTED
        )
        subtitle.pack(anchor="w", padx=45, pady=(0, 15))

        # ---------------- SCROLLABLE LIST ---------------- #
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=900,
            height=450,
            corner_radius=20,
            fg_color=CARD,
            scrollbar_button_color=NEON_PURPLE,
            scrollbar_button_hover_color=NEON_CYAN
        )
        self.scroll_frame.pack(padx=45, pady=10, fill="both", expand=True)

        self.load_applications()

    def load_applications(self):
        try:
            apps = get_applications_by_worker(self.user["phone"])
        except Exception as e:
            error = ctk.CTkLabel(
                self.scroll_frame,
                text="⚠ Database error. Check terminal.",
                font=("Arial", 16, "bold"),
                text_color=NEON_PINK
            )
            error.pack(pady=60)
            print("MY APPLICATIONS ERROR:", e)
            return

        if len(apps) == 0:
            empty = ctk.CTkLabel(
                self.scroll_frame,
                text="You have not applied for any tasks yet.",
                font=("Arial", 16, "bold"),
                text_color=MUTED
            )
            empty.pack(pady=60)
            return

        for app in apps:
            self.create_application_card(app)

    def create_application_card(self, app):
        status = app["status"]

        if status == "Pending":
            status_color = NEON_PURPLE
        elif status == "Approved":
            status_color = NEON_GREEN
        elif status == "Rejected":
            status_color = NEON_PINK
        elif status == "Completed":
            status_color = NEON_CYAN
        else:
            status_color = MUTED

        card = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=18,
            fg_color=PANEL,
            border_width=2,
            border_color=status_color
        )
        card.pack(fill="x", pady=12, padx=15)

        title = ctk.CTkLabel(
            card,
            text=app["title"],
            font=("Arial", 18, "bold"),
            text_color=TEXT
        )
        title.pack(anchor="w", padx=20, pady=(15, 2))

        details = ctk.CTkLabel(
            card,
            text=f"📍 {app['location']}   |   💰 R{app['reward']}   |   ⚡ Status: {status}",
            font=("Arial", 13),
            text_color=MUTED
        )
        details.pack(anchor="w", padx=20, pady=(0, 10))

        status_label = ctk.CTkLabel(
            card,
            text=status,
            font=("Arial", 13, "bold"),
            text_color=status_color
        )
        status_label.pack(anchor="e", padx=20, pady=(0, 15))