import pygame
import random

class Clicker:

    def __init__(self):
        # Initialize Pygame Mixer
        pygame.mixer.init()
        # Load the click sound
        self._click_sound = pygame.mixer.Sound('ultra_type/data/click-2.wav')

    def click(self):
        try:
            self._click_sound.set_volume(random.random() * 0.5 + 0.5)
            self._click_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

