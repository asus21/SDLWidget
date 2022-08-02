TTF="D:\\Minget\\SDL_TTFmingw32\\lib"
SDL2="D:\\Minget\\SDL2mingw32\\lib"
Minget="D:\\Minget\\lib"
IMG="D:\\Minget\\SDLimagemingw32\\lib"
ming32_lib="mingw32"
SDL2main_lib="SDL2main"
SDL2_lib="SDL2"
TTF_lib="SDL2_ttf"
IMG_lib="SDL2_image"


main.exe:SDLButton.o SDLColor.o SDLWindow.o main.o SDLObject.o
	g++ -o $@ $^ -L$(TTF) -L$(SDL2) -L$(Minget) -L$(IMG) -l$(ming32_lib) -l$(SDL2main_lib) -l$(SDL2_lib) -l$(TTF_lib) -l$(IMG_lib)
main.o:main.cpp
	g++ -c main.cpp
SDLButton.o:SDLButton.cpp
	g++ -c SDLButton.cpp
SDLColor.o:SDLColor.cpp
	g++ -c SDLColor.cpp
SDLWindow.o:SDLWindow.cpp
	g++ -c SDLWindow.cpp
SDLObject.o:SDLObject.cpp
	g++ -c SDLObject.cpp
.PHONY:clean
clean:
	del *.o *.exe