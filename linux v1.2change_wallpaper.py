import os
import random
import subprocess
import time

# Replace '/home/indra/Pictures/wallpaper' with the path to your wallpaper folder
WALLPAPERS_FOLDER = '/home/indra/Pictures/wallpaper'
STATE_FILE_PATH = '/home/indra/Pictures/scripts/used_wallpaper.txt'

def set_wallpaper(image_path):
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + image_path])

def get_wallpapers():
    wallpaper_list = [file for file in os.listdir(WALLPAPERS_FOLDER) if file.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    return [os.path.join(WALLPAPERS_FOLDER, wallpaper) for wallpaper in wallpaper_list]

def shuffle_wallpapers(wallpapers):
    random.shuffle(wallpapers)

def save_wallpapers_state(wallpapers, index):
    with open(STATE_FILE_PATH, 'w') as state_file:
        state_file.write(','.join(wallpapers))
        state_file.write(f'\n{index}')

def load_wallpapers_state():
    if os.path.exists(STATE_FILE_PATH):
        with open(STATE_FILE_PATH, 'r') as state_file:
            lines = state_file.readlines()
            if len(lines) == 2:
                wallpaper_list = lines[0].strip().split(',')
                index = int(lines[1])
                return wallpaper_list, index
    return None, None

def reset_wallpapers_state():
    if os.path.exists(STATE_FILE_PATH):
        os.remove(STATE_FILE_PATH)

if __name__ == '__main__':
    wallpapers, current_index = load_wallpapers_state()

    if wallpapers is None or current_index is None or current_index >= len(wallpapers):
        wallpapers = get_wallpapers()
        current_index = 0
        shuffle_wallpapers(wallpapers)

    while True:
        wallpaper = wallpapers[current_index]
        set_wallpaper(wallpaper)
        current_index = (current_index + 1) % len(wallpapers)
        save_wallpapers_state(wallpapers, current_index)
        # Wait for 24 hours (86400 seconds) before changing the wallpaper again
        time.sleep(86400)

        # If the current_index is 0, it means all wallpapers have been shown in the current loop
        # In that case, reset the state to reshuffle the wallpapers for the next loop
        if current_index == 0:
            reset_wallpapers_state()
