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
    The ID of the pawns are stored in a list (blackPawns and whitePawns).
    We also bind to each pawn some callbacks to enable the drag-n-drop mechanism.
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
    :param event: used to know the X and Y coordinates of the mouse
    :return: nothing
    """
    pawnId = event.widget.find_withtag('current')[0]
    nearestX = ceil(event.x / 50) * 50
    nearestY = ceil(event.y / 50) * 50
    can.coords(pawnId, nearestX - 45, nearestY - 45, nearestX - 5, nearestY - 5)


# variables
blackPawns = []
whitePawns = []

# GUI
fen = Tk()
fen.title("Le jeu de dames")
fen.resizable(False, False)
can = Canvas(fen, width=500, height=500, bg="#efcba0")
can.pack()
initPawnsButton = Button(fen, text="Réinitialiser le jeu", command=initPawns)
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
