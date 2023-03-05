#ifdef _WIN32
#include <direct.h>
#define getcwd _getcwd
#else
#include <unistd.h>
#endif

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <windows.h>
#include <conio.h>
#include <algorithm>
#include <cmath>

using namespace std;

// Support Functions
// ----------------------------------------------
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

std::string execute_command(const char *cmd)
{
    std::string output = "";
    char buffer[128];
    FILE *pipe = _popen(cmd, "r");
    if (pipe == NULL)
    {
        throw std::runtime_error("popen failed");
    }
    while (fgets(buffer, sizeof(buffer), pipe) != NULL)
    {
        output += buffer;
    }
    _pclose(pipe);
    // Remove newline characters from the output string
    output.erase(std::remove(output.begin(), output.end(), '\n'), output.end());
    output.erase(std::remove(output.begin(), output.end(), '\r'), output.end());
    return output;
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

void hwid_check()
{
    try
    {
        std::vector<std::string> HWIDS = {"7AB5C494-39F5-4941-9163-47F54D6D5016", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4", "FF577B79-782E-0A4D-8568-B35A9B7EB76B", "08C1E400-3C56-11EA-8000-3CECEF43FEDE", "6ECEAF72-3548-476C-BD8D-73134A9182C8", "49434D53-0200-9036-2500-369025003865", "119602E8-92F9-BD4B-8979-DA682276D385", "12204D56-28C0-AB03-51B7-44A8B7525250", "63FA3342-31C7-4E8E-8089-DAFF6CE5E967", "365B4000-3B25-11EA-8000-3CECEF44010C", "D8C30328-1B06-4611-8E3C-E433F4F9794E", "00000000-0000-0000-0000-50E5493391EF", "00000000-0000-0000-0000-AC1F6BD04D98", "4CB82042-BA8F-1748-C941-363C391CA7F3", "B6464A2B-92C7-4B95-A2D0-E5410081B812", "BB233342-2E01-718F-D4A1-E7F69D026428", "9921DE3A-5C1A-DF11-9078-563412000026", "CC5B3F62-2A04-4D2E-A46C-AA41B7050712", "00000000-0000-0000-0000-AC1F6BD04986", "C249957A-AA08-4B21-933F-9271BEC63C85", "BE784D56-81F5-2C8D-9D4B-5AB56F05D86E", "ACA69200-3C4C-11EA-8000-3CECEF4401AA", "3F284CA4-8BDF-489B-A273-41B44D668F6D", "BB64E044-87BA-C847-BC0A-C797D1A16A50", "2E6FB594-9D55-4424-8E74-CE25A25E36B0", "42A82042-3F13-512F-5E3D-6BF4FFFD8518", "38AB3342-66B0-7175-0B23-F390B3728B78", "48941AE9-D52F-11DF-BBDA-503734826431", "A7721742-BE24-8A1C-B859-D7F8251A83D3", "3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E", "D2DC3342-396C-6737-A8F6-0C6673C1DE08", "EADD1742-4807-00A0-F92E-CCD933E9D8C1", "AF1B2042-4B90-0000-A4E4-632A1C8C7EB1", "FE455D1A-BE27-4BA4-96C8-967A6D3A9661", "921E2042-70D3-F9F1-8CBD-B398A21F89C6", "6AA13342-49AB-DC46-4F28-D7BDDCE6BE32", "F68B2042-E3A7-2ADA-ADBC-A6274307A317", "07AF2042-392C-229F-8491-455123CC85FB", "4EDF3342-E7A2-5776-4AE5-57531F471D56", "032E02B4-0499-05C3-0806-3C0700080009"};

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
        if (!CreatePipe(&hChildStdoutRd, &hChildStdoutWr, &saAttr, 0))
        {
            throw std::runtime_error("Failed to create anonymous pipe");
        }

        if (!SetHandleInformation(hChildStdoutRd, HANDLE_FLAG_INHERIT, 0))
        {
            throw std::runtime_error("Failed to set handle information for anonymous pipe");
        }

        si.hStdOutput = hChildStdoutWr;
        si.dwFlags |= STARTF_USESTDHANDLES;

        // Launch the wmic process
        if (!CreateProcessA(NULL, &commandLine[0], NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi))
        {
            throw std::runtime_error("Failed to create process");
        }

        WaitForSingleObject(pi.hProcess, INFINITE);

        if (!CloseHandle(hChildStdoutWr))
        {
            throw std::runtime_error("Failed to close handle to anonymous pipe");
        }

        char buffer[1024];
        DWORD bytesRead;
        std::string output;
        while (ReadFile(hChildStdoutRd, buffer, sizeof(buffer), &bytesRead, NULL) && bytesRead > 0)
        {
            output.append(buffer, bytesRead);
        }

        if (!CloseHandle(hChildStdoutRd))
        {
            throw std::runtime_error("Failed to close handle to anonymous pipe");
        }

        std::string HWID = output.substr(0, output.find_first_of('\r'));

        if (std::find(HWIDS.begin(), HWIDS.end(), HWID) != HWIDS.end())
        {
            throw std::runtime_error("HWID is blacklisted");
        }
        else
        {
            mdebug("HWID check passed");
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}

void name_check()
{
    std::vector<std::string> NAMES = {"BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", "NETTYPC", "DESKTOP-BUGIO", "DESKTOP-CBGPFEE", "SERVER-PC", "TIQIYLA9TW5M", "DESKTOP-KALVINO", "COMPNAME_4047", "DESKTOP-19OLLTD", "DESKTOP-DE369SE", "EA8C2E2A-D017-4", "AIDANPC", "LUCAS-PC", "ACEPC", "MIKE-PC", "DESKTOP-IAPKN1P", "DESKTOP-NTU7VUO", "LOUISE-PC", "T00917", "test42", "DESKTOP-CM0DAW8"};

    try
    {
        std::string NAME = getenv("COMPUTERNAME");
        if (std::find(NAMES.begin(), NAMES.end(), NAME) != NAMES.end())
        {
            merror("Computer Name: " + NAME + " is blacklisted");
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

bool directory_exists(const std::string &dir_path)
{
    bool result = false;

#ifdef _WIN32
    if (_access(dir_path.c_str(), 0) == 0)
    {
        result = true;
    }
#else
    if (access(dir_path.c_str(), F_OK) == 0)
    {
        result = true;
    }
#endif
    return result;
}

void path_check()
{
    try
    {
        std::vector<std::string> paths = {"D:\\Tools", "D:\\OS2", "D:\\NT3X"};
        for (const auto &path : paths)
        {
            if (directory_exists(path))
            {
                std::cerr << "PATH: " << path << " is blacklisted" << std::endl;
            }
        }
        mdebug("Path Check has passed");
    }
    catch (const std::exception &e)
    {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}

void mac_check()
{
    try
    {
        std::vector<std::string> macs = {"00:03:47:63:8b:de","00:0c:29:05:d8:6e","00:0c:29:2c:c1:21","00:0c:29:52:52:50","00:0d:3a:d2:4f:1f","00:15:5d:00:00:1d","00:15:5d:00:00:a4","00:15:5d:00:00:b3","00:15:5d:00:00:c3","00:15:5d:00:00:f3","00:15:5d:00:01:81","00:15:5d:00:02:26","00:15:5d:00:05:8d","00:15:5d:00:05:d5","00:15:5d:00:06:43","00:15:5d:00:07:34","00:15:5d:00:1a:b9","00:15:5d:00:1c:9a","00:15:5d:13:66:ca","00:15:5d:13:6d:0c","00:15:5d:1e:01:c8","00:15:5d:23:4c:a3","00:15:5d:23:4c:ad","00:15:5d:b6:e0:cc","00:1b:21:13:15:20","00:1b:21:13:21:26","00:1b:21:13:26:44","00:1b:21:13:32:20","00:1b:21:13:32:51","00:1b:21:13:33:55","00:23:cd:ff:94:f0","00:25:90:36:65:0c","00:25:90:36:65:38","00:25:90:36:f0:3b","00:25:90:65:39:e4","00:50:56:97:a1:f8","00:50:56:97:ec:f2","00:50:56:97:f6:c8","00:50:56:a0:06:8d","00:50:56:a0:38:06","00:50:56:a0:39:18","00:50:56:a0:45:03","00:50:56:a0:59:10","00:50:56:a0:61:aa","00:50:56:a0:6d:86","00:50:56:a0:84:88","00:50:56:a0:af:75","00:50:56:a0:cd:a8","00:50:56:a0:d0:fa","00:50:56:a0:d7:38","00:50:56:a0:dd:00","00:50:56:ae:5d:ea","00:50:56:ae:6f:54","00:50:56:ae:b2:b0","00:50:56:ae:e5:d5","00:50:56:b3:05:b4","00:50:56:b3:09:9e","00:50:56:b3:14:59","00:50:56:b3:21:29","00:50:56:b3:38:68","00:50:56:b3:38:88","00:50:56:b3:3b:a6","00:50:56:b3:42:33","00:50:56:b3:4c:bf","00:50:56:b3:50:de","00:50:56:b3:91:c8","00:50:56:b3:94:cb","00:50:56:b3:9e:9e","00:50:56:b3:a9:36","00:50:56:b3:d0:a7","00:50:56:b3:dd:03","00:50:56:b3:ea:ee","00:50:56:b3:ee:e1","00:50:56:b3:f6:57","00:50:56:b3:fa:23","00:e0:4c:42:c7:cb","00:e0:4c:44:76:54","00:e0:4c:46:cf:01","00:e0:4c:4b:4a:40","00:e0:4c:56:42:97","00:e0:4c:7b:7b:86","00:e0:4c:94:1f:20","00:e0:4c:b3:5a:2a","00:e0:4c:b8:7a:58","00:e0:4c:cb:62:08","00:e0:4c:d6:86:77","06:75:91:59:3e:02","08:00:27:3a:28:73","08:00:27:45:13:10","12:1b:9e:3c:a6:2c","12:8a:5c:2a:65:d1","12:f8:87:ab:13:ec","16:ef:22:04:af:76","1a:6c:62:60:3b:f4","1c:99:57:1c:ad:e4","1e:6c:34:93:68:64","2e:62:e8:47:14:49","2e:b8:24:4d:f7:de","32:11:4d:d0:4a:9e","3c:ec:ef:43:fe:de","3c:ec:ef:44:00:d0","3c:ec:ef:44:01:0c","3c:ec:ef:44:01:aa","3e:1c:a1:40:b7:5f","3e:53:81:b7:01:13","3e:c1:fd:f1:bf:71","42:01:0a:8a:00:22","42:01:0a:8a:00:33","42:01:0a:8e:00:22","42:01:0a:96:00:22","42:01:0a:96:00:33","42:85:07:f4:83:d0","4e:79:c0:d9:af:c3","4e:81:81:8e:22:4e","52:54:00:3b:78:24","52:54:00:8b:a6:08","52:54:00:a0:41:92","52:54:00:ab:de:59","52:54:00:b3:e4:71","56:b0:6f:ca:0a:e7","56:e8:92:2e:76:0d","5a:e2:a6:a4:44:db","5e:86:e4:3d:0d:f6","60:02:92:3d:f1:69","60:02:92:66:10:79","7e:05:a3:62:9c:4d","90:48:9a:9d:d5:24","92:4c:a8:23:fc:2e","94:de:80:de:1a:35","96:2b:e9:43:96:76","a6:24:aa:ae:e6:12","ac:1f:6b:d0:48:fe","ac:1f:6b:d0:49:86","ac:1f:6b:d0:4d:98","ac:1f:6b:d0:4d:e4","b4:2e:99:c3:08:3c","b4:a9:5a:b1:c6:fd","b6:ed:9d:27:f4:fa","be:00:e5:c5:0c:e5","c2:ee:af:fd:29:21","c8:9f:1d:b6:58:e4","ca:4d:4b:ca:18:cc","d4:81:d7:87:05:ab","d4:81:d7:ed:25:54","d6:03:e4:ab:77:8e","ea:02:75:3c:90:9f","ea:f6:f1:a2:33:76","f6:a5:41:31:b2:78",};
        std::string mac = "";

        // Execute the "getmac" command to get the MAC address
        std::string output = execute_command("getmac /fo csv /nh");
        // Extract the MAC address from the output string
        size_t start = output.find_first_of('"') + 1;
        size_t end = output.find_last_of('"');
        mac = output.substr(start, end - start);

        // Check if the MAC address is blacklisted
        if (std::find(macs.begin(), macs.end(), mac) != macs.end())
        {
            std::cerr << "MAC Address: " << mac << " is blacklisted" << std::endl;
        }
        mdebug("Mac Check Passed");
    }
    catch (const std::exception &e)
    {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}

void dll_check()
{
    try
    {
        std::string system_root = std::getenv("SystemRoot");
        std::string vmware_dll = system_root + "\\System32\\vmGuestLib.dll";
        std::string virtualbox_dll = system_root + "\\vboxmrxnp.dll";

        std::ifstream vmware_file(vmware_dll.c_str());
        std::ifstream virtualbox_file(virtualbox_dll.c_str());

        if (vmware_file.good())
        {
            std::cerr << "Virtual Machine Detected: VMWare: from " << vmware_dll << std::endl;
        }
        else
        {
            mdebug("not vmware");
        }
        if (virtualbox_file.good())
        {
            std::cerr << "Virtual Machine Detected: VirtualBox: from " << virtualbox_dll << std::endl;
        }
        else
        {
            mdebug("not vbox");
        }
    }
    catch (std::exception const &e)
    {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}

void specs_check()
{
    try
    {
        MEMORYSTATUSEX memory_status;
        memory_status.dwLength = sizeof(memory_status);
        GlobalMemoryStatusEx(&memory_status);
        double RAM = static_cast<double>(memory_status.ullTotalPhys) / std::pow(1024, 3);

        if (RAM <= 2.0)
        {
            std::cerr << "Invalid RAM Amount" << std::endl;
        }
        else
        {
            mdebug("ram check passed");
        }
        SYSTEM_INFO sysinfo;
        GetSystemInfo(&sysinfo);
        if (sysinfo.dwNumberOfProcessors <= 1)
        {
            std::cerr << "Invalid CPU Count" << std::endl;
        }
        else
        {
            mdebug("cpu check passed");
        }
    }
    catch (std::exception const &e)
    {
        std::cerr << "[ERROR]: " << e.what() << std::endl;
    }
}

void anti_debug()
{
    user_check();
    hwid_check();
    name_check();
    path_check();
    mac_check();
    dll_check();
    specs_check();
}

int main()
{
    // Anti Debug Mocde Check
    anti_debug();
    return 0;

    std::cout << "\n\nPress [Enter] to close the console window..." << std::endl;
    while (_getch() != 13)
        ;
    return 0;
}
