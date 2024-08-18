import ctypes
import psutil
import json
import keyboard
import time

class HotkeyManager:
    def __init__(self, config_path = "config.json"):
        self.config_path = config_path
        self.hotkeys = []
        self.last_foreground_exe = ""
        self.switch_profile_callback = None
        self.activation = False
        self.load_config()
        
    def set_config(self, config):
        self.config = config

    def get_profile_names(self):
        return list(self.config.get("profiles", {}).keys())

    def get_valid_switch_profiles(self):
        profile_names = self.get_profile_names()
        profiles = self.config.get("profile_switch", {}).get("profiles", [])
        return [profile for profile in profiles if profile in profile_names]

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.config_path, 'w') as file:
                self.config = {}

    def get_active_profile_name(self):
        return self.config.get("active_profile", "")

    def get_active_profile_settings(self):
        active_profile_name = self.get_active_profile_name()
        return self.config.get("profiles", {}).get(active_profile_name, {})

    def execute_action(self, action):
        if action["action"] == "press":
            keyboard.press_and_release(action["key"])
        elif action["action"] == "press_down":
            keyboard.press(action["key"])
        elif action["action"] == "press_up":
            keyboard.release(action["key"])
        elif action["action"] == "write":
            keyboard.write(action["text"])
        elif action["action"] == "delay":
            print("duration", action["duration"])
            time.sleep(float(action["duration"]) / 1000.0)

    def on_key_press(self, actions):
        for action in actions:
            self.execute_action(action)
        return False  

    def setup_hotkeys(self):
        for hotkey in self.hotkeys:
            keyboard.remove_hotkey(hotkey)
        self.hotkeys = []

        active_profile_settings = self.get_active_profile_settings()
        for key, settings in active_profile_settings.items():
            actions = settings.get("actions", [])
            hotkey = keyboard.add_hotkey(key, lambda a=actions: self.on_key_press(a), suppress=True)
            self.hotkeys.append(key)  

        profile_switch = self.config.get("profile_switch", {})
        switch_key = profile_switch.get("key_combination", "")
        if switch_key:
            keyboard.add_hotkey(switch_key, self.switch_profile, suppress=True)
            self.hotkeys.append(switch_key) 


    def switch_profile(self):
        switch_profiles = self.get_valid_switch_profiles()
        active_profile_name = self.get_active_profile_name()            

        if switch_profiles:
            if active_profile_name not in switch_profiles:
                self.current_profile_index = 0
            else:
                self.current_profile_index = switch_profiles.index(active_profile_name)
            self.current_profile_index = (self.current_profile_index + 1) % len(switch_profiles)
            new_profile_name = switch_profiles[self.current_profile_index]
            self.config["active_profile"] = new_profile_name

            if self.switch_profile_callback:
                self.switch_profile_callback(new_profile_name)

    def set_switch_profile_callback(self, callback):
        self.switch_profile_callback = callback

    def get_foreground_window_exe(self):
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process = psutil.Process(pid.value)
        return process.name()

    def check_auto_switch(self):
        if not self.activation:
            return
        foreground_exe = self.get_foreground_window_exe()
        if(self.last_foreground_exe == foreground_exe):
            return
        
        profile_names = self.get_profile_names()
        auto_switch_programs = {profile: path for profile, path in self.config.get("auto_switch", {}).get("programs", {}).items() if profile in profile_names}
        active_profile_name = self.get_active_profile_name()
        self.last_foreground_exe = foreground_exe
        for profile_name, exe_path in auto_switch_programs.items():
            if foreground_exe.lower() == exe_path.lower():
                if profile_name != active_profile_name:
                    self.config["active_profile"] = profile_name
                    print(f"Auto-switched to profile: {profile_name}")
                    if self.switch_profile_callback:
                        self.switch_profile_callback(profile_name)

    def start(self):
        self.activation = True
        self.setup_hotkeys()

    def stop(self):
        self.activation = False
        for hotkey in self.hotkeys:
            keyboard.remove_hotkey(hotkey)
        self.hotkeys = []
