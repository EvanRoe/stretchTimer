import tkinter as tk

class timerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.seconds = 0

        self.label_title = tk.Label(root, text="Stretch Timer", font=("Arial", 20))
        self.label_title.pack()
        
        self.label_time = tk.Label(root, text="0:00", font=("Arial", 40))
        self.label_time.pack()

        self.start_btn = tk.Button(root,  text="Start", command=self.start)
        self.start_btn.pack()

        self.running = False
    
    def start(self):
        if not self.running:
            self.running = True
            self.update_timer()
    
    def update_timer(self):
        if self.running:
            self.seconds += 1
            mins, secs = divmod(self.seconds, 60)
            self.label_time.config(text=f"{mins}:{secs:02d}")
            self.root.after(1000, self.update_timer)

root = tk.Tk()
app = timerApp(root)
root.mainloop()
