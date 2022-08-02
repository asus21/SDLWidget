#include <iostream>
#include <SDL2/SDL.h>
#include "SDLButton.hpp"
#include "SDLWindow.hpp"
#include "SDLColor.hpp"
#include <fstream>
#include <string>

class MainWindow :public SDLWindow
{
    private:
    SDLButton *but;
    public:
    MainWindow()
    {
       but=new SDLButton(this,"ok",SDLColor("Red"),SDLColor("Red"));
       but->bind(this,onClick);
    }
    void onClick(SDL_Event event)
    {
        std::cout<<"exit";
        SDL_Quit();
    }
};
int main(int args,char** argv)
{
    SDLColor color=std::string("#FF0000FF");
    MainWindow *win=new MainWindow();
    //win->init("Chapter1",100,100,640,480,SDL_WINDOW_SHOWN);
    win->main();
   return 0;
}