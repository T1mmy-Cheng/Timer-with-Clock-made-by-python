import tkinter as tk
from tkinter import ttk, messagebox
import time, threading, math, ctypes
from datetime import datetime

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.fullscreen = False
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        self.root.tk.call('tk', 'scaling', 1.0)  # Set DPI scaling to 100%
        self.running = False
        self.time_left = 0
        self.fonts = {}
        self.button_style = ttk.Style()

        self._configure_window()
        self._init_vars()
        self._build_ui()
        self._layout_ui()
        # bind traces here, after timer_label exists
        self.hour_var.trace_add('write', lambda *args: self.update_timer_label_from_spinbox())
        self.min_var.trace_add('write', lambda *args: self.update_timer_label_from_spinbox())
        self.sec_var.trace_add('write', lambda *args: self.update_timer_label_from_spinbox())

        self.update_fonts_and_buttons()
        self.update_clock()
        self.update_analog_clock()

    # ---------- Window & Layout ----------
    def _configure_window(self):
        # Column weights for centering
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=2)
        self.root.columnconfigure(3, weight=2)
        self.root.columnconfigure(4, weight=2)
        self.root.columnconfigure(5, weight=1)

        # Row weights for vertical balance
        self.root.rowconfigure(0, weight=1)  # input row
        self.root.rowconfigure(1, weight=2)  # timer label
        self.root.rowconfigure(2, weight=2)  # buttons
        self.root.rowconfigure(3, weight=1)  # clock label
        self.root.rowconfigure(4, weight=3)  # analog clock
        self.root.rowconfigure(5, weight=1)  # settings/exit
        desired_width = 1600
        desired_height = 900
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        self.root.title("Countdown Timer")
        self.root.geometry(f"{desired_width}x{desired_height}")
        self.root.minsize(800, 600)
        self.root.maxsize(sw, sh)
        self.root.resizable(True, True)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Configure>', self.on_resize)

        for i in range(6):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)


    def _init_vars(self):
        self.hour_var, self.min_var, self.sec_var = tk.StringVar(value="0"), tk.StringVar(value="0"), tk.StringVar(value="0")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        # ~30–35% of the smaller screen dimension, capped at 500px
        self.canvas_size = min(int(min(screen_w, screen_h) * 0.33), 500)

    # ---------- UI ----------
    def _build_ui(self):
        self.hour_label = ttk.Label(self.root, text="Hour:")
        self.hour_spin = tk.Spinbox(self.root, from_=0, to=23, width=3, justify="center", textvariable=self.hour_var, command=self.update_timer_label_from_spinbox)
        self.min_label = ttk.Label(self.root, text="Min:")
        self.min_spin = tk.Spinbox(self.root, from_=0, to=59, width=3, justify="center", textvariable=self.min_var, command=self.update_timer_label_from_spinbox)
        self.sec_label = ttk.Label(self.root, text="Sec:")
        self.sec_spin = tk.Spinbox(self.root, from_=0, to=59, width=3, justify="center", textvariable=self.sec_var, command=self.update_timer_label_from_spinbox)

        self.timer_label = ttk.Label(self.root, text="00:00:00", anchor="center")
        self.start_btn = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.stop_btn = ttk.Button(self.root, text="Stop", command=self.stop_timer)
        self.reset_btn = ttk.Button(self.root, text="Reset", command=self.reset_timer)
        self.clock_label = ttk.Label(self.root, text="", anchor="center")

        self.clock_canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white", highlightthickness=0, bd=0)

        self.exit_btn = ttk.Button(self.root, text="Exit", command=self.root.destroy)
        self.settings_btn = ttk.Button(self.root, text="Settings", command=self.open_settings)

    def _layout_ui(self):
        self.hour_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.hour_spin.grid(row=0, column=1, padx=2, pady=5, sticky="nsew")
        self.min_label.grid(row=0, column=2, padx=2, pady=5, sticky="nsew")
        self.min_spin.grid(row=0, column=3, padx=2, pady=5, sticky="nsew")
        self.sec_label.grid(row=0, column=4, padx=2, pady=5, sticky="nsew")
        self.sec_spin.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")

        self.timer_label.grid(row=1, column=0, columnspan=6, pady=10, sticky="nsew")
        self.start_btn.grid(row=2, column=1, padx=5, pady=8, sticky="nsew")
        self.stop_btn.grid(row=2, column=2, padx=5, pady=8, sticky="nsew")
        self.reset_btn.grid(row=2, column=3, padx=5, pady=8, sticky="nsew")

        self.clock_label.grid(row=3, column=0, columnspan=6, pady=5, sticky="nsew")
        self.clock_canvas.grid(row=4, column=0, columnspan=6, pady=2, sticky="nsew")

        self.settings_btn.grid(row=5, column=4, padx=8, pady=8, sticky="nsew")
        self.exit_btn.grid(row=5, column=5, padx=8, pady=8, sticky="nsew")

    # ---------- Appearance ----------
    def update_fonts_and_buttons(self):
        """Recalculate font sizes and button padding based on current window height."""
        window_h = self.root.winfo_height() or self.root.winfo_screenheight()

        # Font size calculations
        self.fonts = {
            'big':   ("Segoe UI", max(28, min(72, window_h // 16)), "bold"),
            'med':   ("Segoe UI", max(16, min(48, window_h // 32)), "bold"),
            'small': ("Segoe UI", max(10, min(28, window_h // 60)))
        }

        # Separate horizontal / vertical padding for better button height control
        if self.fullscreen:
            horiz_pad = 12
            vert_pad = 6
        else:
            horiz_pad = max(6, min(16, window_h // 80))
            vert_pad  = max(3, min(8, window_h // 160))
        self.button_style.configure(
            'TButton',
            font=self.fonts['med'],
            padding=(horiz_pad, vert_pad)
        )

        # Map widgets to font keys and update them if they exist
        widget_font_map = {
            'hour_label': 'med', 'min_label': 'med', 'sec_label': 'med',
            'hour_spin': 'med',  'min_spin': 'med',  'sec_spin': 'med',
            'timer_label': 'big', 'clock_label': 'med'
        }
        for widget_name, font_key in widget_font_map.items():
            if hasattr(self, widget_name):
                getattr(self, widget_name).config(font=self.fonts[font_key])

    def on_resize(self, event):
        max_w, max_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        w = max(800, min(event.width, max_w))
        h = max(600, min(event.height, max_h))

        self.update_fonts_and_buttons()
        scale_factor = 0.55
        max_size = 900 if self.fullscreen else 600
        self.canvas_size = min(h * scale_factor, max_size)
        self.clock_canvas.config(width=self.canvas_size, height=self.canvas_size)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    # ---------- Clock ----------
    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%Y-%m-%d   %H-%M-%S"))
        self.root.after(1000, self.update_clock)

    def update_timer_label_from_spinbox(self):
        try:
            h, m, s = int(self.hour_var.get()), int(self.min_var.get()), int(self.sec_var.get())
        except ValueError:
            h, m, s = 0, 0, 0
        self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    def update_analog_clock(self):
        self.clock_canvas.delete("all")
        cx = cy = self.canvas_size // 2
        r = int(self.canvas_size * 0.40)

        # Face
        self.clock_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#f8f8f8", outline="#333", width=3)

        # Hour marks
        for i in range(12):
            angle = math.radians(i * 30)
            x1 = cx + (r - 10) * math.sin(angle)
            y1 = cy - (r - 10) * math.cos(angle)
            x2 = cx + r * math.sin(angle)
            y2 = cy - r * math.cos(angle)
            self.clock_canvas.create_line(x1, y1, x2, y2, fill="#333", width=3)

        # Numbers
        for num, angle in zip([12, 3, 6, 9], [0, 90, 180, 270]):
            rad = math.radians(angle)
            nx = cx + (r - 30) * math.sin(rad)
            ny = cy - (r - 30) * math.cos(rad)
            self.clock_canvas.create_text(nx, ny, text=str(num),
                                          font=("Segoe UI", max(10, int(r*0.18)), "bold"),
                                          fill="#222")

        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second + now.microsecond / 1_000_000

        # Hour hand — shortened for better proportions
        hour_angle = (hour + minute / 60) * 30
        hx = cx + (r - 50) * math.sin(math.radians(hour_angle))
        hy = cy - (r - 50) * math.cos(math.radians(hour_angle))
        self.clock_canvas.create_line(cx, cy, hx, hy, fill="#222", width=8,
                                      capstyle=tk.ROUND, smooth=True)

        # Minute hand
        min_angle = (minute + second / 60) * 6
        mx = cx + (r - 15) * math.sin(math.radians(min_angle))
        my = cy - (r - 15) * math.cos(math.radians(min_angle))
        self.clock_canvas.create_line(cx, cy, mx, my, fill="#444", width=4,
                                      capstyle=tk.ROUND, smooth=True)

        # Second hand
        sec_angle = second * 6
        sx = cx + (r - 5) * math.sin(math.radians(sec_angle))
        sy = cy - (r - 5) * math.cos(math.radians(sec_angle))
        self.clock_canvas.create_line(cx, cy, sx, sy, fill="#e33", width=2,
                                      capstyle=tk.ROUND, smooth=True)

        # Center hub
        self.clock_canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#222")

        self.root.after(1, self.update_analog_clock)

    # ---------- Timer Controls ----------
    def start_timer(self):
        if not self.running:
            self._toggle_spinboxes("disabled")
            try:
                if self.time_left == 0:
                    h, m, s = int(self.hour_var.get()), int(self.min_var.get()), int(self.sec_var.get())
                    self.time_left = h * 3600 + m * 60 + s
            except ValueError:
                self.timer_label.config(text="Invalid")
                self._toggle_spinboxes("normal")
                return

            if self.time_left <= 0:
                self.timer_label.config(text="00:00:00")
                messagebox.showinfo("Timer", "Time is up.")
                self._toggle_spinboxes("normal")
                return

            self.running = True
            threading.Thread(target=self._run_timer, daemon=True).start()

    def _run_timer(self):
        while self.time_left > 0 and self.running:
            h, rem = divmod(self.time_left, 3600)
            m, s = divmod(rem, 60)
            self.timer_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
            time.sleep(1)
            self.time_left -= 1
        if self.time_left == 0:
            self.timer_label.config(text="00:00:00")
            messagebox.showinfo("Timer", "Time is up.")
            self._toggle_spinboxes("normal")
        self.running = False

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.running = False
        self.hour_var.set("0")
        self.min_var.set("0")
        self.sec_var.set("0")
        self._toggle_spinboxes("normal")
        self.timer_label.config(text="00:00:00")
        self.time_left = 0

    def _toggle_spinboxes(self, state):
        self.hour_spin.config(state=state)
        self.min_spin.config(state=state)
        self.sec_spin.config(state=state)

    # ---------- Settings ----------
    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("500x300")
        settings_win.resizable(False, False)
        settings_win.grab_set()
        large_font = ("Segoe UI", 16)
        style = ttk.Style()
        style.configure("Settings.TButton", font=large_font, padding=(10, 6))
        style.configure("Settings.TCheckbutton", font=large_font)

        fullscreen_var = tk.BooleanVar(value=self.fullscreen)
        def toggle_fs():
            self.fullscreen = fullscreen_var.get()
            self.root.attributes("-fullscreen", self.fullscreen)

        ttk.Checkbutton(settings_win, text="Fullscreen", variable=fullscreen_var,
                        command=toggle_fs).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(settings_win, text="Window Size:").grid(row=1, column=0, sticky="e")
        all_sizes = ["800x600", "1024x768", "1280x800", "1600x900", "1920x1080", "2560x1440", "3840x2160"]
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        size_options = [s for s in all_sizes if int(s.split("x")[0]) <= sw and int(s.split("x")[1]) <= sh]
        size_var = tk.StringVar(value=f"{self.root.winfo_width()}x{self.root.winfo_height()}")
        size_combo = ttk.Combobox(settings_win, textvariable=size_var, values=size_options, state="readonly", justify="center")
        size_combo.grid(row=1, column=1, sticky="w")

        def apply_size():
            try:
                w, h = map(int, size_var.get().split("x"))
                if w > sw or h > sh:
                    messagebox.showwarning("Invalid Size", "Selected size exceeds your screen resolution.")
                    return
                self.root.minsize(w, h)
                self.root.geometry(f"{w}x{h}")
            except Exception:
                pass

        ttk.Button(settings_win, text="Apply Size", command=apply_size).grid(row=3, column=0, columnspan=2, pady=(15, 2))

        ttk.Label(settings_win, text="App Style:").grid(row=2, column=0, sticky="e")
        style_options = list(ttk.Style().theme_names())
        style_var = tk.StringVar(value=ttk.Style().theme_use())
        style_combo = ttk.Combobox(settings_win, textvariable=style_var, values=style_options, state="readonly", justify="center")
        style_combo.grid(row=2, column=1, sticky="w")

        def apply_style():
            try:
                ttk.Style().theme_use(style_var.get())
            except Exception:
                pass

        ttk.Button(settings_win, text="Apply Style", command=apply_style).grid(row=4, column=0, columnspan=2, pady=2)
        ttk.Button(settings_win, text="Close", command=settings_win.destroy).grid(row=5, column=0, columnspan=2, pady=(10, 10))

# DPI awareness first for crisp rendering
if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()