import tkinter as tk
from tkinter import messagebox
import csv
from pathlib import Path
import simpleaudio as sa
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class timerApp:
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.root.title("Timer")

        self.audio_player = AudioPlayer()

        self.label_title = tk.Label(root, text="Stretch Timer", font=("Arial", 50))
        self.label_title.pack()
        
        self.label_time = tk.Label(root, text="0:00", font=("Arial", 60))
        self.label_time.pack()

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.start_btn = tk.Button(button_frame,  text="Start", font=("Arial", 30), command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(button_frame, text="Reset", font=("Arial", 30), command=self.reset)
        self.reset_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(button_frame, text="Pause", font=("Arial", 30), command=self.toggle_pause)
        self.pause_btn.pack(side="left", padx=5)

        self.label_next = tk.Label(root, text="", font=("Arial", 0))
        self.label_next.pack()

        self.running = False
    
    def start(self):
        if not self.running:
            self.running = True
            self.file = open(self.path, newline="")
            self.file2 = open(self.path, newline="")
            self.peek = csv.DictReader(self.file2)
            self.next_position = next(self.peek)
            self.reader = csv.DictReader(self.file)
            self.next_row()
    
    def next_row(self):
        try:
            self.next_position = next(self.peek)
            row = next(self.reader)
            self.current_title = row["position"]
            self.label_title.config(text=self.current_title)
            self.target_time = int(row["time"])
            if self.current_title == "rest":
                self.label_next.config(text=self.next_position["position"], font=("Arial", 40))
            else:
                self.label_next.config(text="", font=("Arial", 0))
            self.seconds = 0
            self.update_timer()
        except StopIteration:
            self.file.close()
            self.file2.close()
            self.beep()
            self.label_title.config(text="FINISHED!")
            self.label_time.config(text="0:00")
            self.running = False

    
    def update_timer(self):
        if self.running:
            self.seconds += 1
            mins, secs = divmod(self.seconds, 60)
            self.label_time.config(text=f"{mins}:{secs:02d}")

            if self.seconds < self.target_time:
                if self.current_title == "rest":
                    time_left = self.target_time - self.seconds
                    if time_left <= 2:
                        self.beep()
                
                self.root.after(1000, self.update_timer)
            else:
                self.beep()
                self.root.after(1000, self.next_row)
    
    def toggle_pause(self):
        self.running = not self.running
        if self.running:
            self.pause_btn.config(text="Pause")
            self.update_timer()
        else:
            self.pause_btn.config(text="Play")
    
    def reset(self):
        self.running = False
        self.seconds = 0
        self.label_time.config(text="0:00")
        self.label_title.config(text="Stretch Timer")

    def beep(self):
        self.audio_player.play_beep()

class AudioPlayer:
    def __init__(self):
        self.wav_file = "beep.wav"
        self.wav_path = resource_path(self.wav_file)
        self._check_file_exists()
    
    def _check_file_exists(self):
        if not os.path.exists(self.wav_path):
            print(f"WARNING: Audio file not found at: {self.wav_path}")
            try:
                if hasattr(sys, '_MEIPASS'):
                    temp_dir = sys._MEIPASS
                    print(f"Files in temp directory ({temp_dir}):")
                    for f in os.listdir(temp_dir):
                        print(f"  - {f}")
            except:
                pass
    
    def play_beep(self):
        try:
            wav_path_str = str(self.wav_path)
            if not os.path.exists(wav_path_str):
                print(f"Cannot find audio file: {wav_path_str}")
                self._fallback_beep()
                return False
            wave_obj = sa.WaveObject.from_wave_file(wav_path_str)
            play_obj = wave_obj.play()
        
        except Exception as e:
            print(f"Audio error: {e}")
            self._fallback_beep()
            return None
    
    def _fallback_beep(self):
        try:
            import winsound
            winsound.Beep(1000, 200)
            print("Used fallback beep")
        except Exception as e:
            print(f"Fallback also failed: {e}")
                        
        
root = tk.Tk()
path = resource_path("stretches.csv")
app = timerApp(root, path)
root.mainloop()
