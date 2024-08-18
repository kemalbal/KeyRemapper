import keyboard
import json
import time

class MacroRecorder:
    def __init__(self):
        self.recorded_macro = []
        self.is_recording = False
        self.last_time = None

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recorded_macro = []
        self.is_recording = True
        self.last_time = time.time()
        keyboard.hook(self.record_event, True)

    def stop_recording(self):
        self.is_recording = False
        keyboard.unhook_all()

    def record_event(self, event):
        if self.is_recording:
            current_time = time.time()
            delay = current_time - self.last_time
            self.last_time = current_time
            self.recorded_macro.append((event, delay))

    def get_combination_or_single_word(self):
        combination = []

        key_event = keyboard.read_event(True)
        while key_event.event_type != keyboard.KEY_UP:
            if key_event.name not in combination:
                combination.append(key_event.name)
            key_event = keyboard.read_event(True)  

        return '+'.join(combination)

    def get_macro(self):        
        actions = []
        i = 0
        while i < len(self.recorded_macro):
            event, delay = self.recorded_macro[i]
            
            if delay > 0:
                actions.append({"action": "delay", "duration": f"{int(delay * 1000)}"})
            
            if event.event_type == keyboard.KEY_DOWN:
                if (i + 1 < len(self.recorded_macro) and 
                    self.recorded_macro[i + 1][0].event_type == keyboard.KEY_UP and 
                    self.recorded_macro[i + 1][0].name == event.name):
                    actions.append({"action": "press", "key": event.name})
                    i += 1  
                else:
                    actions.append({"action": "press_down", "key": event.name})
            
            elif event.event_type == keyboard.KEY_UP:
                actions.append({"action": "press_up", "key": event.name})
            
            i += 1  
        
        return actions
