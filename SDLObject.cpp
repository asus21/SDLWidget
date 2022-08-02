#include "SDLObject.hpp"

SDLObject::SDLObject(SDLObject *top, std::string text, std::string prefix, SDLColor bg, SDLColor fg, int xpos, int ypos, int width, int height, std::string font, std::string picture)
{
    father = top;
    win = top->win;
    ren = top->ren;
    /*控件的位置*/
    rect.x = xpos;
    rect.y = ypos;
    rect.w = width;
    rect.h = height;

    this->text = text;       //控件的文本
    this->picture = picture; //控件的图片
    this->bg = bg;           //控件的背景
    this->fg = fg;           //控件前景

    /*设置控件ID*/
    std::stringstream ss;
    ss << prefix << "_" << top->widget.size();
    id = ss.str();

    top->addWidget(this); //父控件添加子控件
}
void SDLObject::setSize(int w, int h)
{
    this->rect.w = w;
    this->rect.h = h;
}
void SDLObject::setBackground(SDLColor color)
{
    this->bg = color;
}
void SDLObject::setForeground(SDLColor color)
{
    this->fg = color;
}
void SDLObject::setText(std::string text)
{
    this->text = text;
}
void SDLObject::setPicture(std::string picture)
{
    this->picture = picture;
}
void SDLObject::setPadding(int padding)
{
    this->padding = padding;
}
void SDLObject::setMargin(int margin)
{
    this->margin = margin;
}
void SDLObject::setFontSize(int size)
{
    this->fontsize = size;
}
void SDLObject::setFont(std::string font)
{
    this->font = font;
}
void SDLObject::getSize(int &w, int &y)
{
    w = this->rect.w;
    y = this->rect.h;
}
SDLColor SDLObject::getBackground()
{
    return this->bg;
}
SDLColor SDLObject::getForeground()
{
    return this->fg;
}
std::string SDLObject::getText()
{
    return this->text;
}
std::string SDLObject::getPicture()
{
    return this->picture;
}
int SDLObject::getPadding()
{
    return this->padding;
}
int SDLObject::getMargin()
{
    return this->margin;
}
std::string SDLObject::getFont()
{
    return this->font;
}
int SDLObject::getFontSize()
{
    return this->fontsize;
}
void SDLObject::handleEvent(SDL_Event event)
{
    std::cout << "handEvent doesn't implement"<<std::endl;
}
void SDLObject::draw()
{
    std::cout << "draw doesn't implement"<<std::endl;
}

void SDLObject::main()
{
    std::cout << "main doesn't implement"<<std::endl;
}
void SDLObject::addWidget(SDLObject *widget)
{
    this->widget.push_back(widget);
}

SDL_Texture *SDLObject::Font_To_Texture()
{
    if (TTF_Init() != 0)
    {
        std::cout << "font init error"<<std::endl;
        return NULL;
    }
    if (font.size() == 0)
    {
#if defined(__WIN32__) || defined(__WINRT__)
        font.append("C:\\Windows\\Fonts\\SIMSUN.TTC");
#elif defined(__LINUX__)
        font.append("/fonts/SIMSUN.TTC");
#endif
    }
    TTF_Font *font = TTF_OpenFont(this->font.c_str(), 20);
    if (font==NULL)
    {
        std::cout << "font open error" <<std::endl;
        return NULL;
    }
    SDL_Surface *surface = TTF_RenderUTF8_Solid(font, text.c_str(), fg.color);
    SDL_Texture *texture = SDL_CreateTextureFromSurface(ren, surface);
    SDL_FreeSurface(surface);
    TTF_CloseFont(font);
    return texture;
}

SDL_Texture* SDLObject::Picture_To_Texture()
{
    if(IMG_Init(IMG_INIT_PNG)==0)
    {
        std::cout<<"image init error"<<std::endl;
    }
    if (picture.size() == 0)
    {
        std::cout<<"not giving picture"<<std::endl;
    }
    SDL_Surface* surface =IMG_Load(this->font.c_str());
    if (!surface)
    {
        std::cout << "image open error" <<std::endl;
        return NULL;
    }
    SDL_Texture *texture = SDL_CreateTextureFromSurface(ren, surface);
    SDL_FreeSurface(surface);
    return texture;
} 