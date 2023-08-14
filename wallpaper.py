import os
import random
import time
import sys
import subprocess

wallpaper_folder = "/home/indra/Pictures/wallpaper"

def set_wallpaper(wallpaper_path):
    # Use gsettings to set wallpaper for GNOME
    subprocess.run(["dconf", "write", "/org/gnome/desktop/background/picture-uri", f"'file://{wallpaper_path}'"])

def load_used_wallpaper(file_path):
    used_wallpaper = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                wallpaper, last_usage = line.strip().split(",")
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

    print("Image files found:", image_files)
    print("Available wallpapers:", available_wallpapers)

    if not available_wallpapers:
        # Reset used_wallpapers if all wallpapers have been used.
        used_wallpapers = {}
        available_wallpapers = image_files

    # Pick a random wallpaper from available wallpapers
    wallpaper = random.choice(available_wallpapers)

    # Get the absolute path of the wallpaper
    wallpaper_path = os.path.abspath(os.path.join(wallpaper_folder, wallpaper))

    # Set the wallpaper
    set_wallpaper(wallpaper_path)

    # Update the used_wallpapers dictionary with the current wallpaper and its last usage date.
    used_wallpapers[wallpaper] = time.time()

    print("Setting wallpaper:", wallpaper_path)

    # Save the used_wallpapers dictionary to the file.
    save_used_wallpapers(used_wallpapers, file_path)

def main():
    change_wallpaper(wallpaper_folder)

    while True:
        # Sleep for 24 hours (86400 seconds) before changing the wallpaper again
        time.sleep(86400)
        change_wallpaper(wallpaper_folder)

if __name__ == "__main__":
    main()
