import os
import random
import ctypes
import time
import sys


wallpaper_folder = r"C:\Users\indrajit\Pictures\wallpaper"
def set_wallpaper(wallpaper_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,wallpaper_path,3)

def hide_console_window():
    #hide the console window while running as a exetuble file
    if hasattr(sys, "frozen"):
        import win32gui
        import win32con
        win32gui.ShowWindow(win32gui.GetForegroundWindow(),win32con.SW_HIDE)

def load_used_wallpaper(file_path):
    used_wallpaper = {}
    if os.path.exists(file_path):
        with open(file_path,"r") as file:
            for line in file:
                wallpaper,last_usage = line.strip().split(",")
                used_wallpaper[wallpaper] = float(last_usage)
    return used_wallpaper


def save_used_wallpapers(used_wallpapers, file_path):
    with open(file_path, "w") as file:
        for wallpaper, last_usage in used_wallpapers.items():
            file.write(f"{wallpaper},{last_usage}\n")



def change_wallpaper(wallpaper_folder):
    

    file_path = "used_wallpaper.txt"
    used_wallpapers = load_used_wallpaper(file_path)

    image_files = [file for file in os.listdir(wallpaper_folder) if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))]
    available_wallpapers = [wallpaper for wallpaper in image_files if wallpaper not in used_wallpapers]

    if not available_wallpapers:
        # Reset used_wallpapers if all wallpapers have been used.
        used_wallpapers = {}
        available_wallpapers = image_files

    # Pick a random wallpaper from available wallpapers
    wallpaper = random.choice(available_wallpapers)
     # Set the wallpaper
    wallpaper_path = os.path.join(wallpaper_folder, wallpaper)
    set_wallpaper(wallpaper_path)

    # Update the used_wallpapers dictionary with the current wallpaper and its last usage date.
    used_wallpapers[wallpaper] = time.time()

    # Save the used_wallpapers dictionary to the file.
    save_used_wallpapers(used_wallpapers, file_path)

def main():
    hide_console_window()
    change_wallpaper(wallpaper_folder)
    
   

    while True:
        # Sleep for 24 hours (86400 seconds) before changing the wallpaper again
        time.sleep(86400)
        change_wallpaper(wallpaper_folder)

if __name__ == "__main__":
    main()