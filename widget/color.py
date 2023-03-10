import curses
curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_WHITE,0)
curses.init_pair(2,curses.COLOR_RED,0)
curses.init_color(100,500,500,500)
curses.init_pair(3,100,0)
white=curses.color_pair(1)
red=curses.color_pair(2)
gray=curses.color_pair(3)

