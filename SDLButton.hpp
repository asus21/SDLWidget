#include <SDL2/SDL.h>
#include <iostream>
#include "SDLObject.hpp"
#ifndef SDLBUTTON_HPP
#define SDLBUTTON_HPP
#define BUTTON "BUTTON"
class SDLButton : public SDLObject
{
public:
    SDLButton(SDLObject* top);
    SDLButton(SDLObject* top, std::string text, SDLColor bbg=SDLColor("White"), SDLColor ffg=SDLColor("White"), int xpos=0, int ypos=0, int width=50, int height=30, std::string picture="");
    virtual void draw();
    virtual void handleEvent(SDL_Event event);
};
#endif