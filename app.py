import customtkinter
from constants import *
from profile_manager import ProfileManager
from ui_components.navigation import NavigationFrame
from ui_components.home import HomeFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.title("Key Remapper (Beta)")
        self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        # self.icon_path = "img/icon.ico"
        # self.iconbitmap(self.icon_path)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        customtkinter.set_appearance_mode("dark")
        self.generate()

    def center_window(self, width, height):
        self.update_idletasks() 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f'{width}x{height}+{x}+{y}')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f"+{x}+{y}")

    def generate(self):
        self.profile_manager = ProfileManager()
        self.home_frame = HomeFrame(self)
        self.navigation_frame = NavigationFrame(self)
        self.start_listening()

    def start_listening(self):
        if self.profile_manager.activation:
            self.profile_manager.check_auto_switch()
        self.after(1000, self.start_listening)