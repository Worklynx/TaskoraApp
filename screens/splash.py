import customtkinter as ctk
from theme import *


class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BG)

        self.master = master
        self.text = "Taskora"
        self.index = 0
        self.cursor_visible = True

        self.center = ctk.CTkFrame(self, fg_color="transparent")
        self.center.place(relx=0.5, rely=0.5, anchor="center")

        self.logo_circle = ctk.CTkFrame(
            self.center,
            width=140,
            height=140,
            corner_radius=70,
            fg_color=PANEL,
            border_width=3,
            border_color=NEON_CYAN
        )
        self.logo_circle.pack(pady=(0, 25))

        self.logo_text = ctk.CTkLabel(
            self.logo_circle,
            text="T",
            font=("Arial", 65, "bold"),
            text_color=NEON_CYAN
        )
        self.logo_text.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(
            self.center,
            text="",
            font=("Arial", 52, "bold"),
            text_color=TEXT
        )
        self.title_label.pack()

        self.subtitle = ctk.CTkLabel(
            self.center,
            text="Earn • Level Up • Get Trusted",
            font=("Arial", 15),
            text_color=NEON_PINK
        )
        self.subtitle.pack(pady=(10, 0))

        self.progress = ctk.CTkProgressBar(
            self.center,
            width=320,
            height=12,
            corner_radius=10,
            fg_color="#111827",
            progress_color=NEON_PURPLE
        )
        self.progress.pack(pady=(40, 10))
        self.progress.set(0)

        self.loading_text = ctk.CTkLabel(
            self.center,
            text="Initializing...",
            font=("Arial", 13),
            text_color=MUTED
        )
        self.loading_text.pack()

        self.animate_typing()
        self.animate_progress()
        self.animate_logo_glow()

        self.after(3600, self.master.show_login)

    def animate_typing(self):
        if self.index <= len(self.text):
            typed = self.text[:self.index]
            cursor = "|" if self.cursor_visible else ""
            self.title_label.configure(text=typed + cursor)

            self.cursor_visible = not self.cursor_visible
            self.index += 1
            self.after(140, self.animate_typing)

    def animate_progress(self):
        current = self.progress.get()
        if current < 1:
            self.progress.set(current + 0.03)
            self.after(80, self.animate_progress)

    def animate_logo_glow(self):
        current_border = self.logo_circle.cget("border_color")

        if current_border == NEON_CYAN:
            self.logo_circle.configure(border_color=NEON_PURPLE)
            self.logo_text.configure(text_color=NEON_PURPLE)
        else:
            self.logo_circle.configure(border_color=NEON_CYAN)
            self.logo_text.configure(text_color=NEON_CYAN)

        self.after(700, self.animate_logo_glow)