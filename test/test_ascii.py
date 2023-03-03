import curses
from curses import ascii
win=curses.initscr()
curses.noecho()
curses.cbreak()
win.nodelay(False)
win.keypad(True)
try:
    while True:
        a=win.get_wch()
        if isinstance(a,str):
            if a==ascii.ctrl("s"):
                win.addstr(0,0,"ok")
            else:
                win.addstr(0,0,a)
except Exception as e:
    raise e
finally:
    curses.endwin()
