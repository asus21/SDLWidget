#include <iostream>
#include <string>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#include <sstream>
#include "SDLColor.hpp"
#include "SDLSlot.hpp"
#ifndef SDLOBJECT_HPP
#define SDLOBJECT_HPP
class SDLObject
{
protected:
    bool isRun;
    SDL_Renderer *ren;
    SDL_Window *win;
    SDLColor bg;
    SDLColor fg;
    SDL_Rect rect;
    SDLObject *father;
    Signal<SDL_Event> signal;
    std::string font;
    std::string id;
    std::string text;
    std::string picture;
    int padding;
    int margin;
    int fontsize;
    std::vector<SDLObject *> widget;
    virtual SDL_Texture* Font_To_Texture();
    virtual SDL_Texture* Picture_To_Texture();
public:
    SDLObject(){isRun=false;};
    SDLObject(SDLObject *top, std::string text, std::string prefix, SDLColor bg = SDLColor("White"), SDLColor fg = SDLColor("White"), int xpos = 0, int ypos = 0, int width = 50, int height = 30, std::string font = "", std::string picture = "");
    const char *getID() { return id.c_str(); }
    template <typename F, typename T>
    void bind(F top, void (T::*func)(SDL_Event)) { signal.Bind(top, func); }
    virtual void setSize(int w, int h);
    virtual void setBackground(SDLColor color);
    virtual void setForeground(SDLColor color);
    virtual void setText(std::string text);
    virtual void setPicture(std::string picture);
    virtual void setPadding(int padding);
    virtual void setMargin(int margin);
    virtual void setFontSize(int size); 
    virtual void setFont(std::string font);
    virtual void getSize(int &w,int &h);
    virtual SDLColor getBackground();
    virtual SDLColor getForeground();
    virtual std::string getText();
    virtual std::string getPicture();
    virtual int getPadding();
    virtual int getMargin();
    virtual std::string getFont();
    virtual int getFontSize();
    virtual void handleEvent(SDL_Event event);
    virtual void draw();
    virtual void main();
    virtual void addWidget(SDLObject *);
};
#endif