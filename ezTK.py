# ==============================================================================
"""ezTK : a toolbox for easy development of Tk-based user-interface"""
# ==============================================================================
__author__ = "Christophe Schlick"
__version__ = "1.0"
__date__ = "2015-07-01"
# ==============================================================================
import tkinter as tk
# from tkinter.constants import *
from tkinter import messagebox as MessageDialog
from tkinter import filedialog as FileDialog
from tkinter import colorchooser as ColorDialog

# ------------------------------------------------------------------------------
Menu, Image = tk.Menu, tk.PhotoImage
IntVar, StringVar = tk.IntVar, tk.StringVar
# img = Image(width=48, height=48); img.blank() # fully transparent image
# ------------------------------------------------------------------------------
_side = {'S': 'top', 'N': 'bottom', 'E': 'left', 'W': 'right'}
_orient = {'N': 'vertical', 'S': 'vertical', 'E': 'horizontal', 'W': 'horizontal'}
_anchor = {'C': 'center', 'N': 'n', 'S': 's', 'E': 'e', 'W': 'w', 'NE': 'ne', 'NW': 'nw',
           'SE': 'se', 'SW': 'sw', 'EN': 'en', 'ES': 'es', 'WN': 'wn', 'WS': 'ws'}
_buts = {1: 'LMB', 2: 'MMB', 3: 'RMB'}
_mods = ((1, 'Shift'), (4, 'Control'), (131072, 'Alt'), (262144, 'Ext'),
         (2, 'Caps_Lock'), (8, 'Num_Lock'), (32, 'Scroll_Lock'),
         (256, 'LMB'), (512, 'MMB'), (1024, 'RMB'))


# ------------------------------------------------------------------------------
def _merge(current, **default):
    """merge 'current' dictionary with 'default' dictionary"""
    for key, val in default.items(): current.setdefault(key, val)


# ==============================================================================
class _ezTK(object):
    """interface class to add 'ezTK' features to standard 'tkinter' widgets"""

    # ----------------------------------------------------------------------------
    def __init__(self, state, keys, **props):
        """store multiple values for selected widget properties"""
        self._text, self._image, self._bg, self._fg = (), (), (), ()
        if 'text' in keys and isinstance(keys['text'], tuple):  # multiple texts
            self._text = keys['text'];
            del keys['text']
        if 'image' in keys and isinstance(keys['image'], tuple):  # multiple images
            self._image = keys['image'];
            del keys['image']
        if 'bg' in keys and isinstance(keys['bg'], tuple):  # multiple backgrounds
            self._bg = keys['bg'];
            del keys['bg']
        if 'fg' in keys and isinstance(keys['fg'], tuple):  # multiple foregrounds
            self._fg = keys['fg'];
            del keys['fg']
        self.states = max(map(len, (self._text, self._image, self._bg, self._fg)))
        props.update(keys)
        if 'anchor' in props: props['anchor'] = _anchor[props['anchor']]
        self.config(**props);
        self(state)  # config widget and set initial state

    # ----------------------------------------------------------------------------
    def __call__(self, state=None):
        """get or set current widget state"""
        if state is None:
            return self._state
        else:
            if self._text: self['text'] = self._text[state % len(self._text)]
            if self._image: self['image'] = self._image[state % len(self._image)]
            if self._bg: self['bg'] = self._bg[state % len(self._bg)]
            if self._fg: self['fg'] = self._fg[state % len(self._fg)]
            if 'activebackground' in self.keys(): self['activeback'] = self['bg']
            if 'activeforeground' in self.keys(): self['activefore'] = self['fg']
            self._state = state


