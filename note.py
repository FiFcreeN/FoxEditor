from pygame import Surface
from guiElements.inputs.button import Button
from guiElements.inputs.textInput import TextInput
from guiElements.inputs.fastMenu import FastMenu

class Note(Button):
    def __init__(self, text: str, pos: tuple, color: tuple = (255, 255, 255)):
        """
        Costructor of the class Note\n

        Args:
            text: the text to appear on the note
            pos: the position of the note
        """
        super().__init__(text, color, pos)
