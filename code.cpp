#ifndef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <cstdio>
#include <cstdlib>
#include <sstream>
#include <array>
#include <stdexcept>
#include <iomanip>
#include <windows.h>
#include <conio.h>
#include <cstdio>

using namespace std;

static bool consoleHasColors = false;
static HANDLE consoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);

void mdebug(std::string message)
{
    if (!consoleHasColors)
    {
        DWORD consoleMode;
        if (GetConsoleMode(consoleHandle, &consoleMode))
        {
            consoleHasColors = SetConsoleMode(consoleHandle, consoleMode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
        }
    }
    if (consoleHasColors)
    {
        std::cout << "\33[90m" << message << "\033[0m" << std::endl;
    }
    else
    {
        std::cout << message << std::endl;
    }
}

void merror(std::string message)
{
    if (!consoleHasColors)
    {
        DWORD consoleMode;
        if (GetConsoleMode(consoleHandle, &consoleMode))
        {
            consoleHasColors = SetConsoleMode(consoleHandle, consoleMode | ENABLE_VIRTUAL_TERMINAL_PROCESSING);
        }
    }
    if (consoleHasColors)
    {
        std::cout << "\033[31m" << message << "\033[0m" << std::endl;
    }
    else
    {
        std::cout << message << std::endl;
    }
}

void checkFileExists(std::string filename)
{
    if (std::remove(filename.c_str()) != 0)
    {
        mdebug("No existing file " + filename + " to delete.");
    }
    else
    {
        merror("Existing file " + filename + " deleted.");
    }
}

void recoverWifiPasswords(std::string wifi_passwords_filename)
{

    cout << "      _______         _  _  _ _       _______ _ " << std::endl;
    cout << "     |.-----.|       (_)(_)(_|_)     (_______|_)" << std::endl;
    cout << "     ||x . x||        _  _  _ _ _____ _____   _" << std::endl;
    cout << "     ||_.-._||       | || || | (_____)  ___) | |" << std::endl;
    cout << "     `--)-(--`       | || || | |     | |     | |" << std::endl;
    cout << "    __[=== o]___      \\_____/|_|     |_|     |_|" << std::endl;
    cout << "   |:::::::::::|\\    " << std::endl;
    cout << "   `-=========-`()            Passwords\n\n"
         << std::endl;

    checkFileExists(wifi_passwords_filename);
    std::ofstream file(wifi_passwords_filename, std::ios::out | std::ios::app);
    if (!file)
    {
        throw std::runtime_error("Error opening file");
    }

    mdebug("Created file and starting to save wifi passwords to it -> " + wifi_passwords_filename);
    mdebug("Running command: `netsh wlan show profiles`");

    std::string command = "netsh wlan show profiles";
    std::array<char, 128> buffer{}; // Initializes all elements to 0
    std::string data;
    FILE *pipe = _popen(command.c_str(), "r");
    if (!pipe)
    {
        throw std::runtime_error("popen() failed");
    }
    while (fgets(buffer.data(), 128, pipe) != nullptr)
    {
        data += buffer.data();
    }
    _pclose(pipe);

    std::vector<std::string> profiles;
    std::stringstream ss(data);
    std::string line;
    while (std::getline(ss, line))
    {
        if (line.find("All User Profile") != std::string::npos)
        {
            std::string profile = line.substr(line.find(":") + 2, line.length() - 1);
            profiles.push_back(profile);
        }
    }

    mdebug("Found a total of " + std::to_string(profiles.size()) + " WiFi networks");

    for (const auto &i : profiles)
    {
        try
        {
            std::string command = "netsh wlan show profile " + i + " key=clear";
            mdebug("Running command: `" + command + "`");
            std::array<char, 128> buffer{};
            std::string results;
            FILE *pipe = _popen(command.c_str(), "r");
            if (!pipe)
            {
                throw std::runtime_error("popen() failed");
            }
            while (fgets(buffer.data(), 128, pipe) != nullptr)
            {
                results += buffer.data();
            }
            _pclose(pipe);

            std::vector<std::string> keys;
            std::stringstream ss(results);
            std::string line;
            while (std::getline(ss, line))
            {
                if (line.find("Key Content") != std::string::npos)
                {
                    std::string key = line.substr(line.find(":") + 2, line.length() - 1);
                    keys.push_back(key);
                }
            }

            if (!keys.empty())
            {
                mdebug("Found password of " + i + " wifi network");
                file << std::left << std::setw(30) << i << "|  " << keys[0] << std::endl;
            }
            else
            {
                std::cout << "Unable to get the password of " << i << " network. No password is available -> by Running `netsh wlan show profile " << i << " key=clear`" << std::endl;
                file << std::left << std::setw(30) << i << "|  "
                     << "" << std::endl;
            }
        }
        catch (const std::exception &ex)
        {
            merror("Unable to get the wifi password of " + i + " network -> " + ex.what());
            file << std::left << std::setw(30) << i << "|  "
                 << "ENCODING ERROR" << std::endl;
        }
    }

    mdebug("Saved all wifi passwords to " + wifi_passwords_filename);
}

int main()
{
    recoverWifiPasswords("wifi.txt");

    std::cout << "\n\nPress [Enter] to close the console window..." << std::endl;
    while (_getch() != 13)
        ;
    return 0;
}
