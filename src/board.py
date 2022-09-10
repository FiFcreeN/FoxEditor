# Created by Ricardo Quintela

from pygame import Surface, Rect, draw
from guiElements.inputs import Button
from guiElements.inputs import DropDownMenu
from guiElements.inputs import TextInput

#default colors
white = (255,255,255)
black = (0,0,0)

class Board:
    def __init__(self, name: str, pos: tuple, color: tuple = black):
        """
        Constructor of the class Board\n
        A board is a rectangle with labels inside

        Args:
            name: the name of the board
            pos: the position of the board
            color: the color of the border of the board
        """
        #base attributes
        self.name = name
        self.pos = pos
        self.color = color

        #dimensions of the board (later are given by the biggest label)
        self.dimensions = [0,0]

        # a pygame object
        self.hitbox = Rect(pos, self.dimensions)
        self.center = self.hitbox.center
        self.left = self.hitbox.left
        self.right = self.hitbox.right
        self.bottom = self.hitbox.bottom
        self.top = self.hitbox.top

        #create the board surface
        self.board = Surface(self.dimensions)

        #stores all of the texts in this object
        self.nameText = Button(self.name, white, textColor=black, pos=(7,7), textSize=20, event=lambda: self.setDropDownMenuType(2))

        self.renameClass = Button("Rename", (60,60,60),
                                          event=lambda: self.resetTextInput(self.name,
                                                                            (self.nameText.pos[0] +
                                                                            self.pos[0],
                                                                            self.nameText.pos[1] +
                                                                            self.pos[1]),
                                                                            2))


        self.nameMenu = DropDownMenu([self.renameClass])

        self.attributeTexts = []
        self.methodTexts = []

        #parent of this board
        self.parent = None

        #store the position where the board is being clicked for moving
        self.clickPos = (0,0)
        #click checkpoint
        self.clicked = False

        #to work with the fast menus
        self.hoveredAttribute = 0
        self.hoveredMethod = 0


        #attribute and method menus
        self.removeAttributeButton = Button("Remove", (60,60,60),
                                            event=lambda: self.removeAttribute(self.hoveredAttribute))

        self.changeAttributeName = Button("Rename", (60,60,60),
                                          event=lambda: self.resetTextInput(self.attributeTexts[self.hoveredAttribute].text,
                                                                            (self.attributeTexts[self.hoveredAttribute].pos[0] +
                                                                            self.pos[0],
                                                                            self.attributeTexts[self.hoveredAttribute].pos[1] +
                                                                            self.pos[1]),
                                                                            0))

        self.attributeMenu = DropDownMenu([self.changeAttributeName, self.removeAttributeButton])

        self.removeMethodButton = Button("Remove", (60, 60, 60),
                                            event=lambda: self.removeMethod(self.hoveredMethod))

        self.changeMethodName = Button("Rename", (60, 60, 60),
                                          event=lambda: self.resetTextInput(self.methodTexts[self.hoveredMethod].text,
                                                                            (self.methodTexts[self.hoveredMethod].pos[0] +
                                                                             self.pos[0],
                                                                             self.methodTexts[self.hoveredMethod].pos[1] +
                                                                             self.pos[1]),
                                                                            1))


        self.methodMenu = DropDownMenu([self.changeMethodName, self.removeMethodButton])

        #the menu that is active in the board
        self.DropDownMenuType = 0


        #text input
        self.txtInput = TextInput((0,0), (60,60,60))
        self.textInputActive = False


        #abstracts
        self.nameIsAbstract = False


        self.draw(self.color)



    def setupDimensions(self):
        """
        Defines the dimensions of the board based on the largest items in it\n
        (iterates through labels and gets the biggest dimensions of text)
        """

        #base dimensions
        self.dimensions[0] = self.nameText.size[0] + 14
        self.dimensions[1] = self.nameText.size[1] + 14

        # try to resize dimensons if the attribute texts list is not empty
        if self.attributeTexts:
            self.dimensions[1] += 7

            # iterate through the attribute texts to get the largest item
            for button in self.attributeTexts:

                #increase X size
                if button.size[0] > self.dimensions[0] - 14:
                    self.dimensions[0] = button.size[0] + 14

                #Ysize
                self.dimensions[1] += button.size[1] + 7

        #try to resize dimensons if the method texts list is not empty
        if self.methodTexts:
            self.dimensions[1] += 7

            #iterate through the method texts to get the largest item
            for button in self.methodTexts:

                #increase X size
                if button.size[0] > self.dimensions[0] - 14:
                    self.dimensions[0] = button.size[0] + 14

                # Y size
                self.dimensions[1] += button.size[1] + 7


    def draw(self, color: tuple):
        """
        Draws in the board the name, attributes, methods and border

        Args:
            color: the color of the border of the board
        """

        #get the minimal possible dimensions for the box
        self.setupDimensions()


        #create a new board
        self.board = Surface(self.dimensions)

        #fill the board with base elements (background color and border)
        self.board.fill(white)
        draw.rect(self.board, color, (0,0, self.dimensions[0] - 1, self.dimensions[1] - 1), 2)

        #draw the name of the Board and a line under it
        self.nameText.blit(self.board)
        draw.line(self.board, color, (0, self.nameText.size[1] + 14), (self.dimensions[0], self.nameText.size[1] + 14), 2)

        # the Y position on where to draw the label
        labelY = self.nameText.size[1] + 21
        if self.attributeTexts:

            #iterates through the attributes list and draws every label on the board
            for button in self.attributeTexts:
                button.setPos((10, labelY))
                button.blit(self.board)
                labelY += button.size[1] + 7

            #draw a line only if there are methods
            if self.methodTexts:
                draw.line(self.board, color, (0, labelY), (self.dimensions[0], labelY), 2)


        labelY += 7 if self.attributeTexts else 0


        if self.methodTexts:
            #iterates through the methods list and draws every label on the board
            for button in self.methodTexts:
                button.setPos((10, labelY))
                button.blit(self.board)
                labelY += button.size[1] + 7

        #reset hitbox position
        self.hitbox = self.board.get_rect()
        self.hitbox.topleft = self.pos
        self.center = self.hitbox.center


    def setDropDownMenuType(self, index: int):
        """
        Set the fast menu type\n

        Args:
            index: the index o the fast menu that is supposed to be active
        """
        self.DropDownMenuType = index


    def getDropDownMenu(self):
        """
        Get the fast menu that is currently active
        Returns:
            the fast menu object that corresponds to a method or an attribute; None if there is no attribute and method
        """

        if len(self.attributeTexts) + len(self.methodTexts) == 0:
            return self.nameMenu

        if self.DropDownMenuType == 0:
            return self.attributeMenu
        elif self.DropDownMenuType == 1:
            return self.methodMenu
        else:
            return self.nameMenu


    def addAttribute(self, attribute: str):
        """
        Adds a new attribute to the board\n

        Args:
            attribute: the name of the attribute to add on the new label
        """
        #add the new text to the texts attribute
        self.attributeTexts.append(Button(attribute, white, textColor=black, index=len(self.attributeTexts),
                                          event=lambda: self.setDropDownMenuType(0)))

        #redraw the board
        self.draw(self.color)


    def removeAttribute(self, index: int):
        """
        Remove an attribute text from the attribute texts array\n

        Args:
            index: the index of the attribute to remove
        """

        self.attributeTexts.pop(index)

        #lower the index number
        for i in range(index, len(self.attributeTexts)):
            self.attributeTexts[i].index -= 1

        self.draw(self.color)


    def setAttributeName(self, name: str):
        """
        Set a new name to the attribute\n

        Args:
            name: the new name to the attribute
            mousePos: the position of the mouse pointer
        """
        self.textInputActive = False

        self.attributeTexts[self.hoveredAttribute].setText(name)
        self.draw(self.color)


    def addMethod(self, method: str):
        """
        Adds a new method to the board\n

        Args:
            method: the name of the method to add on the new label
        """
        #add the new text to the texts attribute
        self.methodTexts.append(Button(method, white, textColor=black, index=len(self.methodTexts),
                                       event=lambda: self.setDropDownMenuType(1)))

        #redraw the board
        self.draw(self.color)


    def removeMethod(self, index: int):
        """
        Remove an attribute text from the method texts array\n

        Args:
            index: the index of the method to remove
        """

        self.methodTexts.pop(index)

        # lower the index number
        for i in range(index, len(self.methodTexts)):
            self.methodTexts[i].index -= 1

        self.draw(self.color)


    def setMethodName(self, name: str):
        """
        Set a new name to the method\n

        Args:
            name: the new name to the method
            mousePos: the position of the mouse pointer
        """
        self.textInputActive = False

        self.methodTexts[self.hoveredMethod].setText(name)
        self.draw(self.color)


    def setName(self, name: str):
        """
        Change the name of the board
        Args:
            name: the new name of the board
        """

        self.name = name
        self.nameText.setText(name)
        self.draw(self.color)


    def addParent(self, board):
        """
        Adds a parent board\n

        Args:
            board: the board to be associated as a parent
        """
        self.parent = board

    def removeParent(self):
        """
        Resets the parent attribute
        """

        self.parent = None


    def drawAssociations(self, canvas: Surface):
        """
        Draws lines on screen from the associated board to this one\n

        Args:
            canvas: the surface where to draw the board
        """
        if self.parent != None:
            draw.line(canvas, self.color, self.center, self.parent.center, 2)



    def setColor(self, color: tuple):
        """
        Sets a new color to the border of the board
        Args:
            color: the new color of the border of the board
        """

        #sets the color attribute to the given color
        self.color = color

        #redraws the board
        self.draw(color)



    def move(self, pos: tuple) -> None:
        """
        Changes the pos attribute to the given position
        Args:
            pos: the position where the board will be moved
        """
        self.pos = pos
        self.hitbox.topleft = self.pos
        self.center = self.hitbox.center


    def isHovered(self, mousePos: tuple):
        """
        Whether the board is hovered by the mouse pointer or not\n

        Args:
            mousePos: the position of the mouse pointer

        Returns:
            True if its hovered, False otherwise
        """
        if self.hitbox.collidepoint(mousePos):
            return True

        return False


    def buttonIsHovered(self, mousePos: tuple):
        """
        Detects when a button is being hovered\n

        Args:
            mousePos: the position of the mouse

        Returns:
            True if its being hovered; False otherwise
        """

        mousePosition = (mousePos[0] - self.attributeMenu.pos[0], mousePos[1] - self.attributeMenu.pos[1])

        if len(self.attributeTexts) + len(self.methodTexts) == 0:
            return False

        for button in self.attributeMenu.options:
            if button.isHovered(mousePosition):
                return False


        for button in self.methodMenu.options:
            if button.isHovered(mousePosition):
                return False


        if self.textInputActive:
            return False

        mousePosition = (mousePos[0] - self.pos[0], mousePos[1] - self.pos[1])

        if self.nameText.isHovered(mousePosition):
            return True

        #iterate through the attribute text buttons and check if they are being hovered
        for button in self.attributeTexts:
            if button.isHovered(mousePosition):
                self.hoveredAttribute = button.index

                return True

        # iterate through the method text buttons and check if they are being hovered
        for button in self.methodTexts:
            if button.isHovered(mousePosition):
                self.hoveredMethod = button.index

                return True

        return False


    def isClicked(self, mousePos: tuple, mouseClick: bool, mouseUp: bool):
        """
        Whether the box is being clicked or not\n
        Clicking is considered click the box but not in a label\n

        Args:
            mousPos: the position of the mouse pointer
            mouseClick: the button of the mouse that is being clicked
            mouseUp: the button of the mouse that stopped being clicked

        Returns:
            the truth value of whether the box is being clicked
        """
        if mouseUp:
            self.clicked = False
            return False


        #set a checkpoint for continuous clicking
        if self.clicked:
            return True

        if self.isHovered(mousePos):
            #return False if any button is being hovered
            if self.buttonIsHovered(mousePos):
                return False

            if mouseClick:
                self.clicked = True
                return True

        return False


    def updateButtons(self):
        """
        Draw every button on the board
        """

        #draw the attribute buttons on the surface
        for button in self.attributeTexts:
            button.blit(self.board)

        # draw the method buttons on the surface
        for button in self.methodTexts:
            button.blit(self.board)



    def clickEvent(self, mousePos: tuple, click: bool):
        """
        Runs all the buttons and draws them on the surface\n

        Args:
            mousePos: the position of the canvas where to draw the menu
            click: the button of the mouse that was clicked
        """
        #itereate through the buttons array and check for hover and clicks in each one
        mousePosition = (mousePos[0] - self.pos[0], mousePos[1] - self.pos[1])

        self.nameText.clickEvent(mousePosition, click)

        for button in self.attributeTexts:
            button.clickEvent(mousePosition, click)

        for button in self.methodTexts:
            button.clickEvent(mousePosition, click)

        #redraw the buttons in the surface
        self.updateButtons()


    def resetTextInput(self, name: str, pos: tuple, index: int):
        """
        Resets the text input object to the given arguments\n

        Args:
            name: the new text to appear on the text input box
            pos: the new position of the text input
        """
        self.textInputActive = True
        self.txtInput.setPos(pos)
        self.txtInput.setText(name)
        self.txtInput.setName(name)
        self.txtInput.index = index


    def runTextInput(self, canvas: Surface, text: str, enter: bool, backspace: bool):
        """
        Updates the text input object\n

        Args:
            canvas: the surface to draw the text input
            text: the text to add to the text input
            backspace: whether backspace was pressed or  not
        """
        if self.textInputActive:
            # close text input
            if enter:
                self.textInputActive = False

                #get the text - if there is no text the name stays the same
                txt = self.txtInput.getText()
                if txt == None:
                    return

                # change attribute name
                if self.txtInput.index == 0:
                    self.setAttributeName(txt)

                # change method name
                elif self.txtInput.index == 1:
                    self.setMethodName(txt)

                # change the name of the class
                elif self.txtInput.index == 2:
                    self.setName(txt)

                return

            char = text
            if char:
                self.txtInput.addChar(char, backspace)
            self.txtInput.blit(canvas)


    def blit(self, canvas: Surface):
        """
        Draws the board on the given canvas\n

        Args:
            canvas: the Surface object on which to draw the board
        """
        canvas.blit(self.board, self.pos)
