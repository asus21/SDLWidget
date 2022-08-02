#include "SDLColor.hpp"
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <fstream>
#include <string>
SDLColor::SDLColor(std::string ccolor)
{
    std::ifstream in("color.txt");
    std::string a;
    std::string b;
    std::string c;
    std::string d;
    std::string e;
    std::string temp = "";
    while (std::getline(in, temp))
    {
        std::istringstream ss(temp);
        ss >> a >> b >> c >> d >> e;
        if (a == ccolor || b == ccolor.substr(0, ccolor.length() - 2))
        {
            color = {(uint8_t)atoi(c.c_str()), (uint8_t)atoi(d.c_str()), (uint8_t)atoi(e.c_str())};
            break;
        }
    }
    if (ccolor.find("#") >= 0)
    {
        temp = ccolor.substr(ccolor.length() - 2, 2);
        if (temp != "")
        {
            temp = "0x" + temp;
            int nValude = 0;
            sscanf(temp.c_str(), "%x", &nValude); //十六进制转数字
            color.a = nValude;
        }
    }
    else
        color.a = 255;
}
SDLColor SDLColor::operator=(std::string color)
{
    return SDLColor(color);
}
SDLColor SDLColor::operator=(SDLColor color)
{
    this->color=color.color;
    return *this;
}