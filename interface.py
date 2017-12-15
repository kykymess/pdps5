# ==============================================================================
"""WIN : demo program for window manipulations"""
# ==============================================================================
__author__ = "Nator_Lulu"
__version__ = "1.1"  #
__date__ = "2017-11-17"
# ==============================================================================
from ezCLI import *
from ezTK import *
from random import choice


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
        Win.__init__(self, title='GRID', fold=cols)  # grid window
        # --------------------------------------------------------------------------

        for ligne in range(rows):
            for colonne in range(cols):
                if colonne == 0:
                    # win[ligne][colonne]=  "2"
                    images = tuple(Image(file="images/B%s.png" % color) for color in "2")
                    Button(self, height=64, width=64, image=images)
                elif colonne == cols - 1:
                    # win[ligne][colonne]=  "8"
                    images = tuple(Image(file="images/B%s.png" % color) for color in "8")
                    Button(self, height=64, width=64, image=images)
                else:
                    tuile_alea = choice(["3", "5", "6", "7", "9", "A", "B", "C", "D", "E"])
                    # win[ligne][colonne]=  tuile_alea
                    images = tuple(Image(file="images/R%s.png" % color) for color in tuile_alea)
                    Button(self, height=64, width=64, image=images)
        # --------------------------------------------------------------------------
        # for loop in range(rows*cols): Label(self, height=64, width=64, image = images)
        Button(self, text='Nouvelle grille', command=ConfigWin)
        # --------------------------------------------------------------------------
        win = self
        self.loop()


# ==============================================================================
if __name__ == "__main__":  # testcode for class 'DemoWin'
    win = None  # define a global variable to store current window
    ConfigWin()
# ==============================================================================
