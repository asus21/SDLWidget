#include "SDLButton.hpp"
SDLButton::SDLButton(SDLObject* top):SDLButton(top,"BUTTON")
{

}
SDLButton::SDLButton(SDLObject* top, std::string text, SDLColor bbg, SDLColor ffg, int xpos, int ypos, int width, int height, std::string picture):SDLObject(top,text,BUTTON,bbg,ffg,xpos,ypos,width,height,picture)
{

}
void SDLButton::draw()
{
    SDL_Texture* font=this->Font_To_Texture();
    SDL_Texture* picture=this->Picture_To_Texture();
    SDL_SetRenderDrawColor(ren, bg.color.r, bg.color.g, bg.color.b, bg.color.a);
    int w,h;
    SDL_QueryTexture(font,NULL,NULL,&w,&h);
    rect.x=100,rect.y=100,rect.w=w,rect.h=h;
    SDL_RenderCopy(ren,font,NULL,&rect);
    //SDL_RenderDrawRect(ren, &rect);
}

void SDLButton::handleEvent(SDL_Event event)
{
    SDL_Point point{event.button.x, event.button.y};
    if (event.type == SDL_MOUSEBUTTONDOWN&&SDL_PointInRect(&point,&rect))
    {
        if (signal.isBind())
        {
            signal(event);
        }
    }
}
