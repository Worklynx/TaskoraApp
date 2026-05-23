import customtkinter as ctk
from theme import *

from database import (
    get_worker_completed_tasks,
    get_worker_pending_tasks,
    get_creator_posted_tasks
)


class ProfileScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.user = self.master.current_user

        # ================= TOP ================= #
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=25, pady=20)

        back_btn = ctk.CTkButton(
            top,
            text="← Back",
            width=100,
            command=self.master.show_dashboard
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            top,
            text="My Profile",
            font=("Arial", 32, "bold"),
            text_color=NEON_CYAN
        )
        title.pack(side="left", padx=20)

        # ================= PROFILE CARD ================= #
        card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=20,
            border_width=2,
            border_color=NEON_PURPLE
        )
        card.pack(padx=40, pady=20, fill="x")

        # ================= NAME ================= #
        name = ctk.CTkLabel(
            card,
            text=self.user["name"],
            font=("Arial", 30, "bold"),
            text_color=TEXT
        )
        name.pack(anchor="w", padx=30, pady=(25, 10))

        # ================= USER INFO ================= #
        info = f"""
Phone: {self.user['phone']}
Role: {self.user['role']}
Rank: {self.user['rank']}
Points: {self.user['points']}
"""

        details = ctk.CTkLabel(
            card,
            text=info,
            justify="left",
            font=("Arial", 16),
            text_color=MUTED
        )
        details.pack(anchor="w", padx=30)

        # ================= PROGRESS ================= #
        points = self.user["points"]

        if points < 100:
            next_rank = 100
            rank_name = "Silver"

        elif points < 250:
            next_rank = 250
            rank_name = "Gold"

        elif points < 500:
            next_rank = 500
            rank_name = "Platinum"

        else:
            next_rank = 500
            rank_name = "MAX"

        progress = min(points / next_rank, 1)

        progress_label = ctk.CTkLabel(
            card,
            text=f"Progress to {rank_name}",
            font=("Arial", 15, "bold"),
            text_color=NEON_GREEN
        )
        progress_label.pack(anchor="w", padx=30, pady=(20, 5))

        progressbar = ctk.CTkProgressBar(
            card,
            width=500,
            progress_color=NEON_CYAN
        )
        progressbar.pack(anchor="w", padx=30)

        progressbar.set(progress)

        # ================= STATS ================= #
        stats = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats.pack(fill="x", padx=40, pady=20)

        completed = get_worker_completed_tasks(self.user["phone"])
        posted = get_creator_posted_tasks(self.user["phone"])
        applications = get_worker_pending_tasks(self.user["phone"])

        self.make_stat(
            stats,
            "Completed Tasks",
            completed
        ).pack(side="left", expand=True, padx=10)

        self.make_stat(
            stats,
            "Posted Tasks",
            posted
        ).pack(side="left", expand=True, padx=10)

        self.make_stat(
            stats,
            "Applications",
            applications
        ).pack(side="left", expand=True, padx=10)

    # ================= STAT CARD ================= #
    def make_stat(self, parent, title, value):

        frame = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=18,
            border_width=2,
            border_color=NEON_CYAN,
            width=220,
            height=120
        )

        frame.pack_propagate(False)

        number = ctk.CTkLabel(
            frame,
            text=str(value),
            font=("Arial", 32, "bold"),
            text_color=NEON_GREEN
        )
        number.pack(pady=(20, 5))

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 14),
            text_color=TEXT
        )
        label.pack()

        return frame