import customtkinter as ctk
from theme import *
from database import apply_for_task, get_connection


class TaskDetailsScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.user = self.master.current_user
        self.task = self.master.selected_task

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
            command=self.master.show_browse_tasks
        )
        back_btn.pack(side="left")

        title = ctk.CTkLabel(
            top,
            text="Task Details",
            font=("Arial", 30, "bold"),
            text_color=NEON_CYAN
        )
        title.pack(side="left", padx=20)

        # ---------------- MAIN CARD ---------------- #
        self.card = ctk.CTkFrame(
            self,
            corner_radius=22,
            fg_color=CARD,
            border_width=2,
            border_color=NEON_PURPLE
        )
        self.card.pack(padx=60, pady=30, fill="both", expand=True)

        self.task_title = ctk.CTkLabel(
            self.card,
            text=self.task["title"],
            font=("Arial", 26, "bold"),
            text_color=TEXT
        )
        self.task_title.pack(anchor="w", padx=30, pady=(25, 10))

        info = (
            f"📍 Location: {self.task['location']}\n"
            f"💰 Reward: R{self.task['reward']}\n"
            f"⚡ Status: {self.task['status']}"
        )

        self.task_info = ctk.CTkLabel(
            self.card,
            text=info,
            font=("Arial", 14),
            text_color=MUTED,
            justify="left"
        )
        self.task_info.pack(anchor="w", padx=30, pady=(0, 15))

        self.desc_label = ctk.CTkLabel(
            self.card,
            text="Description",
            font=("Arial", 16, "bold"),
            text_color=NEON_CYAN
        )
        self.desc_label.pack(anchor="w", padx=30, pady=(0, 5))

        self.desc_text = ctk.CTkLabel(
            self.card,
            text=self.task["description"],
            font=("Arial", 13),
            text_color=TEXT,
            wraplength=800,
            justify="left"
        )
        self.desc_text.pack(anchor="w", padx=30, pady=(0, 20))

        self.message = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 14, "bold"),
            text_color=NEON_GREEN
        )
        self.message.pack(pady=(0, 10))

        self.apply_btn = ctk.CTkButton(
            self.card,
            text="Apply for Task →",
            width=260,
            height=50,
            corner_radius=18,
            fg_color=NEON_CYAN,
            hover_color=NEON_PURPLE,
            text_color=BG,
            font=("Arial", 15, "bold"),
            command=self.apply_task
        )
        self.apply_btn.pack(pady=(10, 25))

        self.check_task_status()

    # ---------------- CHECK STATUS ---------------- #
    def check_task_status(self):
        if self.task["status"] != "Open":
            self.apply_btn.configure(state="disabled", fg_color="#1F2A55")
            self.message.configure(text="⚠ This task is no longer open.", text_color=NEON_PINK)
            return

        # check if already applied in database
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT id FROM applications
                WHERE task_id = %s AND worker_phone = %s
                """,
                (self.task["id"], self.user["phone"])
            )

            result = cur.fetchone()

            cur.close()
            conn.close()

            if result:
                self.apply_btn.configure(state="disabled", fg_color="#1F2A55")
                self.message.configure(text="✔ You already applied for this task.", text_color=NEON_GREEN)

        except Exception as e:
            print("CHECK APPLICATION ERROR:", e)

    # ---------------- APPLY TASK ---------------- #
    def apply_task(self):
        # Prevent creator applying
        if self.task["creator"] == self.user["phone"]:
            self.message.configure(text="⚠ You cannot apply for your own task.", text_color=NEON_PINK)
            return

        # Task must be open
        if self.task["status"] != "Open":
            self.message.configure(text="⚠ This task is no longer open.", text_color=NEON_PINK)
            self.apply_btn.configure(state="disabled", fg_color="#1F2A55")
            return

        try:
            # Insert into database
            apply_for_task(self.task["id"], self.user["phone"])

            self.message.configure(text="✔ Application sent successfully!", text_color=NEON_GREEN)
            self.apply_btn.configure(state="disabled", fg_color="#1F2A55")

        except Exception as e:
            error_text = str(e).lower()

            if "duplicate" in error_text:
                self.message.configure(text="✔ You already applied for this task.", text_color=NEON_GREEN)
                self.apply_btn.configure(state="disabled", fg_color="#1F2A55")
            else:
                self.message.configure(text="⚠ Database error. Check terminal.", text_color=NEON_PINK)
                print("APPLY TASK ERROR:", e)