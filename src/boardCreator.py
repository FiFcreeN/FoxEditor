# Created by Ricardo Quintela

from pygame import Surface
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesnocancel, showwarning
from json import dumps, loads
from guiElements.window import Window
from guiElements.window import WindowEvent
from board import Board
from guiElements.inputs import Button
from guiElements.inputs import DropDownMenu
from guiElements.inputs import TextInput
from guiElements.inputs import ColorPicker

#colors
white = (255, 255, 255)
black = (0,0,0)


#TODO - implementar mudança de nome em Classes


class BoardCreator:
    def __init__(self, win: Window):
        """
        Constructor of the BoardCreator class\n

        Instances of this class can be used to control elements on screen\n
        """

        # state of the program
        self.running = True

        #the window object
        self.win = win


        #create a WindowEvent analyzer
        self.events = WindowEvent()



        ######################
        #   WINDOW OBJECTS
        ######################

        self.txtInput = TextInput((100, 100), (100, 100, 100))

        # FAST MENU BUTTONS
        #default
        self.addClass = Button("New Class", (60, 60, 60), event=lambda: self.resetTextInput("NewClass", self.defaultMenu.pos))
        self.loadUML = Button("Load Board", (60,60,60), event=self.loadFileButton)
        self.saveAsUML = Button("Save As", (60,60,60), event=lambda: self.saveFile(True))
        self.saveUML = Button("Save", (60,60,60), event=self.saveFile, active=False, textColor=(120,120,120))

        #board
        self.addAttribute = Button("New Attribute", (60,60,60), event=lambda: self.resetTextInput("newAttribute", self.boardMenu.pos, 0))
        self.addMethod = Button("New Method", (60,60,60), event=lambda: self.resetTextInput("newMethod()", self.boardMenu.pos, 1))
        self.addParent = Button("Inherit From", (60,60,60), event=self.activateBoardMenu, active=False, textColor=(120,120,120))
        self.pickColor = Button("Pick Color", (60,60,60), event=self.activateColorPicker)
        self.deleteClass = Button("Delete", (60,60,60), event=self.deleteBoard)

        # FAST MENU BUTTONS ARRAY
        defaultMenu = [self.addClass, self.loadUML, self.saveAsUML, self.saveUML]
        boardMenu = [self.addAttribute, self.addMethod, self.addParent, self.pickColor, self.deleteClass]

        # FAST MENU OBJECT
        self.defaultMenu = DropDownMenu(defaultMenu)

        self.boardMenu = DropDownMenu(boardMenu)


        self.fastMenus = [self.defaultMenu, self.boardMenu, None, None]

        # list which will contain all of the boards
        self.boards = []

        # fast menu variables
        self.fastMenuOpen = False
        self.fastMenuCoords = (0, 0)

        #if the mouse is hovering a board
        self.fastMenuType = 0


        #COLOR PICKER
        self.colorPicker = ColorPicker((60,60,60))
        self.colorPickerActive = False


        #text input variables
        self.isTextInput = False

        self.fileName = None





    #BUTTON METHODS
    def resetTextInput(self, name: str, pos: tuple, index: int= -1):
        """
        Sets the text input name and position and activates its control attribute\n

        Args:
            name: the new name of the TextInput object
            pos: the new position of the TextInput object

        Returns:

        """
        if index >= 0:
            self.txtInput.setIndex(index)
        self.txtInput.setPos(pos)
        self.txtInput.setName(name)
        self.isTextInput = True



    def loadFileButton(self):
        """
        Actions of the loadFile button
        """
        self.loadFile()
        self.fastMenuOpen = False


    def activateBoardMenu(self):
        """
        Activates the board menu by defining the necessary attributes to the correct values
        """
        self.fastMenuType = 2
        self.fastMenus[2] = self.createBoardMenu()


    def activateColorPicker(self):
        """
        Activates the color picker by defining the necessary attributes to the correct values
        """
        self.colorPickerActive = True
        self.colorPicker.setPos((self.win.size[0] / 2 - self.colorPicker.size[0] / 2, self.win.size[1] / 2 - self.colorPicker.size[1] / 2))


    def buttonAddParent(self, option: int):
        print(self.boards[option].name, option)
        self.boards[-1].addParent(self.boards[option])
        self.fastMenuOpen = False


    def jsonErrorCompat(self, action: str):
        """
        Shows an error message saying that the read file is incompatible
        """

        # Console message
        print("ERROR: JSON format is incompatible with the board loader.")

        # window message
        root = Tk()
        root.withdraw()
        showwarning("ERRO", "Unable to %s the Board." % (action))


    def setTitle(self):
        """
        Sets the title of the window
        """
        filename = self.fileName.replace("\\", "/")
        try:
            filename = filename[-filename[::-1].index("/"):]
        except:
            filename = self.fileName

        self.win.setTitle("Fox Editor - " + filename)


    def loadFile(self):
        """
        Loads the contents of a jason file into boards
        """
        root = Tk()
        root.withdraw()
        self.fileName = askopenfilename(title="Load Board", defaultextension=".json", filetypes=[("JSON files", ".json"), ("All files", ".*")])


        #safety in case user cancels it or exists it
        if self.fileName == None:
            return

        if not self.fileName:
            self.fileName = None
            return


        try:
            #read the file in the path
            with open(self.fileName, "r") as f:
                text = f.read()

            #store in a dict
            boards = loads(text)

        #show a warning in case the user fed an incompatible file
        except:
            self.jsonErrorCompat("load")

            return

        checkList = ["pos", "color", "attributes", "methods", "parent"]

        for content in boards.values():
            for val in content.keys():
                if val in checkList:
                    continue
                else:
                    self.jsonErrorCompat("load")
                    return

        self.setTitle()

        self.boards = []

        # create all of the boards
        for name, contents in boards.items():
            b = Board(name, contents["pos"], contents["color"])

            #add the board attributes
            for attribute in contents["attributes"]:
                b.addAttribute(attribute)

            #add the board methods
            for method in contents["methods"]:
                b.addMethod(method)

            self.boards.append(b)

        # add parents to the boards
        index = 0
        # iterate through the values of the boards dict
        for contents in boards.values():
            # if there is no parent define parent as None and continue
            if contents["parent"] == None:
                self.boards[index].addParent(None)
                index += 1
                continue

            # iterate through the boards list
            for board in self.boards:

                # if the board name is equal to the parent name then it must be the same
                # thus, the parent of the boards[index] is added
                if board.name == contents["parent"]:
                    self.boards[index].addParent(board)
            index += 1

            # activate the save option
            self.saveUML.activate((255, 255, 255))


    def saveFile(self, saveAs: bool = False):
        """
        Sets all the attributes to save a file
        Args:
            pos: the position of the mouse pointer
        """
        if self.fileName == None or saveAs:
            #filedialog
            root = Tk()
            root.withdraw()
            self.fileName = asksaveasfilename(title="Save Board" ,defaultextension=".json", filetypes=[("JSON file", ".json"), ("All files", ".*")])

            #safety in case the user closes the dialog
            if self.fileName == None:
                return

            if not self.fileName:
                self.fileName = None
                return

        self.setTitle()

        #constructs the json text to save
        boards = {}
        for board in self.boards:

            boardParent = None if board.parent == None else board.parent.name
            attributeTexts = [button.text for button in board.attributeTexts]
            methodTexts = [button.text for button in board.methodTexts]

            boards[board.name] = {"pos": board.pos,
                                  "color": board.color,
                                  "attributes": attributeTexts,
                                  "methods": methodTexts,
                                  "parent": boardParent,
                                  }

        #dumps the created dictionary in a jason format string
        text = dumps(boards, indent=4)

        try:
            #save json string in a file
            with open(self.fileName, "w") as f:
                f.write(text)

        except:
            print("ERROR: File does not exist!")
            return

        #activate the save option
        self.saveUML.activate((255,255,255))



    def addTextInput(self, txtInput: TextInput, char: str, backspace: bool, ret: bool) -> str:
        """
        Add a character to the text input\n

        Args:
            txtInput: the text input box object
            char: the character or string to add to the box
            backspace: whether backspace key is pressed or not
            ret: whether return key is pressed or not

        Returns:
            the text in the text box; None if return is not pressed
        """
        if not ret:
            txtInput.addChar(char, backspace)
            return None

        return txtInput.getText()


    def openFastMenu(self, canvas: Surface, openCondition: bool, click: bool, mouseCoords: tuple, blitCoords: tuple, menu: DropDownMenu):
        """
        Opens a fast menu and keeps it open when openCondition is True, closes it when openCondition is False\n

        Args:
            win: the Window object with the canvas to blit the menu
            openCondition: the condition to keep the menu opened
            click: the mouse button which click is going to interact with the buttons
            mouseCoords: the coordinates of the mouse pointer
            blitCoords: the coordinates to blit the menu on the canvas
            menu: the menu to open
            *events: the event arguments of the menu buttons
        """
        if openCondition:            
            menu.clickEvent(mouseCoords, click)
            menu.pos = blitCoords
            menu.blit(canvas)


    def createBoardMenu(self) -> DropDownMenu:
        """
        Creates a FastMenu object with all the available boards

        Returns:
            a FastMenu instance with all of the available boards
        """
        boards = [Button(board.name, (60,60,60), index=i) for i, board in enumerate(self.boards[:-1])]

        menu = DropDownMenu(boards)

        return menu


    def deleteBoard(self):
        """
        Delete the last board of the list
        """

        #delete all parents of that board in all boards
        for board in self.boards[:-1]:
            if self.boards[-1] == board.parent:
                board.removeParent()

        #delete board from the list of boards
        self.boards.pop(-1)


    def mainloop(self):
        """
        The mainloop is where the window events are going to be ran through and checked,
        functions related to window update are going to be called, etc.\n
        """

        #mainloop
        while self.running:
            #tick
            self.win.tick()

            #check for events
            self.events.eventsCheck()

            #state of the program
            if not self.events.getEvent("windowState"):

                if not self.boards:
                    self.running = False
                    break

                root = Tk()
                root.withdraw()
                exitEvent = askyesnocancel("Unsaved Work", "Do you want to save this board?", icon="warning")
                
                if exitEvent != None:
                    if exitEvent:
                        self.saveFile()
                    self.running = False

            #resize the window
            if self.events.getEvent("windowResize"):
                self.win.resize(self.events.getEvent("windowSize"))


            #paint the canvas with the color white
            self.win.fill(white)


            ###############################
            #       DRAW THE BOARDS
            ###############################
            if self.boards:
                #potition of the board where it was clicked
                if self.events.getEvent("mouseButtons")[1]:
                    self.boards[-1].clickPos = (self.events.getEvent("mousePos")[0] - self.boards[-1].pos[0],
                                                self.events.getEvent("mousePos")[1] - self.boards[-1].pos[1])

                #move the board to the mouse position - position where it was clicked
                if self.boards[-1].isClicked(self.events.getEvent("mousePos"), self.events.getEvent("mouseButtons")[1],
                                                               self.events.getEvent("mouseUp")[1]):
                    boxPos = (self.events.getEvent("mousePos")[0] - self.boards[-1].clickPos[0],
                              self.events.getEvent("mousePos")[1] - self.boards[-1].clickPos[1])

                    self.boards[-1].move(boxPos)


                #draw board parent lines
                for board in self.boards:
                    board.drawAssociations(self.win.canvas)

                #draw the boards on screen
                for board in self.boards:
                    board.clickEvent(self.events.getEvent("mousePos"), self.events.getEvent("mouseButtons")[3])
                    board.blit(self.win.canvas)
                    board.runTextInput(self.win.canvas, self.events.getEvent("keyText"),
                                       self.events.getEvent("keyRETURN"), self.events.getEvent("keyBACKSPACE"))


            ###############################################
            #               FAST MENUS
            ###############################################

            #in case there are no sufficient boards to inherit
            if len(self.boards) > 1:
                self.addParent.activate((255,255,255))
            else:
                if self.fastMenuType == 2:
                    self.fastMenuType = 1
                self.addParent.deactivate((120,120,120))

            #check if the mouse is hovering a board
            #only checks for it if a fastmenu is not already opened
            if not (self.fastMenuOpen or self.isTextInput) and not self.events.getEvent("mouseClicking")[0] and not self.colorPickerActive:
                self.fastMenuType = 0

                #set the selected board as the hovered board (iterates through the back of the list)
                for i,board in enumerate(self.boards[::-1]):
                    i = len(self.boards) - 1 - i

                    #change the order of the selected board on the list to the last so that it appears first on screen
                    if board.isHovered(self.events.getEvent("mousePos")):
                        self.boards[i], self.boards[-1] = self.boards[-1], self.boards[i]

                        self.fastMenuType = 1

                        if board.buttonIsHovered(self.events.getEvent("mousePos")):
                            self.fastMenuType = 3

                        break

            #open the fast menu using the right click
            if self.events.getEvent("mouseButtons")[3]:
                self.fastMenuOpen = True
                self.fastMenuCoords = self.events.getEvent("mousePos")

            #draw color picker
            if self.colorPickerActive:
                self.colorPicker.blit(self.win.canvas, self.events.getEvent("mousePos"), self.events.getEvent("mouseButtons")[1])

                #select the color of the color picker and draw the board with it
                if self.colorPicker.select.getClick():
                    self.boards[-1].setColor(self.colorPicker.getColor())
                    self.colorPickerActive = False


            #open fast menu 3 (heritage menu)
            if self.fastMenuType == 2:
                for button in self.fastMenus[2].options:
                    if button.getClick():
                        self.boards[-1].addParent(self.boards[button.index])
                        self.fastMenuOpen = False


            #open fast menu 4 (in Board menu)
            if self.fastMenuType == 3:
                self.fastMenus[3] = self.boards[-1].getDropDownMenu()


            #run the fast menu HERE
            self.openFastMenu(self.win.canvas, self.fastMenuOpen, self.events.getEvent("mouseButtons")[1], self.events.getEvent("mousePos"), self.fastMenuCoords, self.fastMenus[self.fastMenuType])


            #get the text from the text input
            text = None
            #if the text input is on
            if self.isTextInput:
                # text input boxes
                text = self.addTextInput(self.txtInput, self.events.getEvent("keyText"),
                                         self.events.getEvent("keyBACKSPACE"), self.events.getEvent("keyRETURN"))
                #draw the text input
                self.txtInput.blit(self.win.canvas)


            #########################################
            #           CLOSE INPUTS
            #########################################

            #close the fast menu and text inputs
            if self.events.getEvent("mouseButtons")[1]:
                if self.fastMenuType != 2:
                    self.fastMenuOpen = False
                self.txtInput.reset()

            #close text input
            if self.events.getEvent("keyRETURN"):
                self.isTextInput = False
                self.txtInput.reset()
                if text != None:

                    #actions of the fastmenus
                    if self.fastMenuType == 0:
                        self.boards.append(Board(text, self.txtInput.pos))

                    elif self.fastMenuType == 1 and self.txtInput.index == 0:
                        self.boards[-1].addAttribute(text)

                    elif self.fastMenuType == 1 and self.txtInput.index == 1:
                        self.boards[-1].addMethod(text)


            #update window
            self.win.update()
