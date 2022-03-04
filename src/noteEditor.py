from guiElements.window.window import Window
from guiElements.window.windowEvents import WindowEvent
from guiElements.inputs.button import Button
from guiElements.inputs.fastMenu import FastMenu
from guiElements.inputs.textInput import TextInput
from guiElements.inputs.colorPicker import ColorPicker

class NoteEditor:
    def __init__(self, win: Window):
        """
        Constructor of the class NoteEditor
        """
        #window
        self.win = win

        #window state attributes
        self.running = True
        self.events = WindowEvent()


        #note editor attributes
        self.fastMenuActive = False
        self.fastMenuPos = (0,0)

        #default menu
        self.addNote = Button("Texto", (60,60,60), event=lambda: self.resetTextInput("Escrever Nota", self.defaultMenu.pos))

        self.defaultMenu = FastMenu([self.addNote])

        self.textInputActive = False

        self.txtInput = TextInput((0,0), (60,60,60), "Escreva uma nota")




    def openFastMenu(self, fastMenu: FastMenu, pos: tuple, condition: bool):
        """
        Shows the given fast menu in the given position if the given condition is true\n

        Args:
            fastMenu: the fast menu to show
            pos: the position where to draw the fast menu on the canvas
            condition: the condition to check
        """
        if condition:
            fastMenu.blit(self.win.canvas, pos)
            fastMenu.clickEvent(self.events.getEvent("mousePos"), self.events.getEvent("mouseButtons")[1])


    def resetTextInput(self, name: str, pos: tuple):
        """
        Resets the text input object to the given arguments\n

        Args:
            name: the new text to apear on the text input box
            pos: the new position of the text input
        """
        self.textInputActive = True
        self.txtInput.setPos(pos)
        self.txtInput.setName(name)


    def runTextInput(self):
        if self.textInputActive:
            char = self.events.getEvent("keyText")
            if len(char) > 0:
                self.txtInput.addChar(char, self.events.getEvent("keyBACKSPACE"))
            self.txtInput.blit(self.win.canvas)



    def mainloop(self):
        """
        Main loop of the Note Editor Screen
        """
        while self.running:
            #window state event checking
            self.win.tick()
            self.events.eventsCheck()
            self.running = self.events.getEvent("windowState")


            #window draws go here
            self.win.fill((255,255,255))

            #fast menus
            if self.events.getEvent("mouseButtons")[3]:
                self.fastMenuActive = True
                self.fastMenuPos = self.events.getEvent("mousePos")

            self.openFastMenu(self.defaultMenu, self.fastMenuPos, self.fastMenuActive)
            self.runTextInput()


            if self.events.getEvent("mouseButtons")[1]:
                self.fastMenuActive = False


            if self.events.getEvent("keyRETURN"):
                text = self.txtInput.getText()
                print(text)
                self.textInputActive = False


            self.win.update()