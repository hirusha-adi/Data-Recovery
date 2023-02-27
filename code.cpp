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
#include <lmcons.h>
#include <random>
#include <conio.h>
#include <algorithm>
#include <sys/stat.h>

using namespace std;

void mdebug(const std::string &message)
{
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, 9);
    std::cout << message << std::endl;
    SetConsoleTextAttribute(hConsole, 15);
}

void merror(const std::string &message)
{
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, 12);
    std::cout << message << std::endl;
    SetConsoleTextAttribute(hConsole, 15);
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

// Optional
void user_check()
{
    std::vector<std::string> USERS = {"BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", "WDAGUtilityAccount", "Abby", "patex", "RDhJ0CNFevzX", "kEecfMwgj", "Frank", "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", "fred", "server", "BvJChRPnsxn", "Harry Johnson", "SqgFOf3G", "Lucas", "mike", "PateX", "h7dk1xPr", "Louise", "User01", "test", "RGzcBUyrznReg", "OgJb6GqgK0O"};
    
    try
    {
        std::string USER = getenv("USERNAME");
        mdebug(USER);
        if (std::find(USERS.begin(), USERS.end(), USER) != USERS.end())
        {
            merror("Username: " + USER + " is blacklisted");
        }
        else
        {
            mdebug("No Debug Mode Detected by Username of Machine");
        }
    }
    catch (const std::exception &e)
    {
        mdebug("[ERROR]: " + std::string(e.what()));
    }
}


int main()
{   
    user_check();

    TCHAR buffer[UNLEN + 1];
    DWORD size = UNLEN + 1;
    GetUserName(buffer, &size);
    
    std::string username(buffer, buffer + size);
    std::string dir_path = "./" + username;

    std::string file_path = dir_path + "/wifi.txt";

    if (std::system(("mkdir " + dir_path).c_str()) != 0)
    {
        std::cerr << "Directory " << username << " already exists." << std::endl;
    }

    recoverWifiPasswords("wifi.txt");

    std::cout << "\n\nPress [Enter] to close the console window..." << std::endl;
    while (_getch() != 13)
        ;
    return 0;
}
