#include "SDLWindow.hpp"
SDLWindow::SDLWindow():SDLWindow("MainWindow",100,100,480,360,SDL_WINDOW_SHOWN){}
SDLWindow::~SDLWindow()
{
    std::cout << "cleaning wind";
    SDL_DestroyWindow(win);
    SDL_DestroyRenderer(ren);
    SDL_Quit();
};
SDLWindow::SDLWindow(const char *title, int xpos, int ypos, int width, int height, int flags)
{
    if (SDL_Init(SDL_INIT_EVERYTHING) != 0)
    {
        std::cout << "init error";
    }
    win = SDL_CreateWindow(title, xpos, ypos, width, height, flags);
    if (win == NULL)
    {
        std::cout << "window create error";
    }
    ren = SDL_CreateRenderer(win, -1, 0);
    if (ren == NULL)
    {
        std::cout << "render create error";
    }
    isRun = true;
}
void SDLWindow::render()
{
    SDL_SetRenderDrawColor(ren, 255, 255, 255, 255);
    SDL_RenderClear(ren);
    for (SDLObject *temp : widget)
    {
        temp->draw();
    }
    SDL_RenderPresent(ren);
}
void SDLWindow::handleEvent()
{
    SDL_Event event;
    if (SDL_PollEvent(&event))
    {
        switch (event.type)
        {
        case SDL_QUIT:
            isRun = false;
            break;
        default:
            for (SDLObject *x : widget)
            {
                x->handleEvent(event);
            }
            break;
        }
    }
}
void SDLWindow::addWidget(SDLObject *widget) 
{
    this->widget.push_back(widget); 
}
void SDLWindow::main()
{
    while (isRun)
    {
        handleEvent();
        render();
    }
}
void SDLWindow::setTitle(std::string title)
{
    SDL_SetWindowTitle(win,title.c_str());
}