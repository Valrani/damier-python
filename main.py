from tkinter import *
from math import ceil


def drawPawn(posX, posY, color):
    """
    Create a pawn on the canvas.
    This method is used by initPawns().
    :param posX: the number of the case (0 -> 9) on the X axis
    :param posY: the number of the case (0 -> 9) on the Y axis
    :param color: the color of the pawn
    :return: the ID of the pawn
    """
    x = (posX * 50) + 5
    y = (posY * 50) + 5
    x1 = (x + 50) - 10
    y1 = (y + 50) - 10
    return can.create_oval(x, y, x1, y1, fill=color)


def initPawns():
    """
    Init all the pawns for a new game.
    The ID of the pawns are stored in 2 lists, blackPawns and whitePawns.
    We also bind some callbacks to each pawn to enable the drag-n-drop mechanism.
    :return: nothing
    """
    global initPawnsButton, blackLeftCounterLabel, whiteLeftCounterLabel
    # place all black
    blackPawns.append(drawPawn(1, 0, "black"))
    blackPawns.append(drawPawn(3, 0, "black"))
    blackPawns.append(drawPawn(5, 0, "black"))
    blackPawns.append(drawPawn(7, 0, "black"))
    blackPawns.append(drawPawn(9, 0, "black"))
    blackPawns.append(drawPawn(0, 1, "black"))
    blackPawns.append(drawPawn(2, 1, "black"))
    blackPawns.append(drawPawn(4, 1, "black"))
    blackPawns.append(drawPawn(6, 1, "black"))
    blackPawns.append(drawPawn(8, 1, "black"))
    blackPawns.append(drawPawn(1, 2, "black"))
    blackPawns.append(drawPawn(3, 2, "black"))
    blackPawns.append(drawPawn(5, 2, "black"))
    blackPawns.append(drawPawn(7, 2, "black"))
    blackPawns.append(drawPawn(9, 2, "black"))
    blackPawns.append(drawPawn(0, 3, "black"))
    blackPawns.append(drawPawn(2, 3, "black"))
    blackPawns.append(drawPawn(4, 3, "black"))
    blackPawns.append(drawPawn(6, 3, "black"))
    blackPawns.append(drawPawn(8, 3, "black"))
    # place all whites
    whitePawns.append(drawPawn(1, 6, "white"))
    whitePawns.append(drawPawn(3, 6, "white"))
    whitePawns.append(drawPawn(5, 6, "white"))
    whitePawns.append(drawPawn(7, 6, "white"))
    whitePawns.append(drawPawn(9, 6, "white"))
    whitePawns.append(drawPawn(0, 7, "white"))
    whitePawns.append(drawPawn(2, 7, "white"))
    whitePawns.append(drawPawn(4, 7, "white"))
    whitePawns.append(drawPawn(6, 7, "white"))
    whitePawns.append(drawPawn(8, 7, "white"))
    whitePawns.append(drawPawn(1, 8, "white"))
    whitePawns.append(drawPawn(3, 8, "white"))
    whitePawns.append(drawPawn(5, 8, "white"))
    whitePawns.append(drawPawn(7, 8, "white"))
    whitePawns.append(drawPawn(9, 8, "white"))
    whitePawns.append(drawPawn(0, 9, "white"))
    whitePawns.append(drawPawn(2, 9, "white"))
    whitePawns.append(drawPawn(4, 9, "white"))
    whitePawns.append(drawPawn(6, 9, "white"))
    whitePawns.append(drawPawn(8, 9, "white"))
    # add a drag-n-drop detection for each pawn
    for pawnId in blackPawns + whitePawns:
        can.tag_bind(pawnId, '<Button-1>', onPawnClick)
        can.tag_bind(pawnId, '<B1-Motion>', onPawnMoving)
        can.tag_bind(pawnId, '<ButtonRelease-1>', onPawnStopMoving)
    # GUI setup
    initPawnsButton["state"] = DISABLED
    blackLeftCounterLabel["text"] = len(blackPawns)
    whiteLeftCounterLabel["text"] = len(whitePawns)


def initBoard():
    """
    Create the board on the canvas.
    :return: nothing
    """
    for lineNumber in range(0, 10):
        offset = 0 if lineNumber % 2 == 1 else 50
        for squareNumber in range(0, 5):
            x = (100 * squareNumber) + offset
            y = 50 * lineNumber
            x1 = x + 50
            y1 = y + 50
            can.create_rectangle(x, y, x1, y1, fill="#c7784c")


