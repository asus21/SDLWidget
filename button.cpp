#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL.h>
#include "button.hpp"
#include <iostream>
using namespace std;

Button::Button(SDL_Renderer* ren,SDL_Rect rect,string text)
{
    this->ren=ren;
    this->rect=rect;
    this->text=text;
}
SDL_Texture* Button::LoadFont()
{
    TTF_Init();
    TTF_Font* font=TTF_OpenFont("C:\\Windows\\Fonts\\SIMSUN.TTC",20);
    if(!font)
    {
        cout<<"font open error"<<SDL_GetError();
        return NULL;
    }
    SDL_Color fontcolor={255,0,0,255};
    SDL_Surface* surface=TTF_RenderUTF8_Solid(font,text.c_str(),fontcolor);
    SDL_Texture* texture=SDL_CreateTextureFromSurface(ren,surface);
    SDL_FreeSurface(surface);
    TTF_CloseFont(font);
    return texture;
}
void Button::onDraw()
{
    SDL_Texture* texture=LoadFont();
    if(texture!=NULL)
    {
    int w,h;
    SDL_QueryTexture(texture,NULL,NULL,&w,&h);
    rect={0,0,w,h};
    SDL_RenderCopy(ren,texture,NULL,&rect);
    SDL_SetRenderDrawColor(ren,255,0,0,255);
    SDL_RenderDrawRect(ren,&rect);
    }
    SDL_DestroyTexture(texture);
}