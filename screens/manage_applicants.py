import customtkinter as ctk
from theme import *

from database import (
    get_task_by_id,
    get_applicants_for_task,
    approve_application,
    reject_application,
    complete_task_db
)


class ManageApplicantsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.task = self.master.selected_task

        # Always refresh latest DB version
        self.task = get_task_by_id(self.task["id"])

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
            command=self.master.show_my_posted_tasks
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            top,
            text="Manage Applicants",
            font=("Arial", 30, "bold"),
            text_color=NEON_CYAN
        )
        title.pack(side="left", padx=20)

        # ---------------- TASK CARD ---------------- #
        self.card = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=CARD,
            border_width=2,
            border_color=NEON_PURPLE
        )
        self.card.pack(fill="x", padx=50, pady=20)

        self.title_label = ctk.CTkLabel(
            self.card,
            text=self.task["title"],
            font=("Arial", 24, "bold"),
            text_color=TEXT
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.info_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 14),
            text_color=MUTED
        )
        self.info_label.pack(anchor="w", padx=20, pady=(0, 5))

        self.assigned_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 14, "bold"),
            text_color=NEON_GREEN
        )
        self.assigned_label.pack(anchor="w", padx=20, pady=(0, 15))

        self.complete_btn = ctk.CTkButton(
            self.card,
            text="Mark Task as Completed ✓",
            width=240,
            height=48,
            corner_radius=16,
            fg_color=NEON_GREEN,
            hover_color=NEON_CYAN,
            text_color=BG,
            font=("Arial", 14, "bold"),
            command=self.complete_task
        )
        self.complete_btn.pack(anchor="e", padx=20, pady=(0, 20))

        # ---------------- MESSAGE ---------------- #
        self.message = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 14, "bold"),
            text_color=NEON_GREEN
        )
        self.message.pack()

        # ---------------- APPLICANTS ---------------- #
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=CARD,
            corner_radius=20
        )
        self.scroll.pack(fill="both", expand=True, padx=50, pady=20)

        self.refresh_screen()

    # =========================================================
    # REFRESH SCREEN
    # =========================================================
    def refresh_screen(self):

        # Reload latest task
        self.task = get_task_by_id(self.task["id"])

        status = self.task["status"]

        self.info_label.configure(
            text=f"📍 {self.task['location']}   |   💰 R{self.task['reward']}   |   ⚡ {status}"
        )

        assigned = self.task.get("assigned_worker")

        if assigned:
            self.assigned_label.configure(
                text=f"Assigned Worker: {assigned}"
            )
        else:
            self.assigned_label.configure(
                text="No assigned worker yet."
            )

        # Enable complete button ONLY when assigned
        if status == "Assigned":
            self.complete_btn.configure(
                state="normal",
                fg_color=NEON_GREEN
            )
        else:
            self.complete_btn.configure(
                state="disabled",
                fg_color="#1F2A55"
            )

        # Clear old cards
        for widget in self.scroll.winfo_children():
            widget.destroy()

        applicants = get_applicants_for_task(self.task["id"])

        if len(applicants) == 0:
            empty = ctk.CTkLabel(
                self.scroll,
                text="No applicants yet.",
                font=("Arial", 16, "bold"),
                text_color=MUTED
            )
            empty.pack(pady=60)
            return

        for app in applicants:
            self.create_applicant_card(app)

    # =========================================================
    # CREATE APPLICANT CARD
    # =========================================================
    def create_applicant_card(self, app):

        status = app["status"]

        if status == "Pending":
            color = NEON_PURPLE
        elif status == "Approved":
            color = NEON_GREEN
        elif status == "Rejected":
            color = NEON_PINK
        elif status == "Completed":
            color = NEON_CYAN
        else:
            color = MUTED

        card = ctk.CTkFrame(
            self.scroll,
            corner_radius=18,
            fg_color=PANEL,
            border_width=2,
            border_color=color
        )
        card.pack(fill="x", pady=12, padx=10)

        worker = ctk.CTkLabel(
            card,
            text=f"Worker: {app['worker_phone']}",
            font=("Arial", 17, "bold"),
            text_color=TEXT
        )
        worker.pack(anchor="w", padx=20, pady=(15, 5))

        status_label = ctk.CTkLabel(
            card,
            text=f"Status: {status}",
            font=("Arial", 13, "bold"),
            text_color=color
        )
        status_label.pack(anchor="w", padx=20)

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)

        approve_btn = ctk.CTkButton(
            btn_frame,
            text="Approve",
            width=140,
            height=40,
            corner_radius=14,
            fg_color=NEON_GREEN,
            hover_color=NEON_CYAN,
            text_color=BG,
            command=lambda: self.approve(app["id"])
        )
        approve_btn.pack(side="left", padx=(0, 10))

        reject_btn = ctk.CTkButton(
            btn_frame,
            text="Reject",
            width=140,
            height=40,
            corner_radius=14,
            fg_color=NEON_PINK,
            hover_color=NEON_PURPLE,
            text_color=BG,
            command=lambda: self.reject(app["id"])
        )
        reject_btn.pack(side="left")

        if status != "Pending":
            approve_btn.configure(state="disabled")
            reject_btn.configure(state="disabled")

    # =========================================================
    # APPROVE
    # =========================================================
    def approve(self, application_id):

        approve_application(application_id)

        self.message.configure(
            text="✔ Worker approved.",
            text_color=NEON_GREEN
        )

        self.refresh_screen()

    # =========================================================
    # REJECT
    # =========================================================
    def reject(self, application_id):

        reject_application(application_id)

        self.message.configure(
            text="✔ Application rejected.",
            text_color=NEON_PINK
        )

        self.refresh_screen()

    # =========================================================
    # COMPLETE TASK
    # =========================================================
    def complete_task(self):

        try:
            complete_task_db(self.task["id"])

            self.message.configure(
                text="✔ Task marked as completed!",
                text_color=NEON_GREEN
            )

            self.refresh_screen()

        except Exception as e:
            self.message.configure(
                text="⚠ Failed to complete task.",
                text_color=NEON_PINK
            )

            print("COMPLETE TASK ERROR:", e)