# ==============================================================================
class Frame(tk.Frame):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, flow=None, fold=None, takefocus=False, anchor=None,
                 grow=True, font=None, bg=None, fg=None, op=None, ip=None, **keys):
        self.frame, self.index, self._index, self.widgets = self, None, 0, []
        self.fold, self.win = fold, master.win if master else self
        # when no 'flow' is provided, use reversed flow directions from 'master'
        self.flow = master.flow[::-1] if flow is None else flow
        self.font = master.font if font is None else font
        self.anchor = master.anchor if anchor is None else anchor
        self.bg = master.bg if bg is None else bg
        self.fg = master.fg if fg is None else fg
        self.op = master.op if op is None else op
        self.ip = master.ip if ip is None else ip
        props = dict(bg=self.bg, border=0, relief='solid');
        props.update(keys)
        pad = self.op if self.op == op or props['border'] else 0
        tk.Frame.__init__(self, master, padx=pad, pady=pad, **props)
        if isinstance(master, Frame):
            master.win.pack(self, grow)
        else:
            tk.Frame.pack(self, fill='both', expand=grow)

    # ----------------------------------------------------------------------------
    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widgets[index]
        else:
            return tk.Tk.__getitem__(self, index)
        # ----------------------------------------------------------------------------

    def __delitem__(self, index):
        if isinstance(index, int):
            self.widgets[index].destroy();
            del self.widgets[index];
            self._index -= 1
        else:
            tk.Tk.__delitem__(self, index)
        # ----------------------------------------------------------------------------

    @property
    def size(self):
        return (self._index // self.fold, self.fold) if self.fold else self._index

    # ==============================================================================


class Win(Frame):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master=None, title='', fold=None,
                 key=None, click=None, move=None, inout=None, **keys):
        props = dict(grow=True, fold=fold, flow='ES' if fold else 'SE',
                     border=0, relief='solid', anchor='C', op=0, ip=0, takefocus=True,
                     bg='white', fg='grey', font='Arial 12',
                     key=None, click=None, inout=None, move=None);
        props.update(keys)
        # create either a master window (Tk) or a slave window (Toplevel)
        master = tk.Toplevel(master.master) if master else tk.Tk()
        if master.master:
            x, y = master.master.winfo_x(), master.master.winfo_y()
            master.transient(master.master);
            master.geometry("+%s+%s" % (x + 24, y + 24))
        master.win = self;
        Frame.__init__(self, master, **props)
        master.title(title);
        master.resizable(props['grow'], props['grow'])
        self.exit, master.index = master.destroy, None
        if key: self.key = key; master.bind('<Any-Key>', self._key)
        if click: self.click = click; master.bind('<Any-Button>', self._click)
        if move:
            master.bind('<Motion>', lambda e: move(e.widget, (e.x, e.y), self._mods(e.state)))
        if inout:
            master.bind('<Enter>', lambda e: inout(e.widget, 1, self._mods(e.state)))
            master.bind('<Leave>', lambda e: inout(e.widget, 0, self._mods(e.state)))

    # ----------------------------------------------------------------------------
    @property
    def title(self):
        return self.master.title()

    # ----------------------------------------------------------------------------
    def _mods(self, state):
        """generate tuple of modifier keys for given event 'state'"""
        return tuple(name for mask, name in _mods if state & mask)
        # ----------------------------------------------------------------------------

    def _key(self, event):
        """generic key press event handler"""
        # widget = self.winfo_containing(*self.winfo_pointerxy())
        # if not widget: widget = event.widget
        if event.char and ord(event.char[0]) > 31: event.keysym = event.char[0]
        self.key(event.widget, event.keysym, self._mods(event.state))

    # ----------------------------------------------------------------------------
    def _click(self, event):
        """generic mouse click event handler"""
        if event.widget['takefocus'] == '0': self.focus_set()
        self.click(event.widget, _buts[event.num], self._mods(event.state))

    # ----------------------------------------------------------------------------
    def loop(self):
        self.update();
        self.master.minsize(self.winfo_width(), self.winfo_height())
        self.focus_force();
        self.mainloop()

    # ----------------------------------------------------------------------------
    def wait(self):
        self.update();
        self.master.minsize(self.winfo_width(), self.winfo_height())
        try:
            self.grab_set()
        except Exception:
            pass
        self.focus_force();
        self.wait_window()

    # ----------------------------------------------------------------------------
    def pack(self, widget, grow, fill='both'):
        ms = widget.master
        if ms.fold and ms._index % ms.fold == 0:  # create sub-frame at stack bottom
            ms.frame = tk.Frame(ms, bg=ms.bg);
            ms.frame.lower();
            ms.widgets.append([])
            ms.frame.index = None
            ms.frame.pack(in_=ms, side=_side[ms.flow[1]], fill='both', expand=True)
        (ms.widgets[-1] if ms.fold else ms.widgets).append(widget)
        widget.index = divmod(ms._index, ms.fold) if ms.fold else ms._index
        ms._index += 1  # op, ip = ms.op, ms.ip
        # if isinstance(widget, Frame): pass # special padding rules
        widget.pack(in_=ms.frame, fill=fill, expand=grow, side=_side[ms.flow[0]],
                    padx=ms.op, pady=ms.op, ipadx=ms.ip, ipady=ms.ip)


