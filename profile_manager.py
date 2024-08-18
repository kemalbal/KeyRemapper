import json
from hotkey_manager import HotkeyManager

class ProfileManager(HotkeyManager):
    def __init__(self, config_path = "config.json"):
        super().__init__(config_path)
        self.create_default_profile_if_necessary()

    def create_default_profile_if_necessary(self):
        if len(self.get_profile_names()) == 0:
            if "profiles" not in self.config:
                self.config["profiles"] = {}
            self.config["profiles"]["default"] = {}
            self.set_active_profile('default', True)
    
    def create_profile(self, profile_name):
        if profile_name in self.get_profile_names():
            return
        self.config["profiles"][profile_name] = {}
        self.set_active_profile(profile_name)

    def get_profile_names(self):
        return list(self.config.get("profiles", {}).keys())

    def save_active_profile_settings(self, active_profile_settings):
        active_profile_name = self.get_active_profile_name()
        self.config["profiles"][active_profile_name] = active_profile_settings
        self.save_config()

    def set_active_profile(self, profile_name, save_config = False):
        self.config["active_profile"] = profile_name
        self.start()
        if save_config:
            self.save_config()
        
    def save_config(self):
        with open("config.json", 'w') as file:
            json.dump(self.config, file)

    def delete_profile_setting(self, setting_name, save_config = False):
        profile_settings = self.get_active_profile_settings()
        del profile_settings[setting_name]
        if save_config:
            self.save_config()

    def delete_active_profile(self, save_config = False):
        active_profile_name = self.get_active_profile_name()
        if active_profile_name == "":
            return
        del self.config["profiles"][active_profile_name]
        del self.config["active_profile"]

        profile_names = self.get_profile_names()
        if len(profile_names) > 0:
            self.set_active_profile(profile_names[0])

        if save_config:
            self.save_config()

    def get_profile_switch_names(self):
        return self.config.get("profile_switch", {}).get("profiles", [])
    
    def get_profile_switch_key_combination(self):
        return self.config.get("profile_switch", {}).get("key_combination", "")
    
    def delete_profile_switch(self, profile_name, save_config = False):
        profile_names = self.get_profile_switch_names()
        if profile_name in profile_names:
            profile_names.remove(profile_name)
        
        if save_config:
            self.save_config()
    
    def add_active_profile_to_profile_switch(self, save_config = False):
        switch_profile_names = self.get_profile_switch_names()

        if "profile_switch" not in self.config:
            self.config["profile_switch"] = {}
        if "profiles" not in self.config["profile_switch"]:
            self.config["profile_switch"]["profiles"] = []

        if self.get_active_profile_name() not in switch_profile_names:
            self.config["profile_switch"]["profiles"].append(self.get_active_profile_name())

        if save_config:
            self.save_config()

    def set_trigger_program(self, program_name, save_config = False):
        active_profile_name = self.get_active_profile_name()
        if active_profile_name == "":
            return

        if "auto_switch" not in self.config:
            self.config["auto_switch"] = {}
        if "programs" not in self.config["auto_switch"]:
            self.config["auto_switch"]["programs"] = {}

        self.config["auto_switch"]["programs"][active_profile_name] = program_name

        if save_config:
            self.save_config()

    def get_trigger_program(self):
        active_profile_name = self.get_active_profile_name()
        if active_profile_name == "":
            return ""

        return self.config.get("auto_switch", {}).get("programs", {}).get(active_profile_name, "")

    def set_profile_switch_key(self, key, save_config = False):
        if "profile_switch" not in self.config:
            self.config["profile_switch"] = {}
        self.config["profile_switch"]["key_combination"] = key
        if save_config:
            self.save_config()

    def get_profile_switch_key(self):
        return self.config.get("profile_switch", {}).get("key_combination", "")

