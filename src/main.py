import tkinter as tk
import csv
from pathlib import Path
import simpleaudio as sa

class timerApp:
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.root.title("Timer")

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

        self.running = False
    
    def start(self):
        if not self.running:
            self.running = True
            self.file = open(self.path, newline="")
            self.reader = csv.DictReader(self.file)
            self.next_row()
    
    def next_row(self):
        try:
            row = next(self.reader)
            self.beep()
            self.current_title = row["position"]
            self.label_title.config(text=self.current_title)
            self.target_time = int(row["time"])
            self.seconds = 0
            self.update_timer()
        except StopIteration:
            self.file.close()
            self.label_title.config(text="FINISHED!")
            self.label_time.config(text="0:00")
            self.start_btn.config(text="Restart")
            self.running = False

    
    def update_timer(self):
        if self.running:
            self.seconds += 1
            mins, secs = divmod(self.seconds, 60)
            self.label_time.config(text=f"{mins}:{secs:02d}")
            if self.seconds < self.target_time:
                self.root.after(1000, self.update_timer)
            else:
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
        beep_file = Path(__file__).parent.parent / "beep.wav"
        wave_obj = sa.WaveObject.from_wave_file(str(beep_file))
        wave_obj.play()
                        
        
root = tk.Tk()
path = Path(__file__).parent.parent / "stretches.csv"
app = timerApp(root, path)
root.mainloop()
