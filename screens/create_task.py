import customtkinter as ctk
from theme import *
from database import create_task


class CreateTaskScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.user = self.master.current_user

        # ================= TOP BAR ================= #
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
            text="Create Task",
            font=("Arial", 30, "bold"),
            text_color=NEON_CYAN
        )
        title.pack(side="left", padx=20)

        # ================= MAIN CARD ================= #
        self.card = ctk.CTkFrame(
            self,
            corner_radius=22,
            fg_color=CARD,
            border_width=2,
            border_color=NEON_PURPLE
        )
        self.card.pack(
            padx=60,
            pady=20,
            fill="both",
            expand=True
        )

        # ================= ENTRIES ================= #
        self.task_title = self.make_entry("Task Title", 40)

        self.location = self.make_entry("Location", 140)

        self.reward = self.make_entry("Reward Amount (R)", 240)

        # ================= DESCRIPTION ================= #
        desc_label = ctk.CTkLabel(
            self.card,
            text="Description",
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        desc_label.place(x=50, y=340)

        self.description = ctk.CTkTextbox(
            self.card,
            width=900,
            height=100,
            corner_radius=15,
            fg_color=INPUT,
            text_color=TEXT
        )
        self.description.place(x=50, y=370)

        # ================= MESSAGE ================= #
        self.message = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 14, "bold"),
            text_color=NEON_GREEN
        )
        self.message.place(x=50, y=500)

        # ================= BUTTON ================= #
        self.create_btn = ctk.CTkButton(
            self.card,
            text="POST TASK",
            width=200,
            height=45,
            corner_radius=16,
            fg_color=NEON_CYAN,
            hover_color=NEON_PURPLE,
            text_color=BG,
            font=("Arial", 14, "bold"),
            command=self.create_task
        )

        # CENTER BUTTON
        self.create_btn.place(
            relx=0.5,
            y=490,
            anchor="center"
        )

    # ================= ENTRY MAKER ================= #
    def make_entry(self, label_text, y):

        label = ctk.CTkLabel(
            self.card,
            text=label_text,
            font=("Arial", 13, "bold"),
            text_color=TEXT
        )
        label.place(x=50, y=y)

        entry = ctk.CTkEntry(
            self.card,
            width=900,
            height=50,
            corner_radius=16,
            fg_color=INPUT,
            border_width=2,
            border_color=NEON_PURPLE,
            text_color=TEXT,
            placeholder_text=f"Enter {label_text.lower()}",
            placeholder_text_color=MUTED
        )

        entry.place(x=50, y=y + 30)

        return entry

    def create_task(self):

        title = self.task_title.get().strip()
        location = self.location.get().strip()
        reward = self.reward.get().strip()
        desc = self.description.get("1.0", "end").strip()

        # Validation
        if title == "" or location == "" or reward == "" or desc == "":
            self.message.configure(
                text="⚠ Please fill in all fields.",
                text_color=NEON_PINK
            )
            return

        # Reward must be integer
        try:
            reward = int(reward)

        except:
            self.message.configure(
                text="⚠ Reward must be a number.",
                text_color=NEON_PINK
            )
            return

        # Save task
        try:
            create_task(
                title=title,
                description=desc,
                location=location,
                reward=reward,
                creator_phone=self.user["phone"]
            )

            self.message.configure(
                text="✔ Task posted successfully!",
                text_color=NEON_GREEN
            )

            self.after(
                1200,
                self.master.show_my_posted_tasks
            )

        except Exception as e:

            self.message.configure(
                text="⚠ Database error. Check terminal.",
                text_color=NEON_PINK
            )

            print("CREATE TASK ERROR:", e)