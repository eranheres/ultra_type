import pygame
import random


class Clicker:

    def __init__(self, sound_enabled=True):
        self.sound_enabled = sound_enabled# Store state of the click sound
        # Initialize Pygame Mixer
        try:
            pygame.mixer.init()
            # Load the click sound
            self._click_sound = pygame.mixer.Sound('ultra_type/data/click-2.wav')
        except Exception as e:
            self._click_sound = None

    def click(self):
        if self._click_sound is None:
            return
        try:
            self._click_sound.set_volume(random.random() * 0.5 + 0.5)
            if self.sound_enabled: # Check if sound is enabled before playing
                self._click_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled # Toggle the state of the click sound

