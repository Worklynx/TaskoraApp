import customtkinter as ctk

from screens.splash import SplashScreen
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.dashboard import DashboardScreen
from screens.create_task import CreateTaskScreen
from screens.browse_tasks import BrowseTasksScreen
from screens.task_details import TaskDetailsScreen
from screens.my_applications import MyApplicationsScreen
from screens.my_posted_task import MyPostedTasksScreen
from screens.manage_applicants import ManageApplicantsScreen
from screens.profile import ProfileScreen


class TaskoraApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ================= WINDOW SETTINGS ================= #
        self.title("Taskora")

        self.geometry("1280x720")

        self.resizable(True, True)

        self.minsize(1000, 650)

        # Open maximized
        try:
            self.state("zoomed")

        except:
            self.attributes("-zoomed", True)

        # ================= CUSTOMTKINTER SETTINGS ================= #
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # ================= APP STATE ================= #
        self.current_screen = None
        self.current_user = None
        self.selected_task = None

        # ================= TEMP STORAGE ================= #
        self.users = []
        self.tasks = []
        self.applications = []

        # ================= START APP ================= #
        self.show_splash()

    # ================= SCREEN SWITCHER ================= #
    def switch_screen(self, screen_class):

        # Destroy old screen
        if self.current_screen:
            self.current_screen.destroy()

        # Create new screen
        self.current_screen = screen_class(self)

        # Show screen
        self.current_screen.pack(fill="both", expand=True)

        # Refresh UI
        self.update_idletasks()

        # Reset focus
        self.focus_force()
        self.current_screen.focus_set()

        # Reset scroll position
        try:
            self.current_screen._parent_canvas.yview_moveto(0)
        except:
            pass

    # ================= NAVIGATION ================= #
    def show_splash(self):
        self.switch_screen(SplashScreen)

    def show_login(self):
        self.switch_screen(LoginScreen)

    def show_register(self):
        self.switch_screen(RegisterScreen)

    def show_dashboard(self):
        self.switch_screen(DashboardScreen)

    def show_create_task(self):
        self.switch_screen(CreateTaskScreen)

    def show_browse_tasks(self):
        self.switch_screen(BrowseTasksScreen)

    def show_task_details(self, task):

        self.selected_task = task
        self.switch_screen(TaskDetailsScreen)

    def show_my_applications(self):
        self.switch_screen(MyApplicationsScreen)

    def show_my_posted_tasks(self):
        self.switch_screen(MyPostedTasksScreen)

    def show_profile(self):
        self.switch_screen(ProfileScreen)

    def show_manage_applicants(self, task):

        self.selected_task = task
        self.switch_screen(ManageApplicantsScreen)


# ================= RUN APP ================= #
if __name__ == "__main__":

    app = TaskoraApp()
    app.mainloop()