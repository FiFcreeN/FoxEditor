# Created by Ricardo Quintela

import pygame

from guiElements.window import Window
from boardCreator import BoardCreator


def main() -> None:
    """
    The main function of the code where all of the others are going to be called\n
    """

    print("Program started!")
    #initialize pygame engine
    pygame.init()

    #canvas variables
    size = (800, 600)
    FPS = 60

    #window object
    win = Window(size, FPS, "Fox Editor")


    #todo add a note editor
    #board creator object
    boardCreator = BoardCreator(win)

    #noteEditor = NoteEditor(win)


    #game loop
    boardCreator.mainloop()

    #quit the pygame engine
    pygame.quit()
    print("Program terminated!")

if __name__ == "__main__":
    main()
