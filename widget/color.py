import curses
curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_WHITE,0)
curses.init_pair(2,curses.COLOR_RED,1)
white=curses.color_pair(1)
red=curses.color_pair(2)