def onPawnClick(event):
    """
    Callback executed the first time the mouse interact with a pawn.
    Used to store the original position of the pawn, so when the pawn is moved then released,
    if the position is invalid, we can move it back to its original position.
    We temporarily store the original position inside the movingPawnOriginalCoordinates variable.
    :param event: used to retrieve the ID of the pawn we interact with
    :return: nothing
    """
    global movingPawnOriginalCoordinates
    pawnId = event.widget.find_withtag('current')[0]
    movingPawnOriginalCoordinates = can.coords(pawnId)


def onPawnMoving(event):
    """
    Callback executed during the pawn movement.
    Used to recompute its position as the mouse is moving.
    :param event: used to know the X and Y coordinates of the mouse
    :return: nothing
    """
    pawnId = event.widget.find_withtag('current')[0]
    can.coords(pawnId, event.x - 20, event.y - 20, event.x + 20, event.y + 20)


def onPawnStopMoving(event):
    """
    Callback executed when the mouse is released.
    Used to correctly place the pawn to the nearest case.
    Check if the case is valid (see the rules of the game).
    If not, replace the pawn to its original position.
    :param event: used to know the X and Y coordinates of the mouse
    :return: nothing
    """
    pawnId = event.widget.find_withtag('current')[0]
    nearestX = ceil(event.x / 50) * 50
    nearestY = ceil(event.y / 50) * 50
    # destination coordinates
    x = nearestX - 45
    y = nearestY - 45
    x1 = nearestX - 5
    y1 = nearestY - 5
    if isValidMove(pawnId, x, y, x1, y1):
        can.coords(pawnId, x, y, x1, y1)
    else:
        can.coords(pawnId, movingPawnOriginalCoordinates)


def isValidMove(pawnId, destX, destY, destX1, destY1):
    """
    Check if the pawn can be moved to the given coordinates.
    Rules :
    - the case cannot be occupied by another pawn;
    - the pawn can only move 1 case in diagonal, or 2 if he "jumps" above an enemy pawn;
    :return: True if the move is valid, False otherwise
    """
    sourceX = movingPawnOriginalCoordinates[0]
    sourceY = movingPawnOriginalCoordinates[1]
    sourceX1 = movingPawnOriginalCoordinates[2]
    sourceY1 = movingPawnOriginalCoordinates[3]
    # TODO remove after debug
    print("The pawn n°", pawnId, "wants to move from", sourceX, sourceY, sourceX1, sourceY1, "to", destX, destY, destX1,
          destY1)
    # check if the pawn is outside de bounds of the canvas
    if (destX < 0 or destX > 500) or (destY < 0 or destY > 500) or (destX1 < 0 or destX1 > 500) or (
            destY1 < 0 or destY1 > 500):
        return False
    # check if the move is not 1 case in diagonal
    if (destX != sourceX + 50 and destX != sourceX - 50) or (destY != sourceY + 50 and destY != sourceY - 50) or (
            destX1 != sourceX1 + 50 and destX1 != sourceX1 - 50) or (
            destY1 != sourceY1 + 50 and destY1 != sourceY1 - 50):
        # is so, we also check if the move is 2 cases in diagonal AND there is an enemy pawn in-between
        if destX == sourceX - 100 and destY == sourceY - 100 and destX1 == sourceX1 - 100 and destY1 == sourceY1 - 100:
            print("on a bougé de 2 cases en haut à gauche")
        if destX == sourceX + 100 and destY == sourceY - 100 and destX1 == sourceX1 + 100 and destY1 == sourceY1 - 100:
            print("on a bougé de 2 cases en haut à droite")
        if destX == sourceX - 100 and destY == sourceY + 100 and destX1 == sourceX1 - 100 and destY1 == sourceY1 + 100:
            print("on a bougé de 2 cases en bas à gauche")
        if destX == sourceX + 100 and destY == sourceY + 100 and destX1 == sourceX1 + 100 and destY1 == sourceY1 + 100:
            print("on a bougé de 2 cases en bas à droite")
        return False
    # the move is valid
    return True


# variables
blackPawns = []
whitePawns = []
movingPawnOriginalCoordinates = None

# GUI
fen = Tk()
fen.title("Le jeu de dames")
fen.resizable(False, False)
can = Canvas(fen, width=500, height=500, bg="#efcba0")
can.pack()
initPawnsButton = Button(fen, text="Nouvelle partie", command=initPawns)
initPawnsButton.pack(side=BOTTOM, padx=3, pady=3)
blackLeftLabel = Label(fen, text="Noirs restants :")
blackLeftLabel.pack()
blackLeftCounterLabel = Label(fen, text=0)
blackLeftCounterLabel.pack()
whiteLeftLabel = Label(fen, text="Blancs restants :")
whiteLeftLabel.pack()
whiteLeftCounterLabel = Label(fen, text=0)
whiteLeftCounterLabel.pack()

initBoard()
fen.mainloop()
