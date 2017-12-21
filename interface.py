# ==============================================================================
"""WIN : demo program for window manipulations"""
# ==============================================================================
from kernel import PipesGrid

__author__ = "Nator_Lulu"
__version__ = "1.1"  #
__date__ = "2017-11-17"
# ==============================================================================
from ezTK import *
from score import ScoreSaver


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
        self.params = (rows, cols, count)
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
        try:
            r, c, score = next(iterator)
            if score:
                self.score_var.set(str(int(self.score_var.get()) + 100))
            self.updateCell(self.board[r][c])
            self.after(10, lambda x=iterator: self.show_collapse(x))
        except StopIteration:
            for col in (0, self.kernel.cols - 1):
                for row in range(self.kernel.rows):
                    self.kernel.colorConnected(self.kernel.getAllConnected(row, col))
            for col in range(self.kernel.cols):
                for row in range(self.kernel.rows):
                    self.updateCell(self.board[row][col])
            self.score_var.set(str(self.kernel.score))
            self.animating = False

    def timeIsRunningOut(self):
        """Ghosts keeping me alive ..."""
        self.kernel.times_up()
        self.time_var.set(str(self.kernel.count))
        if self.kernel.count > 0:
            self.after(1000, self.timeIsRunningOut)
        else:
            EndScoreWin(self.kernel.score, *self.params)


class EndScoreWin(Win):
    def __init__(self, score, rows, cols, count):
        """create the config window and pack the widgets"""
        self.score, self.rows, self.cols, self.count = score, rows, cols, count
        global win  # existing grid window is stored as a global variable
        if win: win.exit()  # exit previous grid window if it already exists
        Win.__init__(self, title='Sauvegarde_Score', grow=True, fold=1, op=2)  # config window
        # ---
        self.saver = ScoreSaver()
        # --------------------------------------------------------------------------
        texts = "You played with a board of {} rows and {} cols and a time of {} seconds.".format(rows, cols, count)
        Label(self, text=texts, grow=False, anchor='SW', relief='flat')
        # --------------------------------------------------------------------------
        Label(self, text="Your score : {0:.2f}".format(self.score / self.count), grow=True, fg='black')
        # --------------------------------------------------------------------------
        best_scores = self.saver.get(rows * cols)
        scores_frame = Frame(self, fold=len(best_scores), flow="SE", grow=True)
        for score, name in best_scores:
            Label(scores_frame, grow=True, text=name)
        for score, names in best_scores:
            Label(scores_frame, grow=True, text="{0:.2f}".format(score))
        # --------------------------------------------------------------------------
        save_score = Frame(self, grow=True, fold=1)
        # --
        self.entry = Entry(save_score, grow=True, text="Nameless")
        self.button = Button(save_score, grow=True, text="Press to save", command=self.save_score)
        # --------------------------------------------------------------------------
        Button(self, text='New grid', command=ConfigWin)
        # --------------------------------------------------------------------------
        win = self
        self.loop()

    def save_score(self):
        name = self.entry.get()
        battu = self.saver.write(self.rows * self.cols, name, self.score / self.count)
        if battu:
            self.button['text'] = "Congratulation ! Welcome to Top 10 !"



# ==============================================================================
if __name__ == "__main__":  # testcode for class 'DemoWin'
    win = None  # define a global variable to store current window
    ConfigWin()
# ==============================================================================
