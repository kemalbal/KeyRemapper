import customtkinter, os
from constants import *
import tkinter as tk
from macro_recorder import MacroRecorder
from tkinter import messagebox
from tkinter import filedialog

class HomeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color=SECONDARY_BACKGROUND)

        self.master = master
        self.profile_manager = master.profile_manager
        self.macro_recorder = MacroRecorder()
        self.current_macro = []
        self.activate_switch_var = customtkinter.StringVar(value="on")

        self.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self._create_header()
        self._create_bottom_buttons()
        self._create_split_frame()

    def _create_header(self):
        header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=SECONDARY_BACKGROUND, height=30)
        header_frame.grid_rowconfigure(0, weight=1)
        header_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def _create_split_frame(self):
        self.split_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.split_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.split_frame.grid_rowconfigure(1, weight=1)
        self.split_frame.grid_columnconfigure(0, weight=1)
        self.split_frame.grid_columnconfigure(1, weight=0)

    def _is_there_any_profile(self):
        profile_names = self.profile_manager.get_profile_names()
        if len(profile_names) == 0:
            return False
        else:
            return True

    def _select_trigger_program(self):
        file_path = filedialog.askopenfilename(
        title="Bir program seçin", 
        filetypes=[("Programlar", "*.exe")]) 
    
        if file_path:
            file_name = os.path.basename(file_path)
            self.trigger_program_entry.delete(0, customtkinter.END)  
            self.trigger_program_entry.insert(0, file_name)

    def _record_switch_key(self):
        self.record_keys_for_profile_switch.configure(text=" RECORDING ", fg_color=ORANGE_COLOR)

        def _start_recording():
            key_combination = self.macro_recorder.get_combination_or_single_word()
            self.profile_switch_key_entry.delete(0, tk.END)  
            self.profile_switch_key_entry.insert(0, key_combination)  
            self.record_keys_for_profile_switch.configure(text=" RECORD ", fg_color=TEXT_COLOR)

        self.after(100, _start_recording)

    def _activate(self):
        pass
        if self.activate_switch_var.get() == "on":
            self.profile_manager.start()
        else:
            self.profile_manager.stop()

    def _create_settings_frame(self):
        self.settings_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=BACKGROUND_COLOR)
        self.settings_frame.grid(row=1, column=1, padx=0, pady=0,sticky="nsew")    
        self.settings_frame.rowconfigure(0, weight=1)
        if not self._is_there_any_profile():
            return

        activate = customtkinter.CTkSwitch(self.settings_frame, text="activate", 
                                        variable=self.activate_switch_var, onvalue="on", offvalue="off", button_color=TEXT_COLOR, button_hover_color=TEXT_COLOR, text_color=TEXT_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                        progress_color=ORANGE_COLOR, font=(PRIMARY_FONT, 14), command=self._activate)
        activate.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="wes")
        self._activate()

        canvas = tk.Canvas(
            master=self.settings_frame,
            bg=SECONDARY_BACKGROUND,
            height=5, 
            width=230,
            bd=0,
            highlightthickness=0
        )
        canvas.grid(row=8, column=0, padx=0, pady=0, sticky="ew")

        select_program = customtkinter.CTkButton(self.settings_frame, text=" SELECT TRIGGER PROGRAM ", font=(PRIMARY_FONT, 14, "bold"), height=45,  corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._select_trigger_program)
        select_program.grid(row=9, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        
        self.trigger_program_entry = customtkinter.CTkEntry(self.settings_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40,  text_color=ORANGE_COLOR,
                                     placeholder_text="Program Name", placeholder_text_color=TEXT_COLOR)
        self.trigger_program_entry.grid(row=10, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        trigger_program_name = self.profile_manager.get_trigger_program()

        if trigger_program_name != "":
            self.trigger_program_entry.delete(0, customtkinter.END)
            self.trigger_program_entry.insert(0, trigger_program_name)

        canvas = tk.Canvas(
            master=self.settings_frame,
            bg=SECONDARY_BACKGROUND,
            height=5, 
            width=230,
            bd=0,
            highlightthickness=0
        )
        canvas.grid(row=12, column=0, padx=0, pady=0, sticky="ew")

        self.delete_active_profile = customtkinter.CTkButton(self.settings_frame, text=" DELETE ACTIVE PROFILE ", font=(PRIMARY_FONT, 14, "bold"), height=45,  corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self.delete_profile)
        self.delete_active_profile.grid(row=13, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        self.record_keys_for_profile_switch = customtkinter.CTkButton(self.settings_frame, text=" RECORD ", font=(PRIMARY_FONT, 14, "bold"), height=45,  corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._record_switch_key)
        self.record_keys_for_profile_switch.grid(row=14, column=0, padx=3, pady=3, sticky="we")

        self.profile_switch_key_entry = customtkinter.CTkEntry(self.settings_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40,  text_color=ORANGE_COLOR,
                                     placeholder_text="Profile Switch Key", placeholder_text_color=TEXT_COLOR)
        self.profile_switch_key_entry.grid(row=15, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        profile_switch_key = self.profile_manager.get_profile_switch_key()
        if profile_switch_key != "":
            self.profile_switch_key_entry.delete(0, customtkinter.END)
            self.profile_switch_key_entry.insert(0, profile_switch_key)

        profiles_for_switching_frame = customtkinter.CTkScrollableFrame(self.settings_frame, height=50 , bg_color="#1E1E1E", corner_radius=0, label_text="Profiles for Switching", label_font=(PRIMARY_FONT, 14), label_text_color=TEXT_COLOR)
        profiles_for_switching_frame.grid(row=16, column=0, columnspan=2, padx=3, pady=3, sticky="wens")
        profiles_for_switching_frame.grid_rowconfigure(0, weight=1)
        profiles_for_switching_frame.grid_columnconfigure(0, weight=1)

        switch_profiles = self.profile_manager.get_profile_switch_names()
        for index, profile_name in enumerate(switch_profiles):
            label = customtkinter.CTkLabel(profiles_for_switching_frame, text=profile_name, text_color=TEXT_COLOR, corner_radius=0, font=(PRIMARY_FONT, 14, "bold"))
            label.grid(row=index, column=0, pady=0, padx=5, sticky="ew")

            delete_switch_profile = customtkinter.CTkButton(profiles_for_switching_frame, text="X", font=(PRIMARY_FONT, 14, "bold"), height=40, width=40, corner_radius=0,
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                   command=lambda profile_name=profile_name: self._delete_switch_profile(profile_name))
            delete_switch_profile.grid(row=index, column=1, pady=5, padx=5, sticky="w")

        add_active_profile_to_switch_profiles = customtkinter.CTkButton(self.settings_frame, text=" Add Active Profile ", font=(PRIMARY_FONT, 14, "bold"), height=45,  corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._add_active_profile_to_switch_profiles)
        add_active_profile_to_switch_profiles.grid(row=17, column=0, padx=3, pady=3, sticky="we")

        canvas = tk.Canvas(
            master=self.settings_frame,
            bg=SECONDARY_BACKGROUND,
            height=5, 
            width=230,
            bd=0,
            highlightthickness=0
        )
        canvas.grid(row=19, column=0, padx=0, pady=0, sticky="ew")

        self.run_at_startup_switch_var = customtkinter.StringVar(value="off")
        run_at_startup = customtkinter.CTkSwitch(self.settings_frame, text="run at startup", 
                                        variable=self.run_at_startup_switch_var, onvalue="on", offvalue="off", button_color=TEXT_COLOR, button_hover_color=TEXT_COLOR, text_color=TEXT_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                        progress_color=ORANGE_COLOR, font=(PRIMARY_FONT, 14), command=self._run_at_startup)
        run_at_startup.grid(row=20, column=0, columnspan=2, padx=10, pady=10, sticky="wes")

    def _run_at_startup(self):
        messagebox.showinfo("Info", "Not implemented yet")
        self.run_at_startup_switch_var = customtkinter.StringVar(value="off")
        self._create_settings_frame()

    def _add_active_profile_to_switch_profiles(self):
        self.profile_manager.add_active_profile_to_profile_switch()
        self._create_settings_frame()

    def _delete_switch_profile(self, profile_name):
        self.profile_manager.delete_profile_switch(profile_name)
        self._create_settings_frame()

    def _create_bottom_buttons(self):
        if not self._is_there_any_profile():
            return
        
        bottom_button_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=BACKGROUND_COLOR)
        bottom_button_frame.grid(row=2, column=0, padx=0, pady=0, sticky="we")

        bottom_button_frame.grid_columnconfigure(0, weight=1)

        new_binding_button = customtkinter.CTkButton(bottom_button_frame, text="+ New Binding", font=(PRIMARY_FONT, 13, 'bold'), hover_color=ORANGE_COLOR, text_color=SECONDARY_TEXT_COLOR, fg_color=SECONDARY_BACKGROUND, corner_radius=0,
                                                     command=self.open_new_binding_panel)
        new_binding_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        revert_button = customtkinter.CTkButton(bottom_button_frame, command=self.revert_settings, text="Revert", font=(PRIMARY_FONT, 13, 'bold'), hover_color=ORANGE_COLOR, text_color=SECONDARY_TEXT_COLOR, fg_color=SECONDARY_BACKGROUND, corner_radius=0)
        revert_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        save_button = customtkinter.CTkButton(bottom_button_frame, text="Save", font=(PRIMARY_FONT, 13, 'bold'), 
                                              hover_color=ORANGE_COLOR, text_color=SECONDARY_TEXT_COLOR, fg_color=SECONDARY_BACKGROUND, corner_radius=0,
                                              command=self.save_settings)
        save_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        def on_enter(event):
            button = event.widget.master
            button._on_enter(event)
            button.configure(
                text_color=BACKGROUND_COLOR,
                fg_color=ORANGE_COLOR
            )

        def on_leave(event):
            button = event.widget.master
            button._on_leave(event)
            button.configure(
                text_color=SECONDARY_TEXT_COLOR,
                fg_color=SECONDARY_BACKGROUND
            )

        new_binding_button.bind("<Enter>", on_enter)
        new_binding_button.bind("<Leave>", on_leave)
        revert_button.bind("<Enter>", on_enter)
        revert_button.bind("<Leave>", on_leave)
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)

    def open_new_binding_panel(self, key=None):
        self.new_binding_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=SECONDARY_BACKGROUND)
        self.new_binding_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.new_binding_frame.grid_columnconfigure(1, weight=1)
        self.new_binding_frame.grid_rowconfigure(2, weight=1)

        self.record_keys_for_activation_button = customtkinter.CTkButton(self.new_binding_frame, text=" RECORD ", font=(PRIMARY_FONT, 14, "bold"), height=40, width=150, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._record_activation_key)
        self.record_keys_for_activation_button.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        self.activation_key_entry = customtkinter.CTkEntry(self.new_binding_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=600, text_color=ORANGE_COLOR,
                                                      placeholder_text="Activation Key or Combination", placeholder_text_color=TEXT_COLOR)
        
        self.activation_key_entry.grid(row=0, column=1, padx=3, pady=0, sticky="we")

        self._draw_separator(self.new_binding_frame, 1, 2)

        self.clear_macro_button = customtkinter.CTkButton(self.new_binding_frame, text=" CLEAR MACRO ", font=(PRIMARY_FONT, 14, "bold"), height=40, width=150, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._clear_macro)
        self.clear_macro_button.grid(row=3, column=0, padx=3, pady=3, sticky="w")
        
        self.record_macro_button = customtkinter.CTkButton(self.new_binding_frame, text=" RECORD MACRO ", font=(PRIMARY_FONT, 14, "bold"), height=40, width=150, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._record_macro)
        self.record_macro_button.grid(row=3, column=1, padx=3, pady=3, sticky="w")

        self.save_macro_button = customtkinter.CTkButton(self.new_binding_frame, text=" SAVE MACRO ", font=(PRIMARY_FONT, 14, "bold"), height=40, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._save_macro)
        self.save_macro_button.grid(row=3, column=1, padx=3, pady=3, sticky="e")

        self._open_new_binding_side_frame()

        if(key):
            key = key.lower()
            self.activation_key_entry.delete(0, tk.END)
            self.activation_key_entry.insert(0, key)

            active_profile_settings = self.profile_manager.get_active_profile_settings()
            self.current_macro = active_profile_settings.get(key, {}).get("actions", [])
            self._render_macro()

    def _save_macro(self):
        key = self.activation_key_entry.get()

        if not (key != "" and self.current_macro != [] and key != None):
            messagebox.showerror("Error", "Please fill in all the fields")
            return
        
        active_profile_settings = self.profile_manager.get_active_profile_settings()
        active_profile_settings[key] = {"actions": self.current_macro}
        self.profile_manager.save_active_profile_settings(active_profile_settings)
        self.list_profile_settings()
        
    def _render_macro(self):
        macro_frame = customtkinter.CTkScrollableFrame(self.new_binding_frame, corner_radius=0, fg_color="transparent")
        macro_frame.grid(row=2, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

        max_columns = 7
        current_row = 0
        current_column = 0

        for i, action in enumerate(self.current_macro):
            if action["action"] == "write":
                text = "Write: " + action["text"]
                label = customtkinter.CTkButton(macro_frame, text=f" {text} ", font=(PRIMARY_FONT, 14), 
                                                           width=50, height=40, corner_radius=0, fg_color=BACKGROUND_COLOR, hover_color=TEXT_COLOR, text_color=ORANGE_COLOR, command=lambda i=i: self._edit_macro(i))
                label.grid(row=current_row, column=current_column, padx=3, pady=3, sticky="nsew")

            elif action["action"] == "delay":
                text = "Delay: " + action["duration"] + " ms"
                label = customtkinter.CTkButton(macro_frame, text=f" {text} ", font=(PRIMARY_FONT, 14), 
                                                           width=50, height=40, corner_radius=0, fg_color=BACKGROUND_COLOR, hover_color=TEXT_COLOR, text_color=ORANGE_COLOR, command=lambda i=i: self._edit_macro(i))
                label.grid(row=current_row, column=current_column, padx=3, pady=3, sticky="nsew")

            else:
                if action["action"] == "press":
                    key_text = action["key"]
                elif action["action"] == "press_down":
                    key_text = f"{action['key']} (down)"
                elif action["action"] == "press_up":
                    key_text = f"{action['key']} (up)"

                button = customtkinter.CTkButton(macro_frame, text=f" {key_text.upper()} ", font=(PRIMARY_FONT, 14), 
                                                           width=50, height=40, corner_radius=5, fg_color=BACKGROUND_COLOR, hover_color=TEXT_COLOR, text_color=ORANGE_COLOR, border_color=TEXT_COLOR, border_width=2,
                                                           command=lambda i=i: self._edit_macro(i))
                button.grid(row=current_row, column=current_column, padx=3, pady=3, sticky="nsew")

            if i < len(self.current_macro) - 1:
                plus_label = customtkinter.CTkLabel(macro_frame, text="+", font=(PRIMARY_FONT, 20), text_color=SECONDARY_TEXT_COLOR)
                plus_label.grid(row=current_row, column=current_column + 1, padx=3, pady=3, sticky="nsew")
                current_column += 2  

            else:
                current_column += 1

            if current_column >= max_columns * 2:
                current_column = 0
                current_row += 1

        self.new_binding_frame.grid_rowconfigure(2, weight=1)
        self.new_binding_frame.grid_columnconfigure(0, weight=1)

    def _edit_macro(self, index):
        if(self.current_macro[index]["action"] in ["press", "press_down", "press_up"]):
            self._open_edit_key_panel(index)
        elif(self.current_macro[index]["action"] == "write"):
            self._open_edit_text_panel(index)
        elif(self.current_macro[index]["action"] == "delay"):
            self._open_edit_delay_panel(index)
        

    def _open_edit_text_panel(self, index):
        new_binding_side_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=BACKGROUND_COLOR)
        new_binding_side_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        new_binding_side_frame.columnconfigure(0, weight=1)

        textbox = customtkinter.CTkTextbox(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=125, width=120, text_color=ORANGE_COLOR, fg_color=BACKGROUND_COLOR, border_color=TEXT_COLOR, border_width=2)
        textbox.grid(row=11, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        textbox.insert("0.0", self.current_macro[index]["text"])

        def _change_text():
            self.current_macro[index]["text"] = textbox.get(0.0, "end-1c")
            self._render_macro()
            self._open_new_binding_side_frame()

        change_text_button = customtkinter.CTkButton(new_binding_side_frame, text=" CHANGE TEXT ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_change_text)
        change_text_button.grid(row=12, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        def _delete_text():
            self.current_macro.pop(index)
            self._render_macro()
            self._open_new_binding_side_frame()

        delete_text_button = customtkinter.CTkButton(new_binding_side_frame, text=" DELETE TEXT ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0,
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_delete_text)
        delete_text_button.grid(row=13, column=0, columnspan=2, padx=3, pady=3, sticky="we")

    def _open_edit_delay_panel(self, index):
        new_binding_side_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=BACKGROUND_COLOR)
        new_binding_side_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        new_binding_side_frame.columnconfigure(0, weight=1)

        delay_entry = customtkinter.CTkEntry(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR,
                                                      placeholder_text="Delay Duration", placeholder_text_color=TEXT_COLOR)
        delay_entry.grid(row=9, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        
        delay_entry.delete(0, tk.END)
        delay_entry.insert(0, self.current_macro[index]["duration"])

        def _change_delay():
            duration = delay_entry.get()
            if not duration.isnumeric():
                messagebox.showerror("Error", "Delay duration must be a number")
                return
            
            self.current_macro[index]["duration"] = duration
            self._render_macro()
            self._open_new_binding_side_frame()

        add_delay_button = customtkinter.CTkButton(new_binding_side_frame, text=" CHANGE DELAY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_change_delay)
        add_delay_button.grid(row=10, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        def _delete_delay():
            del self.current_macro[index]
            self._render_macro()
            self._open_new_binding_side_frame()

        delete_delay_button = customtkinter.CTkButton(new_binding_side_frame, text=" DELETE DELAY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0,
                                                    fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                    command=_delete_delay)
        delete_delay_button.grid(row=11, column=0, columnspan=2, padx=3, pady=3, sticky="we")

    def _open_edit_key_panel(self, index):
        new_binding_side_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=BACKGROUND_COLOR)
        new_binding_side_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        new_binding_side_frame.columnconfigure(0, weight=1)

        self.record_key_button = customtkinter.CTkButton(new_binding_side_frame, text=" RECORD ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._record_key)
        self.record_key_button.grid(row=4, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        optionmenu = customtkinter.CTkOptionMenu(new_binding_side_frame, values=["press", "press_down", "press_up"], 
                                                 corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR, fg_color=BACKGROUND_COLOR,
                                                 dropdown_text_color=ORANGE_COLOR, button_color=BACKGROUND_COLOR, button_hover_color=TEXT_COLOR, dropdown_hover_color=TEXT_COLOR,
                                                 bg_color=SECONDARY_BACKGROUND)
        optionmenu.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        self.key_entry = customtkinter.CTkEntry(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR,
                                            placeholder_text="Key", placeholder_text_color=TEXT_COLOR)
        self.key_entry.grid(row=6, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.current_macro[index]["key"])
        optionmenu.set(self.current_macro[index]["action"])

        def _change_key(index):
            self.current_macro[index]["action"] = optionmenu.get()
            self.current_macro[index]["key"] = self.key_entry.get()
            self._render_macro()
            self._open_new_binding_side_frame()

        change_key_button = customtkinter.CTkButton(new_binding_side_frame, text=" CHANGE KEY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0,
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command = lambda: _change_key(index))
        change_key_button.grid(row=7, column=0, padx=3, pady=3, sticky="we")
        
        def _delete_key(index):
            self.current_macro.pop(index)
            self._render_macro()
            self._open_new_binding_side_frame()

        delete_key_button = customtkinter.CTkButton(new_binding_side_frame, text=" DELETE KEY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0,
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command = lambda: _delete_key(index))
        delete_key_button.grid(row=7, column=1, padx=3, pady=3, sticky="we")
   

    def _open_new_binding_side_frame(self):
        new_binding_side_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=BACKGROUND_COLOR)
        new_binding_side_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

        new_binding_side_frame.columnconfigure(0, weight=1)

        self.record_key_button = customtkinter.CTkButton(new_binding_side_frame, text=" RECORD KEY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                   fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2, command=self._record_key)
        self.record_key_button.grid(row=4, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        optionmenu = customtkinter.CTkOptionMenu(new_binding_side_frame, values=["press", "press_down", "press_up"], 
                                                 corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR, fg_color=BACKGROUND_COLOR,
                                                 dropdown_text_color=ORANGE_COLOR, button_color=BACKGROUND_COLOR, button_hover_color=TEXT_COLOR, dropdown_hover_color=TEXT_COLOR,
                                                 bg_color=SECONDARY_BACKGROUND)
        optionmenu.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        optionmenu.set("press")

        self.key_entry = customtkinter.CTkEntry(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR,
                                         placeholder_text="Key", placeholder_text_color=TEXT_COLOR)
        self.key_entry.grid(row=7, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        
        def _add_key():
            self.current_macro.append({"key": self.key_entry.get(), "action": optionmenu.get()})
            self._render_macro()
            optionmenu.set("press")
            self.key_entry.delete(0, tk.END)

        add_key_button = customtkinter.CTkButton(new_binding_side_frame, text=" ADD KEY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_add_key)
        add_key_button.grid(row=8, column=0, padx=3, pady=3, sticky="we")

        delay_entry = customtkinter.CTkEntry(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=40, width=120, text_color=ORANGE_COLOR,
                                                      placeholder_text="Delay Duration", placeholder_text_color=TEXT_COLOR)
        delay_entry.grid(row=9, column=0, columnspan=2, padx=3, pady=3, sticky="we")
        
        def _add_delay():
            duration = delay_entry.get()
            if not duration.isnumeric():
                messagebox.showerror("Error", "Delay duration must be a number")
                return
            self.current_macro.append({"action": "delay", "duration": delay_entry.get()})
            delay_entry.delete(0, tk.END)
            self._render_macro()

        add_delay_button = customtkinter.CTkButton(new_binding_side_frame, text=" ADD DELAY ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_add_delay)
        add_delay_button.grid(row=10, column=0, columnspan=2, padx=3, pady=3, sticky="we")


        textbox = customtkinter.CTkTextbox(new_binding_side_frame, corner_radius=0, font=(PRIMARY_FONT, 14), height=125, width=120, text_color=ORANGE_COLOR, fg_color=BACKGROUND_COLOR, border_color=TEXT_COLOR, border_width=2)
        textbox.grid(row=11, column=0, columnspan=2, padx=3, pady=3, sticky="we")

        def _add_text():
            self.current_macro.append({"action": "write", "text": textbox.get(0.0, "end-1c")})
            textbox.delete(0.0, "end-1c")
            self._render_macro()


        add_text_button = customtkinter.CTkButton(new_binding_side_frame, text=" ADD TEXT ", font=(PRIMARY_FONT, 14, "bold"), height=45, width=60, corner_radius=0, 
                                                fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, border_color=BACKGROUND_COLOR, border_width=2,
                                                command=_add_text)
        add_text_button.grid(row=12, column=0, columnspan=2, padx=3, pady=3, sticky="we")

    def _clear_macro(self):
        self.current_macro = []
        self._render_macro()

    def _record_macro(self):
        if not self.macro_recorder.is_recording:
            self.record_macro_button.configure(text=" STOP RECORDING ", fg_color=ORANGE_COLOR)
    
            def _start_recording():
                self.macro_recorder.start_recording()

            self.after(100, _start_recording)
        else:
            self.record_macro_button.configure(text=" RECORD MACRO ", fg_color=TEXT_COLOR)
            self.macro_recorder.stop_recording()
            self.current_macro = self.macro_recorder.get_macro()
            self._render_macro()

    def _record_key(self):
        self.record_key_button.configure(text=" RECORDING ", fg_color=ORANGE_COLOR)

        def _start_recording():
            key_combination = self.macro_recorder.get_combination_or_single_word()
            self.key_entry.delete(0, tk.END)  
            self.key_entry.insert(0, key_combination)  
            self.record_key_button.configure(text=" RECORD ", fg_color=TEXT_COLOR)

        self.after(100, _start_recording)


    def _record_activation_key(self):
        self.record_keys_for_activation_button.configure(text=" RECORDING ", fg_color=ORANGE_COLOR)

        def _start_recording():
            key_combination = self.macro_recorder.get_combination_or_single_word()
            self.activation_key_entry.delete(0, tk.END)  
            self.activation_key_entry.insert(0, key_combination)  
            self.record_keys_for_activation_button.configure(text=" RECORD ", fg_color=TEXT_COLOR)

        self.after(100, _start_recording)

    def _draw_separator(self, master, row, span, orientation='horizontal', sticky="ew"):
        canvas = tk.Canvas(
            master=master,
            bg=BACKGROUND_COLOR,
            height=4, 
            bd=0,
            highlightthickness=0
        )
        canvas.grid(row=row, column=0, columnspan=span, padx=0, pady=5, sticky=sticky)

        def resize_canvas(event):
            canvas_width = event.width
            canvas.delete("all")
            canvas.create_line(0, 0, canvas_width, 0, fill=TEXT_COLOR, width=2)
            canvas.create_line(0, 2, canvas_width, 2, fill=BACKGROUND_COLOR, width=2)

        canvas.bind("<Configure>", resize_canvas)

    def save_settings(self):
        trigger_program_name = self.trigger_program_entry.get()
        if(trigger_program_name != ""):
            file_name = os.path.basename(trigger_program_name)
            self.profile_manager.set_trigger_program(file_name)

        profile_switch_key = self.profile_switch_key_entry.get()
        if(profile_switch_key != ""):
            self.profile_manager.set_profile_switch_key(profile_switch_key)

        self.profile_manager.save_config()
        messagebox.showinfo("Save Settings", "Settings saved!")

    def revert_settings(self):
        active_profile_name = self.profile_manager.get_active_profile_name()
        self.profile_manager.load_config()
        self.profile_manager.set_active_profile(active_profile_name)
        self.list_profile_settings()

    def list_profile_settings(self):
        active_profile_settings = self.profile_manager.get_active_profile_settings()
        if len(active_profile_settings) > 9:
            buttons_frame = customtkinter.CTkScrollableFrame(self.split_frame, corner_radius=0, 
                                                             fg_color=SECONDARY_BACKGROUND, scrollbar_button_color=BACKGROUND_COLOR, scrollbar_button_hover_color=ORANGE_COLOR)
        else:
            buttons_frame = customtkinter.CTkFrame(self.split_frame, corner_radius=0, fg_color=SECONDARY_BACKGROUND)
            
        buttons_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        buttons_frame.grid_columnconfigure(4, weight=1)

        for i, (key, actions) in enumerate(sorted(active_profile_settings.items())):
            button = customtkinter.CTkButton(buttons_frame, text=f" {key.upper()} ", font=(PRIMARY_FONT, 14), width=50, height=40, corner_radius=5, fg_color=BACKGROUND_COLOR, 
                                             hover_color=TEXT_COLOR, text_color=ORANGE_COLOR, border_color=TEXT_COLOR, border_width=2,
                                             command=lambda key=key.upper(): self.open_new_binding_panel(key))
            button.grid(row=i * 2, column=0, padx=10, pady=3)

            arrow_label = customtkinter.CTkLabel(buttons_frame, text="→", font=(PRIMARY_FONT, 30), width=10, height=20, corner_radius=0, fg_color=SECONDARY_BACKGROUND, text_color=ORANGE_COLOR)
            arrow_label.grid(row=i * 2, column=1, padx=3, pady=3)

            macro_frame = customtkinter.CTkFrame(buttons_frame, corner_radius=0, fg_color="transparent", height=50)
            macro_frame.grid(row=i * 2, column=2, padx=3, pady=3, sticky="w")

            for ai, action in enumerate(actions["actions"]):
                if action["action"] == "write":
                    text = "Write: " + action["text"]
                    label = customtkinter.CTkLabel(macro_frame, text=f" {text} ", font=(PRIMARY_FONT, 14), height=40, width=50, corner_radius=5, bg_color=BACKGROUND_COLOR, text_color=ORANGE_COLOR)
                    label.grid(row=i * 2, column=ai * 2, padx=3, pady=3, sticky="nsew")
                    pass
                elif action['action'] == 'delay':
                    text = "Delay: " + action["duration"] + " ms"
                    label = customtkinter.CTkLabel(macro_frame, text=f" {text} ", font=(PRIMARY_FONT, 14), height=40, width=50, corner_radius=5, bg_color=BACKGROUND_COLOR, text_color=ORANGE_COLOR)
                    label.grid(row=i * 2, column=ai * 2, padx=3, pady=3, sticky="nsew")
                else:
                    if(action["action"] == "press"):
                        key_text = action["key"]
                    elif action["action"] == "press_down":
                        key_text = action["key"] + " (down)"
                    elif action["action"] == "press_up":
                        key_text = action["key"] + " (up)"
                    macro_button = customtkinter.CTkButton(macro_frame, text=f" {key_text.upper()} ", font=(PRIMARY_FONT, 14), 
                                                           width=50, height=40, corner_radius=5, fg_color=BACKGROUND_COLOR, hover_color=BACKGROUND_COLOR, text_color=ORANGE_COLOR, border_color=TEXT_COLOR, border_width=2)
                    macro_button.grid(row=i * 2, column=ai * 2, padx=3, pady=3)
                if ai < len(actions["actions"]) - 1:
                    plus_label = customtkinter.CTkLabel(macro_frame, text="+", font=(PRIMARY_FONT, 30), width=10, height=20, corner_radius=0, fg_color=SECONDARY_BACKGROUND, text_color=ORANGE_COLOR)
                    plus_label.grid(row=i * 2, column=ai * 2 + 1, padx=3, pady=3)
                if ai > 3:
                    plus_label = customtkinter.CTkLabel(macro_frame, text="...", font=(PRIMARY_FONT, 30), width=10, height=20, corner_radius=0, fg_color=SECONDARY_BACKGROUND, text_color=ORANGE_COLOR)
                    plus_label.grid(row=i * 2, column=ai * 2 + 1, padx=3, pady=3)
                    break
                
            delete_button = customtkinter.CTkButton(buttons_frame, text=" DELETE ", font=(PRIMARY_FONT, 14, "bold"), width=50, height=40, corner_radius=0, fg_color=TEXT_COLOR, hover_color=ORANGE_COLOR, text_color=BACKGROUND_COLOR, 
                                                    border_color=BACKGROUND_COLOR, border_width=2, command=lambda key=key: self.delete_profile_setting(key))
            delete_button.grid(row=i * 2, column=4, padx=10, pady=3, sticky="e") 

            self._draw_separator(buttons_frame, i * 2 + 1, 5, sticky="ew")

        self._create_settings_frame()


    def delete_profile_setting(self, key):
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

        label = customtkinter.CTkLabel(inner_frame, text=f"Are you sure you want to delete the '{key.upper()}' configuration?", text_color=SECONDARY_TEXT_COLOR, font=(PRIMARY_FONT, 12), wraplength=300)
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        def delete():
            self.profile_manager.delete_profile_setting(key)
            self.list_profile_settings()
            popup.destroy()

        button_frame = customtkinter.CTkFrame(inner_frame, fg_color=BACKGROUND_COLOR)
        button_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        yes_button = customtkinter.CTkButton(button_frame, text="Yes", command=delete, fg_color=ORANGE_COLOR, hover_color=ORANGE_COLOR, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        yes_button.grid(row=0, column=0, padx=10, pady=10)

        no_button = customtkinter.CTkButton(button_frame, text="No", command=popup.destroy, fg_color=SECONDARY_BACKGROUND, hover_color=SECONDARY_BACKGROUND, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        no_button.grid(row=0, column=1, padx=10, pady=10)

    def delete_profile(self):
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

        active_profile_name = self.profile_manager.get_active_profile_name()
        label = customtkinter.CTkLabel(inner_frame, text=f"Are you sure you want to delete the '{active_profile_name}' profile?", text_color=SECONDARY_TEXT_COLOR, font=(PRIMARY_FONT, 12), wraplength=300)
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        def delete():
            self.profile_manager.delete_active_profile()
            self.master.navigation_frame.create_widgets()
            profile_names = self.profile_manager.get_profile_names()
            if len(profile_names) == 0:
                self.list_profile_settings()
            popup.destroy()

        button_frame = customtkinter.CTkFrame(inner_frame, fg_color=BACKGROUND_COLOR)
        button_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        yes_button = customtkinter.CTkButton(button_frame, text="Yes", command=delete, fg_color=ORANGE_COLOR, hover_color=ORANGE_COLOR, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        yes_button.grid(row=0, column=0, padx=10, pady=10)

        no_button = customtkinter.CTkButton(button_frame, text="No", command=popup.destroy, fg_color=SECONDARY_BACKGROUND, hover_color=SECONDARY_BACKGROUND, text_color=BUTTON_TEXT_COLOR, font=(PRIMARY_FONT, 12))
        no_button.grid(row=0, column=1, padx=10, pady=10)

    