# ==============================================================================
class Brick(tk.Frame, _ezTK):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, state=0, **props):
        tk.Frame.__init__(self, master)
        _ezTK.__init__(self, state, props, bg=master.bg, border=2,
                       relief='solid', width=32, height=32, takefocus='0')
        master.win.pack(self, grow)


# ==============================================================================
class Label(tk.Label, _ezTK):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, state=0, **props):
        tk.Label.__init__(self, master)
        _ezTK.__init__(self, state, props, bg=master.bg, fg=master.fg, border=2,
                       relief='solid', anchor=master.anchor, font=master.font, takefocus='0')
        master.win.pack(self, grow)


# ==============================================================================
class Button(tk.Button, _ezTK):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, state=0, **props):
        tk.Button.__init__(self, master)
        _ezTK.__init__(self, state, props, bg=master.bg, fg=master.fg, border=2,
                       relief='raised', anchor=master.anchor, font=master.font, takefocus='0')
        master.win.pack(self, grow)


# ==============================================================================
class Checkbutton(tk.Checkbutton, _ezTK):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, state=0, **props):
        tk.Checkbutton.__init__(self, master)
        _ezTK.__init__(self, state, props, bg=master.bg, fg=master.fg, border=2,
                       anchor=master.anchor, font=master.font, takefocus='0')
        master.win.pack(self, grow)


# ==============================================================================
class Radiobutton(tk.Radiobutton):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, **props):
        _merge(props, bg=master.bg, fg=master.fg, anchor=master.anchor,
               font=master.font)
        tk.Radiobutton.__init__(self, master, **props);
        master.win.pack(self, grow)


# ==============================================================================
class Spinbox(tk.Spinbox):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, **props):
        _merge(props, bg=master.bg, fg=master.fg, anchor=master.anchor,
               font=master.font)
        tk.Spinbox.__init__(self, master, **props);
        master.win.pack(self, grow)


# ==============================================================================
class Canvas(tk.Canvas):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, **props):
        #    _merge(props, bg=master.bg, fg=master.fg, border=0); props['border'] -= 2
        _merge(props, bg=master.bg, border=0);
        props['border'] -= 2
        tk.Canvas.__init__(self, master, **props);
        master.win.pack(self, grow)


# ==============================================================================
class Scale(tk.Scale, _ezTK):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, scale=None, state=None,
                 flow='E', command=None, **props):
        start, stop, step = 0, 100, 1 if "resolution" not in props.keys() else props.pop("resolution")
        get = lambda seq, n, val: seq[n] if seq[n:n + 1] else val
        if isinstance(scale, (int, float)):
            stop = scale  # only 'stop' value
        elif isinstance(scale, (tuple, list)):  # get 'start, stop, step' values
            start, stop, step = get(scale, 0, start), get(scale, 1, stop), get(scale, 2, step)
        # if flow in 'WN': start,stop,step = stop,start,-step
        if not state: state = stop if flow in 'WN' else start
        props['orient'] = _orient[flow]
        if command: props['command'] = lambda n: command()
        self.command = command if command else (lambda: None)
        tk.Scale.__init__(self, master, bg=master.bg, fg=master.fg, from_=start,
                          to=stop, resolution=step, takefocus='0', font=master.font, **props)
        self.set(state);
        master.win.pack(self, grow)

    # ----------------------------------------------------------------------------
    def __call__(self, value=None):
        if value is None: return self.get()  # get current value
        if value == self.get(): return  # nothing to do when value hasn't changed
        self.set(value)  # set new value (associated command is called automatically)


# ==============================================================================
class Entry(tk.Entry):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, command=None, **props):
        _merge(props, bg=master.bg, fg=master.fg, font=master.font,
               takefocus='1', border=3)
        tk.Entry.__init__(self, master, **props)
        if command: self.bind('<Return>', lambda event, *args: command(*args))
        self.command = command if command else lambda: None
        master.win.pack(self, grow, 'x')

    # ----------------------------------------------------------------------------
    def __call__(self, value=None):
        if value is None: return self.get()  # get current value
        if value == self.get(): return  # nothing to do when value hasn't changed
        self.delete(0, 'end');
        self.insert(0, value);
        self.command()  # set new value
        # self.event_generate('<Return>', when='tail') # invoke callback for entry


