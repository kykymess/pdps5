# ==============================================================================
"""WIN : demo program for window manipulations"""
# ==============================================================================
from kernel import PipesGrid

__author__ = "Nator_Lulu"
__version__ = "1.1"  #
__date__ = "2017-11-17"
# ==============================================================================
from ezTK import *


# ------------------------------------------------------------------------------
class ConfigWin(Win):
    """configuration window"""

    # ----------------------------------------------------------------------------
    def __init__(self):
        """create the config window and pack the widgets"""
        global win  # existing grid window is stored as a global variable
        if win:
            win.exit()  # exit previous grid window if it already exists
        Win.__init__(self, title='CONFIG_images', grow=False, fold=2, op=2)  # config window
        # --------------------------------------------------------------------------
        text = ('Number of rows :', 'Number of cols :')
        Label(self, text=text[0], grow=False, width=13, anchor='SW', relief='flat')
        Scale(self, scale=(5, 7), flow='W')
        Label(self, text=text[1], grow=False, width=13, anchor='SW', relief='flat')
        Scale(self, scale=(5, 10), flow='W')
        Button(self, text='Créer', command=GridWin)
        # --------------------------------------------------------------------------
        self.rowscale, self.colscale = self[0][1], self[1][1]
        win = self
        self.loop()


# ------------------------------------------------------------------------------
class GridWin(Win):
    """grid window"""

    # ----------------------------------------------------------------------------
    def __init__(self):
        """create the grid window and pack the widgets"""
        global win  # existing config window is stored as a global variable
        rows, cols = win.rowscale(), win.colscale()  # get grid size from scales
        if win: win.exit()  # exit previous config window if it already exists
        #  self.gasup = ConfigGasup(rows,cols) ############### envoi les données de cols et rows au code logique
        Win.__init__(self, title='GRID', click=self.on_click)  # grid window
        # --------------------------------------------------------------------------
        self.kernel = PipesGrid(rows, cols)
        self.board = Frame(self, fold=cols, border=1, relief='solid')
        images = tuple(Image(file='images/{}{}.png'.format(l, n)) for l in 'RGB' for n in '0123456789ABCDEF')
        for row in range(rows):
            for col in range(cols):
                button = Button(self.board, height=64, width=64, image=images)
                self.updateCell(button)
        # --------------------------------------------------------------------------
        # for loop in range(rows*cols): Label(self, height=64, width=64, image = images)
        Button(self, text='Nouvelle grille', command=ConfigWin)
        # --------------------------------------------------------------------------
        win = self
        self.loop()

    def updateCell(self, widget):
        n = self.kernel.getPipeNumber(*widget.index)
        widget(n)

    # ----------------------------------------------------------------------------

    def on_click(self, widget, code, mods):
        """callback function for all 'mouse click' events"""
        if widget.master != self.board or widget.index is None:
            return  # nothing to do if the widget is not a board cell
        changed = self.kernel.makeRotation(widget.index[0], widget.index[1], 'r')
        for r, c in changed:
            self.updateCell(self.board[r][c])


# ==============================================================================
if __name__ == "__main__":  # testcode for class 'DemoWin'
    win = None  # define a global variable to store current window
    ConfigWin()
# ==============================================================================
