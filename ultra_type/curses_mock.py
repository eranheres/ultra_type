import getch
import sys

class CursesMock:
    def __init__(self):
        pass

    def endwin(self):
        pass

    def move(self, y: int, x: int):
        pass

    def addstr(self, text: str):
        print(text, end='')
        pass

    def getch(self):
        c = sys.stdin.read(1)
        return c

    def keypad(self, boolean: bool):
        pass

    def getstr(self):
        return getch.getch()

    def clear(self):
        pass

    def refresh(self):
        pass