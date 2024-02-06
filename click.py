import pygame
from pynput.keyboard import Listener

def play_click_sound():
    # Initialize Pygame Mixer
    pygame.mixer.init()
    # Load the click sound
    click_sound = pygame.mixer.Sound('ultra_type/data/click-2.wav')

    def on_press(key):
        try:
            # Play the click sound
            click_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    # Start listening to keyboard events
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    play_click_sound()
