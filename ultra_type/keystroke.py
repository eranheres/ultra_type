import datetime


class KeyStroke:
    def __init__(self, character: str):
        self.character = character
        self.timestamp = datetime.datetime.now()
