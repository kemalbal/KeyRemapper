import customtkinter
from constants import *
import tkinter as tk
from tkinter import messagebox

class NavigationFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color=BACKGROUND_COLOR)

        self.profile_manager = master.profile_manager

        self.home_frame = None
        self.selected_option = tk.StringVar(value="None")

        self.home_frame = master.home_frame

        self.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.grid_rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.radio_buttons = []
        self._create_navigation_label()
        self._create_config_list_frame()
        self._create_radio_buttons()
        self._create_new_profile_button()

        active_profile_name = self.profile_manager.get_active_profile_name()
        self.select_option(active_profile_name)   

        self.profile_manager.set_switch_profile_callback(self.select_option)    

    def _create_navigation_label(self):
        self.navigation_label_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=SECONDARY_BACKGROUND)
        self.navigation_label_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_label = customtkinter.CTkLabel(
            master=self.navigation_label_frame,
            text="CONFIGURATIONS",
            compound="left",
            font=(PRIMARY_FONT, 13, 'bold'),
            text_color=SECONDARY_TEXT_COLOR,
            height=0
        )
        self.navigation_label.grid(row=0, column=0, padx=10, pady=3, sticky="w")

    def _create_config_list_frame(self):
        options = self.profile_manager.get_profile_names()
        if len(options) > 15: 
            self.config_list_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0,fg_color=BACKGROUND_COLOR) 
        else:
            self.config_list_frame = customtkinter.CTkFrame(self, corner_radius=0,fg_color=BACKGROUND_COLOR) 

        self.config_list_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=5)

    def _create_radio_buttons(self):
        options = self.profile_manager.get_profile_names()
        for i, option in enumerate(options):
            radio_button = customtkinter.CTkRadioButton(
                master=self.config_list_frame,
                text=option,
                variable=self.selected_option,
                value=option,
                font=(PRIMARY_FONT, 12, 'bold'),
                text_color=TEXT_COLOR,
                hover_color=BLUE_COLOR,
                border_color=SECONDARY_BACKGROUND,  
                radiobutton_width=13,
                radiobutton_height=13,
                border_width_unchecked=3,
                border_width_checked=3,
                fg_color=ORANGE_COLOR
            )
            radio_button.grid(row=i*2, column=0, padx=10, pady=0, sticky="w")
            if i < len(options) - 1:  
                canvas = tk.Canvas(
                    master=self.config_list_frame,
                    bg=SECONDARY_BACKGROUND,
                    height=1, 
                    width=200,
                    bd=0,
                    highlightthickness=0
                )
                canvas.grid(row=i*2+1, column=0, padx=0, pady=5, sticky="ew")
            radio_button.configure(command=lambda rb=radio_button: self._option_selected(rb))
            self.radio_buttons.append(radio_button) 

    def _option_selected(self, radio_button):
        selected_profile_name = radio_button.cget('value')

        radio_button.configure(text_color=ORANGE_COLOR)

        for rb in self.radio_buttons:
            if rb != radio_button:
                rb.configure(text_color=TEXT_COLOR)

        self.profile_manager.set_active_profile(selected_profile_name)
        self.list_profile_settings()

    def list_profile_settings(self):
        if(self.home_frame != None):
            self.home_frame.list_profile_settings()

    def _create_new_profile_button(self):
        new_profile_button = customtkinter.CTkButton(
            self,
            text="+ New Profile",
            font=(PRIMARY_FONT, 13, 'bold'),
            hover_color=ORANGE_COLOR,
            text_color=SECONDARY_TEXT_COLOR,
            fg_color=SECONDARY_BACKGROUND,
            command=self._new_profile,
            corner_radius=0
        )
        new_profile_button.grid(row=2, column=0, padx=10, pady=10, sticky="s")

        def on_enter(event):
            new_profile_button._on_enter(event)
            new_profile_button.configure(
                text_color=BACKGROUND_COLOR,
                fg_color=ORANGE_COLOR
            )

        def on_leave(event):
            new_profile_button._on_leave(event)
            new_profile_button.configure(
                text_color=SECONDARY_TEXT_COLOR,
                fg_color=SECONDARY_BACKGROUND
            )

        new_profile_button.bind("<Enter>", on_enter)
        new_profile_button.bind("<Leave>", on_leave)

    def select_option(self, option_name):
        if(self.selected_option.get() == option_name):
            return 
        
        for rb in self.radio_buttons:
            if rb.cget("value") == option_name:
                rb.invoke()

    def _new_profile(self):
        popup = customtkinter.CTkToplevel(self, fg_color=BACKGROUND_COLOR)
        popup.overrideredirect(True)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (350 / 2)
        y = (screen_height / 2) - (150 / 2)
        popup.geometry(f"+{int(x)}+{int(y)}")

        popup.attributes("-topmost", True)

        frame = customtkinter.CTkFrame(popup, fg_color=ORANGE_COLOR, corner_radius=3, width=350, height=150)
        frame.grid(row=0, column=0, padx=0, pady=0)

        inner_frame = customtkinter.CTkFrame(frame, fg_color=BACKGROUND_COLOR, corner_radius=3, width=330, height=130)
        inner_frame.grid(row=0, column=0, padx=3, pady=3)

        label = customtkinter.CTkLabel(inner_frame, text=f"Profile Name:", text_color=SECONDARY_TEXT_COLOR, font=(PRIMARY_FONT, 14, "bold"))
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        entry = customtkinter.CTkEntry(inner_frame,  font=(PRIMARY_FONT, 12), width=300, height=30, corner_radius=0, fg_color=BACKGROUND_COLOR, text_color=ORANGE_COLOR)
        entry.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        def create():
            profile_name = entry.get()
            if profile_name == "" or profile_name in self.profile_manager.get_profile_names():
                popup.destroy()
                messagebox.showerror("Error", "Profile name cannot be empty or already exists")
                return
            self.profile_manager.create_profile(entry.get())
            self.create_widgets()
            popup.destroy()

        button_frame = customtkinter.CTkFrame(inner_frame, fg_color=BACKGROUND_COLOR)
        button_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        yes_button = customtkinter.CTkButton(button_frame, text="Create", command=create, fg_color=ORANGE_COLOR, hover_color=ORANGE_COLOR, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        yes_button.grid(row=0, column=0, padx=10, pady=10)

        no_button = customtkinter.CTkButton(button_frame, text="Cancel", command=popup.destroy, fg_color=SECONDARY_BACKGROUND, hover_color=SECONDARY_BACKGROUND, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        no_button.grid(row=0, column=1, padx=10, pady=10)