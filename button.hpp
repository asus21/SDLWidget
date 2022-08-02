#include <iostream>
#include <string>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL.h>
using namespace std;
#ifndef BUTTON_HPP
#define BUTTON_HPP
class Button
{
    private:
    SDL_Renderer* ren;
    SDL_Rect rect;
    string text;
    public:
    Button(SDL_Renderer* ren,SDL_Rect rect,string text);
    SDL_Texture* LoadFont();
    void onDraw();
    void onPress(SDL_Event event);
};
#endif