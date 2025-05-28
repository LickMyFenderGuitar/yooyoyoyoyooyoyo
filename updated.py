import ctypes
import cv2
import numpy as np
import torch
import pyautogui
import time
import threading
from dearpygui import dearpygui as dpg
import win32con, win32gui

# Windows API
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Screen
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# States
isAimbotChecked = False
isEspChecked = False
fov_radius = 150  # default
aimbot_thread = None
esp_thread = None

# YOLO
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)
yolo_model.conf = 0.4

def is_inside_circle(x, y, radius):
    dx = x - SCREEN_CENTER[0]
    dy = y - SCREEN_CENTER[1]
    return dx*dx + dy*dy <= radius*radius

# AIMBOT
def aimbot_loop():
    global isAimbotChecked
    while isAimbotChecked:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        results = yolo_model(frame)
        found = False

        for *box, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2)//2, (y1 + y2)//2

            if is_inside_circle(cx, cy, fov_radius):
                print(f"[aimbot] Target in FOV at {cx},{cy}")
                found = True
                break

        if not found:
            print("[aimbot] No targets in FOV")
        time.sleep(0.2)

# ESP + FOV circle
def esp_loop():
    global isEspChecked
    hdc = user32.GetDC(0)
    pen = gdi32.CreatePen(0, 2, 0x00FF00)  # Green for FOV
    gdi32.SelectObject(hdc, pen)

    while isEspChecked:
        left = SCREEN_CENTER[0] - fov_radius
        top = SCREEN_CENTER[1] - fov_radius
        right = SCREEN_CENTER[0] + fov_radius
        bottom = SCREEN_CENTER[1] + fov_radius
        gdi32.Ellipse(hdc, left, top, right, bottom)
        time.sleep(0.03)

    gdi32.DeleteObject(pen)
    user32.ReleaseDC(0, hdc)

# Toggles
def toggle_aimbot(sender, app_data, user_data):
    global isAimbotChecked, aimbot_thread
    isAimbotChecked = app_data
    if app_data:
        aimbot_thread = threading.Thread(target=aimbot_loop, daemon=True)
        aimbot_thread.start()

def toggle_esp(sender, app_data, user_data):
    global isEspChecked, esp_thread
    isEspChecked = app_data
    if app_data:
        esp_thread = threading.Thread(target=esp_loop, daemon=True)
        esp_thread.start()

def fov_slider_callback(sender, app_data, user_data):
    global fov_radius
    fov_radius = int(app_data)

# GUI
dpg.create_context()
with dpg.window(tag="overlay_window", no_title_bar=True, no_move=True, no_resize=True, no_collapse=True, no_background=True, pos=(0, 0), width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    dpg.add_checkbox(label="Aimbot", callback=toggle_aimbot)
    dpg.add_checkbox(label="ESP", callback=toggle_esp)
    dpg.add_slider_int(label="FOV Radius", default_value=fov_radius, min_value=50, max_value=500, callback=fov_slider_callback)
    with dpg.drawlist(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, tag="esp_drawlist"):
        dpg.draw_text((50, 50), "ESP ACTIVE", color=(255, 0, 0, 255), size=24)

dpg.create_viewport(title='', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, decorated=False, always_on_top=True, transparent=True)
dpg.setup_dearpygui()
dpg.show_viewport()

# Click-through window
hwnd = dpg.get_viewport_platform_handle()
style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

# Resize fix
def on_resize(sender):
    w = dpg.get_viewport_client_width()
    h = dpg.get_viewport_client_height()
    dpg.configure_item("overlay_window", width=w, height=h)
    dpg.configure_item("esp_drawlist", width=w, height=h)
dpg.set_viewport_resize_callback(on_resize)

dpg.start_dearpygui()
dpg.destroy_context()
