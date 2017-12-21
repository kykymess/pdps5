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
        text = ('Number of rows :', 'Number of cols :', 'Time of games :')
        Label(self, text=text[0], grow=False, width=13, anchor='SW', relief='flat')
        Scale(self, length=350, scale=(5, 20), tickinterval=1, sliderlength=20, flow='W', state=10)
        Label(self, text=text[1], grow=False, width=13, anchor='SW', relief='flat')
        Scale(self, length=350, scale=(5, 20), tickinterval=1, sliderlength=20, flow='W', state=10)
        Label(self, text=text[2], grow=False, width=13, anchor='SW', relief='flat')
        Scale(self, length=650, scale=(30, 120), resolution=5, tickinterval=5, sliderlength=20, flow='W', state=60)
        Button(self, text='Créer', command=GridWin)
        # --------------------------------------------------------------------------
        self.rowscale, self.colscale, self.countscale = self[0][1], self[1][1], self[2][1]
        win = self
        self.loop()


# ------------------------------------------------------------------------------
class GridWin(Win):
    """grid window"""

    # ----------------------------------------------------------------------------
    def __init__(self):
        """create the grid window and pack the widgets"""
        global win  # existing config window is stored as a global variable
        rows, cols, count = win.rowscale(), win.colscale(), win.countscale()  # get grid size from scales
        if win: win.exit()  # exit previous config window if it already exists
        #  self.gasup = ConfigGasup(rows,cols) ############### envoi les données de cols et rows au code logique
        Win.__init__(self, title='GRID', click=self.on_click)  # grid window
        # --------------------------------------------------------------------------
        frame = Frame(self, fold=6)

        # Vars
        self.time_var = StringVar(value=str(count))
        self.score_var = StringVar(value=str(0))
        self.next_score_var = StringVar(value=(0))
        # --------------------------------------------------------------------------
        Label(frame, text='Temps restant = ', grow=True, anchor='SW', relief='flat', bg='white')
        Label(frame, textvar=self.time_var, grow=True, anchor='SW', relief='flat', bg='white', bd=2, fg='black')
        # --
        Label(frame, text='Score = ', grow=True, anchor='SW', relief='flat', bg='white')
        Label(frame, textvar=self.score_var, grow=True, anchor='SW', relief='flat', bg='white', bd=2,
              fg='black')
        # --
        Label(frame, text='A battre = ', grow=True, anchor='SW', relief='flat', bg='white')
        Label(frame, textvar=self.next_score_var, grow=True, anchor='SW', relief='flat', bg='white', bd=2, fg='black')
        # --------------------------------------------------------------------------
        self.kernel = PipesGrid(rows, cols)
        self.kernel.count = count
        self.board = Frame(self, fold=cols, border=1, relief='solid', bg='black')
        # --------------------------------------------------------------------------
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

        self.timeIsRunningOut()
        self.animating = False

        self.loop()

    def updateCell(self, widget):
        # print("{} {}".format(*widget.index))
        n = self.kernel.getPipeNumber(*widget.index)
        widget(n)

    # ----------------------------------------------------------------------------

    def on_click(self, widget, code, mods):
        """callback function for all 'mouse click' events"""
        if widget.master != self.board or widget.index is None or self.animating:
            return  # nothing to do if the widget is not a board cell
        changed = self.kernel.makeRotation(widget.index[0], widget.index[1], 'r')
        green = False
        for r, c in changed:
            self.updateCell(self.board[r][c])
            green = green or self.kernel.grid[r][c][0] == 'G'
        if green:
            iterator = self.kernel.collapse()
            self.animating = True
            self.show_collapse(iterator)

    def show_collapse(self, iterator):
        try :
            r, c, score = next(iterator)
            if score:
                self.score_var.set(str(int(self.score_var.get()) + 1))
            self.updateCell(self.board[r][c])
            self.after(10, lambda x=iterator : self.show_collapse(x))
        except StopIteration:
            for col in (0, self.kernel.cols - 1):
                for row in range(self.kernel.rows):
                    self.kernel.colorConnected(self.kernel.getAllConnected(row, col))
            for col in range(self.kernel.cols):
                for row in range(self.kernel.rows):
                    self.updateCell(self.board[row][col])
            self.score_var.set(str(int(self.score_var.get()) + 1))
            self.animating = False

    def timeIsRunningOut(self):
        """Ghosts keeping me alive ..."""
        self.kernel.times_up()
        self.time_var.set(str(self.kernel.count))
        self.after(1000, self.timeIsRunningOut)

class EndScoreWin(Win)

    def __init__(self):
        """create the config window and pack the widgets"""
        global win  # existing grid window is stored as a global variable
        if win:
            win.exit()  # exit previous grid window if it already exists
        Win.__init__(self, title='Sauvegarde_Score', grow=False, fold=2, op=2)  # config window
        # --------------------------------------------------------------------------
        texts = ('You played with a board of {} rows and {} cols and a time of {} seconds.')
        Label(self, text=texts, grow=False, width=13, anchor='SW', relief='flat')

        Button(self, text='Nouvelle grille', command=ConfigWin)
        # --------------------------------------------------------------------------
        self.rowscale, self.colscale, self.countscale = self[0][1], self[1][1], self[2][1]
        win = self
        self.loop()

# ==============================================================================
if __name__ == "__main__":  # testcode for class 'DemoWin'
    win = None  # define a global variable to store current window
    ConfigWin()
# ==============================================================================
