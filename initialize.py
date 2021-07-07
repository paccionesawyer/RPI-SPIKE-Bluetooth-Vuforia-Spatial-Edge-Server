import os 

def install_libraries():

    os.system("sudo apt update -y && sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo apt-get autoclean -y")

    os.system("sudo apt-get install bluetooth bluez blueman pi-bluetooth python-dev libbluetooth-dev python3-pip -y && sudo pip3 install pybluez adafruit-ampy")


def edit_file():
    file_path = "/etc/systemd/system/dbus-org.bluez.service"
    read = open(file_path, "r")

    list_of_lines = read.readlines()

    edit_line = "ExecStart=/usr/lib/bluetooth/bluetoothd"

    for i in range(len(list_of_lines)):
        if edit_line in list_of_lines[i]:
            print("found")
            list_of_lines[i] = "ExecStart=/usr/lib/bluetooth/bluetoothd -C\n"
            list_of_lines.insert(i+1,"ExecStartPost=/usr/bin/sdptool add SP\n")

    read.close()

    write = open(file_path, "w")

    write.writelines(list_of_lines)

    write.close()
    
def init_bluetoothctl():
    os.system("sudo service bluetooth start")
    os.system("sudo bluetoothctl")
    os.system("power on")
    os.system("pairable on")
    os.system("discoverable on")
    os.system("agent on")
    os.system("default-agent")
    os.system("quit")
    
def main():
    install_libraries()
    edit_file()

    os.system("sudo reboot")

if __name__ == "__main__":
    main()
