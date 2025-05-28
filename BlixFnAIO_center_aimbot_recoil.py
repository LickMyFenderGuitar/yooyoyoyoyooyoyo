import tkinter as tk
from tkinter import messagebox
import threading
import time
import colorsys
import itertools
import webbrowser
import sys
import pyautogui
import cv2
import numpy as np
import torch
from pynput import keyboard
from pynput.mouse import Listener as MouseListener, Button as MouseButton

class BlixFnAIOApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blix Fn AIO")
        self.geometry("600x400")
        self.resizable(False, False)

        self.sidebar = tk.Frame(self, width=120, bg="#222", height=400)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = tk.Frame(self, bg="black", width=480, height=400)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.btn_home = tk.Button(self.sidebar, text="Home", fg="white", bg="#222", bd=0, command=self.show_home)
        self.btn_aio = tk.Button(self.sidebar, text="AIO", fg="white", bg="#222", bd=0, command=self.show_aio)
        self.btn_discord = tk.Button(self.sidebar, text="JOIN MY DISCORD", fg="white", bg="#222", bd=0, command=self.show_discord)
        self.btn_force_stop = tk.Button(self.sidebar, text="FORCE STOP", fg="white", bg="red", bd=0, command=self.confirm_force_stop)

        self.btn_home.pack(fill="x", pady=(20, 10))
        self.btn_aio.pack(fill="x", pady=10)
        self.btn_discord.pack(fill="x", pady=10)
        self.btn_force_stop.pack(fill="x", pady=(150, 0))

        self.animated_label = None
        self.inject_button = None

        self.fonts = itertools.cycle([
            ("Arial", 30, "bold"),
            ("Courier", 28, "bold"),
            ("Helvetica", 32, "bold"),
            ("Times", 30, "bold italic"),
            ("Comic Sans MS", 30, "bold")
        ])

        self.colors = itertools.cycle([
            "#FFFFFF", "#FFAAAA", "#AAFFAA", "#AAAFFF", "#FFFFAA", "#FFAACC"
        ])

        self.hue = 0
        self.model = None
        self.scanning = False
        self.recoil_active = False

        self.start_animation()
        self.start_rainbow_background()
        self.start_keyboard_listener()
        self.start_mouse_listener()
        self.show_home()

    def show_home(self):
        self.clear_main()
        self.animated_label = tk.Label(self.main_frame, text="1AM blix AIO", font=next(self.fonts),
                                       bg=self.main_frame["bg"], fg="white")
        self.animated_label.place(relx=0.5, rely=0.5, anchor="center")

    def show_aio(self):
        self.clear_main()
        self.animated_label = tk.Label(self.main_frame, text="1AM blix AIO", font=next(self.fonts),
                                       bg=self.main_frame["bg"], fg="white")
        self.animated_label.place(relx=0.5, rely=0.5, anchor="center")

        self.inject_button = tk.Button(self.main_frame, text="INJECT AIO", font=("Arial", 16),
                                       bg="#444", fg="white", command=self.run_injection_process)
        self.inject_button.place(relx=0.5, rely=0.65, anchor="center")

    def show_discord(self):
        self.clear_main()
        label = tk.Label(self.main_frame, text="www.discord.com", fg="white", bg=self.main_frame["bg"], font=("Arial", 20))
        label.place(relx=0.5, rely=0.4, anchor="center")

        join_button = tk.Button(self.main_frame, text="JOIN MY DISCORD", bg="#444", fg="white", font=("Arial", 14),
                                command=lambda: webbrowser.open("https://www.discord.com"))
        join_button.place(relx=0.5, rely=0.55, anchor="center")

    def confirm_force_stop(self):
        if messagebox.askyesno("Exit Confirmation", "Do you want to close the application?"):
            self.force_stop()

    def force_stop(self):
        self.scanning = False
        self.destroy()
        sys.exit(0)

    def run_injection_process(self):
        def inject_logic():
            try:
                self.inject_button.config(text="LOADING...")
                for _ in range(3):
                    for dots in range(1, 4):
                        self.inject_button.config(text="LOADING" + "." * dots)
                        time.sleep(1)

                if not self.model:
                    self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

                self.scanning = True
                threading.Thread(target=self.scan_loop, daemon=True).start()
                messagebox.showinfo("Success", "Successfully Injected")
                self.inject_button.config(text="INJECTED")

            except Exception as e:
                print(f"Error: {e}")
                def on_problem_response():
                    resp = messagebox.askquestion("Problem", "We ran into a problem.\nWould you like to rerun?")
                    if resp == "yes":
                        self.run_injection_process()
                messagebox.showerror("Error", "We ran into a problem.")
                on_problem_response()
                self.inject_button.config(text="INJECT AIO")

        threading.Thread(target=inject_logic, daemon=True).start()

    def scan_loop(self):
        while self.scanning:
            screen_w, screen_h = pyautogui.size()
            box_size = 200
            left = (screen_w - box_size) // 2
            top = (screen_h - box_size) // 2

            screenshot = pyautogui.screenshot(region=(left, top, box_size, box_size))
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            results = self.model(screenshot_bgr)
            detections = results.xyxy[0]

            for *box, conf, cls in detections:
                if int(cls) == 0:
                    x1, y1, x2, y2 = map(int, box)
                    rel_head_x = int((x1 + x2) / 2)
                    rel_head_y = int((y1 + y2) / 3)

                    abs_x = left + rel_head_x
                    abs_y = top + rel_head_y

                    pyautogui.moveTo(abs_x, abs_y, duration=0.2, tween=pyautogui.easeInOutQuad)
                    break

            time.sleep(0.1)

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f2:
                    if self.scanning:
                        self.scanning = False
                        print("Aimbot stopped via F2")
                        messagebox.showinfo("Info", "Aimbot Stopped. Press Inject again to rerun.")
            except:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()

    def start_mouse_listener(self):
        def on_click(x, y, button, pressed):
            if button == MouseButton.left:
                self.recoil_active = pressed
                if pressed:
                    threading.Thread(target=self.apply_recoil, daemon=True).start()

        listener = MouseListener(on_click=on_click)
        listener.daemon = True
        listener.start()

    def apply_recoil(self):
        while self.recoil_active:
            pyautogui.moveRel(0, 2)
            time.sleep(0.05)

    def start_animation(self):
        def animate():
            while True:
                font = next(self.fonts)
                color = next(self.colors)
                if self.animated_label:
                    self.animated_label.config(font=font, fg=color)
                time.sleep(1.0)
        threading.Thread(target=animate, daemon=True).start()

    def start_rainbow_background(self):
        def rainbow_loop():
            while True:
                rgb = colorsys.hsv_to_rgb(self.hue, 1, 1)
                hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
                self.main_frame.config(bg=hex_color)
                if self.animated_label:
                    self.animated_label.config(bg=hex_color)
                if self.inject_button:
                    self.inject_button.config(bg=hex_color)
                self.hue += 0.005
                if self.hue > 1:
                    self.hue = 0
                time.sleep(0.03)
        threading.Thread(target=rainbow_loop, daemon=True).start()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.animated_label = None
        self.inject_button = None

if __name__ == "__main__":
    try:
        app = BlixFnAIOApp()
        app.mainloop()
    except Exception as e:
        print(f"[Error] {e}")