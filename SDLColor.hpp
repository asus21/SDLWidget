#include <SDL2/SDL.h>
#include <string>
#ifndef COLOR_HPP
#define COLOR_HPP
class SDLColor
{
    public:
    SDL_Color color;
    public:
    SDLColor(){}
    SDLColor(uint8_t r,uint8_t g,uint8_t b,uint8_t a):color{r,g,b,a}{}
    SDLColor(std::string);
    SDLColor operator=(std::string );
    SDLColor operator=(SDLColor);
};
#endif