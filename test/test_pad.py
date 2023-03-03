import curses

import time
import this

win=curses.initscr()
curses.start_color()
try:
    pad = curses.newpad(100, 100)
# These loops fill the pad with letters; addch() is
# explained in the next section
    pad.addstr(0,0,"hello world")
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    a=this.s.split("\n")
    for i in range(len(a)):
        pad.addstr(i,0,a[i])

# Displays a section of the pad in the middle of the screen.
# (0,0) : coordinate of upper-left corner of pad area to display.
# (5,5) : coordinate of upper-left corner of window area to be filled
#         with pad content.
# (20, 75) : coordinate of lower-right corner of window area to be
#          : filled with pad content.
    pad.refresh( 0,0,0,0, 30,30)
    time.sleep(1000)
except Exception as e:
    raise e
finally:
    curses.endwin()