# ==============================================================================
class Listbox(tk.Listbox):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, grow=True, scroll=True, **props):
        _merge(props, bg=master.bg, fg=master.fg, font=master.font, activestyle=None,
               selectmode='extended')
        if scroll:
            self.frame = tk.Frame(master, bg=props['bg'])
            master.win.pack(self.frame, grow)
            tk.Listbox.__init__(self, self.frame, **props)
            self.xscroll = tk.Scrollbar(self.frame, orient='horizontal',
                                        command=self.xview);
            self.xscroll.pack(side='bottom', fill='both')
            self.yscroll = tk.Scrollbar(self.frame, orient='vertical',
                                        command=self.yview);
            self.yscroll.pack(side='right', fill='both')
            self.config(xscrollcommand=self.xscroll.set)
            self.config(yscrollcommand=self.yscroll.set)
            self.pack(side='left', fill='both', expand=True)
        else:
            tk.Listbox.__init__(self, master, **props);
            master.win.pack(self, grow)
        self.clear()

    # ----------------------------------------------------------------------------
    def __call__(self, lines=None):
        if lines is None:  # get box content as a multi-line string
            return '\n'.join(self.items)
        else:  # set new box content as a multi-line string
            self.clear(lines.split('\n'))

    # ----------------------------------------------------------------------------
    def __len__(self):
        """x.__len__() <==> len(x)"""
        return len(self.items)

    # ----------------------------------------------------------------------------
    def __getitem__(self, index):
        """x.__getitem__(index) <==> x[index] where 'index' is an int or a slice"""
        return self.items[index]

    # ----------------------------------------------------------------------------
    def __setitem__(self, index, item):
        """x.__setitem__(index, items) <==> x[index] = item"""
        self.items[index] = item;
        self.clear(False)

    # ----------------------------------------------------------------------------
    def __delitem__(self, index):
        """x.__delitem__(index) <==> del x[index]"""
        del self.items[index];
        self.clear(False)

    # ----------------------------------------------------------------------------
    def append(self, lines):
        self.items.extend(lines.split('\n'));
        self.clear(False)

    # ----------------------------------------------------------------------------
    def clear(self, reset=True):
        if reset: self.items = []
        self.delete(0, 'end')
        for item in self.items: self.insert('end', item)
        self.see('end')


# ==============================================================================
class Command(Frame):
    """..."""

    # ----------------------------------------------------------------------------
    def __init__(self, master, process=None, prompt=None, **props):
        """"""
        if prompt is None: prompt = "Command"  # default 'prompt' string
        if process is None: process = lambda s: s  # default 'process' function
        self.prompt, self.process = prompt + ' : ', process
        _merge(props, bg=master.bg, fg=master.fg, font=master.font,
               width=80, height=20)
        self.width = props['width'];
        del props['width']
        self.height = props['height'];
        del props['height']
        Frame.__init__(self, master, side='top', **props)
        self.frame = Frame(self, grow=False)  # frame for Label, Entry and Button
        self.label = Label(self.frame, grow=False, text=self.prompt)
        self.entry = Entry(self.frame, command=self.enter)
        Button(self.frame, grow=False, text='ENTER', command=self.enter)
        Button(self.frame, grow=False, text='CLEAR', command=self.clear)
        self.box = Listbox(self, width=self.width, height=self.height)
        self.clear()

    # ----------------------------------------------------------------------------
    def enter(self):
        """"""
        try:
            out = self.process(self.entry())
        except Exception as e:
            out = "%r --> %s: %s" % (self.entry(), type(e).__name__, e)
        self.box.append(out)

    # ----------------------------------------------------------------------------
    def clear(self):
        """"""
        self.box.clear();
        self.entry('');
        self.entry.focus_set()


# ==============================================================================
if __name__ == '__main__':
    # from ezTKdemo import ezTKdemo
    # ezTKdemo()
    win = Win(title='ezTK', op=3)
    frame = Frame(win, fold=3, border=2)
    for loop in range(9): Brick(frame, width=64, height=64, bg='blue')
    Button(win, text='EXIT', width=20, height=2, command=win.exit)
    win.loop()
# ==============================================================================
