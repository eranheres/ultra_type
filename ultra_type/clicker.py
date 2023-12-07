import pygame

class Clicker:

    def __init__(self):
        # Initialize Pygame Mixer
        pygame.mixer.init()
        # Load the click sound
        self._click_sound = pygame.mixer.Sound('ultra_type/data/click-2.wav')

    def click(self):
        try:
            # Play the click sound
            self._click_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

