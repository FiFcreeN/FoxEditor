# new window class based on the guiElements window

from pygame import event, QUIT, VIDEORESIZE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, K_RETURN, K_BACKSPACE, MOUSEWHEEL
from guiElements.window import WindowEvent as winEvents


class WindowEvent(winEvents):
    def __init__(self):
        """
        Constructor of the class WindowEvent\n
        An object of this type can be used to analyze some events in a pygame window\n
        """
        self.events = {}

        self.resetEvents()


    def resetEvents(self):
        """
        Sets all the events to their base state
        """
        super().resetEvents()

        self.events["mouseWheelUp"] = False
        self.events["mouseWheelDown"] = False


    def eventsCheck(self):
        """
        Checks for each event there is on the display\n

        Returns:
            a tuple object with all the values of the checked events
        """

        # resets all the events and gets the mouse position on the window
        self.resetEvents()

        # iterates through all the pygame events
        for e in event.get():
            # quit the window
            if e.type == QUIT:
                print("QUIT EVENT")
                self.events["windowState"] = False

            #if the window gets resized
            if e.type == VIDEORESIZE:
                self.events["windowResize"] = True
                self.events["windowSize"] = (e.w, e.h)

            # check for mouse clicks
            if e.type == MOUSEBUTTONDOWN and e.button < len(self.events["mouseButtons"]):
                print(e.button, len(self.events["mouseButtons"]))
                self.events["mouseButtons"][e.button] = True


            # check for mouse clicks
            if e.type == MOUSEBUTTONUP and e.button < len(self.events["mouseButtons"]):
                self.events["mouseUp"][e.button] = True

            # check for mouse wheel rotation
            if e.type == MOUSEWHEEL:
                if e.y == 1:
                    self.events["mouseWheelUp"] = True
                else:
                    self.events["mouseWheelDown"] = True


            # check for key input (write text)
            if e.type == KEYDOWN:
                self.events["keyText"] = e.unicode

                # return (ENTER) key event
                if e.key == K_RETURN:
                    self.events["keyRETURN"] = True
                # backspace key event
                if e.key == K_BACKSPACE:
                    self.events["keyBACKSPACE"] = True
        
        