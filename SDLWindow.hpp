#include <iostream>
#include <SDL2/SDL.h>
#include <vector>
#include "SDLObject.hpp"
#ifndef SDLWINDOW_HPP
#define SDLWINDOW_HPP
class SDLWindow:public SDLObject
{
    public:
    SDLWindow(const char* title,int xpos,int ypos,int width,int height,int flags);
    SDLWindow();
    ~SDLWindow();
    
    virtual void render();
    virtual void handleEvent();
    virtual void addWidget(SDLObject* widget);
    virtual void main();
    virtual void setTitle(std::string);  
};
#endif