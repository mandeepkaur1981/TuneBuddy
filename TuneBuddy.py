from gpiozero import Button
import pygame
import os
import time
import random

# ---------------------- Button Mapping --------------------------

button_map = {
    4: "Pop",
    17: "Country",
    22: "Jazz",
    27: "Classic",
    5: "Saxophone",
    6: "Piano",
    13: "Guitar",
    26: "Drums",
    23: "Jolly",
    24: "Gloomy",
    25: "Suspenseful",
    12: "Calm",
    16: "Stop",
    20: "Generate"
}

# ---------------------- Row Definitions --------------------------

row_1 = ["Pop", "Jazz", "Country", "Classic"]
row_2 = ["Saxophone", "Piano", "Guitar", "Drums"]
row_3 = ["Gloomy", "Jolly", "Suspenseful", "Calm"]

combo = []  # User-selected combo

# ---------------------- Audio Setup -------------------------------

AUDIO_FOLDER = "/home/tt224/Tunebuddy/"  # Path to audio files
pygame.mixer.init()

# ---------------------- Setup Buttons -----------------------------
buttons = {pin: Button(pin, pull_up=True) for pin in button_map}

# ---------------------- Helper Functions --------------------------

def get_audio_filename(combo):
    """Generates the filename based on button combination."""
    filename = "_".join(sorted(combo)) + ".mp3"
    print(f"Filename to play: {filename}")
    return os.path.join(AUDIO_FOLDER, filename)

def ensure_full_combo():
    """Ensure combo has one selection from each row. Randomize missing."""
    global combo
    # Check if selection from each row exists, else add random
    if not any(item in row_1 for item in combo):
        choice = random.choice(row_1)
        combo.append(choice)
        print(f"Randomly added from row 1: {choice}")
    if not any(item in row_2 for item in combo):
        choice = random.choice(row_2)
        combo.append(choice)
        print(f"Randomly added from row 2: {choice}")
    if not any(item in row_3 for item in combo):
        choice = random.choice(row_3)
        combo.append(choice)
        print(f"Randomly added from row 3: {choice}")
    print(f"Final combo: {combo}")

def play_audio():
    """Plays audio based on selected button combination."""
    filepath = get_audio_filename(combo)
    if os.path.exists(filepath):
        print(f"Playing: {filepath}")
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
    else:
        print(f"File not found: {filepath}")

# ---------------------- Main Button Handler -----------------------
def handle_button_press(pin):
    """Handles individual button presses."""
    global combo

    # ------------------- STOP button always processed ----------------
    if pin == 16:  # 'Stop' button
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("Audio stopped.")
        else:
            print("No audio was playing.")
        combo.clear()  # Clear combo when stopping
        print("Combo cleared.")
        return  # Stop processing further

    # ------------------- Prevent other input if audio playing ----------
    if pygame.mixer.music.get_busy():
        print("Audio is still playing. Press 'Stop' to stop current playback.")
        return  # Ignore other inputs while audio is playing

    # ------------------- Handle Generate ---------------------------
    if pin == 20:  # 'Generate' button
        if len(combo) > 0:
            ensure_full_combo()
            play_audio()
            combo.clear()  # Clear combo after playing
        else:
            print("No buttons selected. Auto-generating combo.")
            ensure_full_combo()
            play_audio()
            combo.clear()  # Clear combo after playing
        return

    # ------------------- Handle Regular Buttons ----------------------

    selected = button_map[pin]

    # Row 1 selection
    if selected in row_1 and not any(btn in row_1 for btn in combo):
        combo.append(selected)
        print(f"Selected (Row 1): {selected}")
    # Row 2 selection
    elif selected in row_2 and not any(btn in row_2 for btn in combo):
        combo.append(selected)
        print(f"Selected (Row 2): {selected}")
    # Row 3 selection
    elif selected in row_3 and not any(btn in row_3 for btn in combo):
        combo.append(selected)
        print(f"Selected (Row 3): {selected}")
    else:
        print(f"Ignored duplicate or over-selection: {selected}")

# ---------------------- Listening Loop ----------------------------

print("Listening for button presses...")

try:
    while True:
        for pin in button_map.keys():
            if buttons[pin].is_pressed:
                handle_button_press(pin)
                time.sleep(0.3)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting...")
