import curses
curses.initscr()
curses.start_color()
curses.init_pair(1,curses.COLOR_WHITE,0)
white=curses.color_pair(1)

curses.init_pair(2,curses.COLOR_RED,0)
red=curses.color_pair(2)

curses.init_pair(3,curses.COLOR_BLUE,0)
blue=curses.color_pair(3)

curses.init_color(100,500,500,500)
curses.init_pair(4,100,0)
gray=curses.color_pair(4)

curses.init_pair(5,curses.COLOR_BLACK,curses.COLOR_RED)
Red=curses.color_pair(5)


