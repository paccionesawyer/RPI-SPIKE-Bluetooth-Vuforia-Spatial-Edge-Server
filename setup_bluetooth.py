"""
Author:  Sawyer Bailey Paccione 
File:    setup_bluetooth.py
Purpose: Setup a Spike Prime on a Raspberry Pi hosting a vuforia spatial edge 
         server.
Last Edit: 7/7/2021, Sawyer Paccione
Company:   Tufts CEEO Fetlab
Description: A simple command-line user interface that will (1) Add a new 
             device by prompting for the name, then making the necessary 
             connections and generating the appropriate vuforia interface 
             folders. (2) Bind all of the already connected devices to 
             appropriate rfcomm ports. (3) Release Binded devices from their 
             rfcomm ports.
Usage: In the Command Line "python3 setup_bluetooth.py"
"""

import os, re, sys, shutil, time, pexpect

def find_mac(search_name):
    '''
    Given the name of a device, find the mac address (DEVICE MUST BE TURNED 
    ON AND PAIRING)
    '''
    response=''
    p = pexpect.spawn('hcitool scan', encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect(search_name)
    response = p.before
    devices = response.split("\n")
    device = devices[-1]
    mac = parse_mac(device)
    
    print("The Mac Address of your Device is:", mac)

    p.close()

    return mac

def parse_mac(line_string):
    '''
    Given a line it will find the first mac address in it (assuming colons ':' 
    aren't used for anything else)
    '''
    index = line_string.find(':')
    mac_address = line_string[index - 2: index + 15]
    return mac_address

def extract_ints(parse_string):
    '''
    Given a string, it will find the first integer in the string
    '''
    int_string = re.findall(r'\d+', parse_string)
    int_string = int_string[0]

    return int_string

def pair_device(mac):
    '''
    Pairs and Trusts the mac address of the new device using bluetoothctl
    '''
    p = pexpect.spawn('bluetoothctl', encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect("#")
    p.sendline("pair " + mac)
    p.sendline("trust " + mac)

def edit_bluetooth(name, mac):
    '''
    Edits the rfBind.sh and rfRelease.sh file with the newly added device
    '''
    # Check to see if files already exist
    if os.path.exists("rfBind.sh") and os.stat("rfBind.sh").st_size != 0:
        bluetooth_file = open("rfBind.sh", 'r')
        list_of_lines = bluetooth_file.readlines()
        for line in list_of_lines:
            if mac in line:
                print("MAC Address Already Paired: Exiting Setup")
                return False, -1
        last_used = find_last_nonempty_line(list_of_lines)
        port = str(int(extract_ints(last_used)) + 1)
        bluetooth_file.close()
    else: 
        bluetooth_file = open("rfBind.sh", 'w')
        print("Empty File")
        port = "0"
        bluetooth_file.close()

    bluetooth_file = open("rfBind.sh", 'a')
    bluetooth_file.write('\necho "Attempting to Bind to ' + name +' - MAC Address '+ mac + '"\n')
    bluetooth_file.write('sudo rfcomm bind ' + port + " " + mac + '\n')
    bluetooth_file.write("sudo ampy --port /dev/rfcomm" + port + " run test.py\n")
    bluetooth_file.close()

    release_file = open("rfRelease.sh", 'a')
    release_file.write('\necho "Releasing rfcomm' + port +' from '+ name + '"\n')
    release_file.write('sudo rfcomm release ' + port + '\n')
    release_file.close()
    return True, port 

def find_last_nonempty_line(list_of_lines):
    '''
    Find the last line that has content in a file converted to list
    '''
    index = -1 
    while list_of_lines[index] == "" or list_of_lines[index] == '\n':
        index = index - 1
    return list_of_lines[index]

def make_new_directory(name, port):
    '''
    Creates a new directory in Vuforia Spatial Toolbox for the new device based off the original Spike-Prime interface
    '''

    # Copy all of the data from the original Spike-Prime Interface to new dir
    path = "/home/pi/vuforia-spatial-edge-server/addons/vuforia-spatial-robotic-addon/interfaces/"
    src  = path + "Spike-Prime"
    dest = path + "Spike-Prime" + port + "_" + name
    
    destination = shutil.copytree(src, dest) 
    return destination

def edit_object_files(name, mac):
    '''
    Edits the Vuforia Spatial Toolbox Files To associate with the newly added device
    '''

    # Edit the serial file for the new device
    resp = edit_bluetooth(name, mac)
    if (not resp[0]):
        return
    else :
        port = resp[1]
    path = "/home/pi/vuforia-spatial-edge-server/addons/vuforia-spatial-robotic-addon/interfaces/"
    src = path + "Spike-Prime"
    if (port != "0"):
        make_new_directory(name, port)
        dest = path + "Spike-Prime" + port + "_" + name
    else :
        dest = src

    # Edit the rfcomm port of the new devices
    serial_file = open(src + "/serial.js", "r")
    list_of_lines = serial_file.readlines()

    for i in range(len(list_of_lines)):
        if list_of_lines[i].startswith("const port = new SerialPort") and list_of_lines[i][0] != '/': 
            list_of_lines[i] = "const port = new SerialPort('/dev/rfcomm"+ port +"', {\n" 
    
    serial_file = open(dest + "/serial.js", "w")
    serial_file.writelines(list_of_lines)
    serial_file.close()

    # Edit Three Lines in the index.js file
    index_file = open(src + "/index.js", "r")
    list_of_lines = index_file.readlines()

    for i in range(len(list_of_lines)):
        if list_of_lines[i].startswith("var TOOL_NAME"): 
            list_of_lines[i] = 'var TOOL_NAME = "Spike' + port + "_" + name + '"; // This is what is made on the webserver for the image target\n'
        elif list_of_lines[i].startswith("let objectName"): 
            list_of_lines[i] = 'let objectName = "spikeNode' + port + "_" + name +'"; // This is the name of the folder in spatialToolbox in Documents\n'
        elif list_of_lines[i].startswith("var complexity"): 
            list_of_lines[i] = 'var complexity = "Spike' + port + "_" + name + '"; // This will make sure the complexity level for each can be different\n'
            
    index_file = open(dest + "/index.js", "w")
    index_file.writelines(list_of_lines)
    index_file.close()

    return port

def validate_input(prompt, valid_answers):
    '''
    Validates users answers to <prompt>, with a list of <valid_answers>
    '''
    response = input(prompt)
    # Continue prompting user until their answer is found withing valid_answers
    while (response.lower() not in valid_answers):
        print("Please respond with either a ", end = "")
        for i in range(len(valid_answers)):
            ans = valid_answers[i]
            if i != len(valid_answers) - 1 :
                print(ans, end=", ")
            else :
                print("or", ans)
        response = input(prompt)

    return response.lower()

def main():
    '''
    User-Interface for the program
    '''
    add_device = validate_input("Would you like to add a new device (Y/N)? ", ['y', 'n'])

    if (add_device == 'y'):
        correct_input = True
        search_name = input("What is the name of the device you want to add? ")
        mac = find_mac(search_name)
        pair_device(mac)
        edit_object_files(search_name, mac)
    elif (add_device == 'n'):
        correct_input = True
        print("Not adding new device")

    bind_devices = validate_input("Would you like to Bind Devices (Y/N)? ", ['y', 'n'])

    if(bind_devices == 'y'):
        os.system("sudo bash rfBind.sh")
    else:
        release_devices = validate_input("Would you like to Release Devices (Y/N)? ", ['y', 'n'])

        if(release_devices == 'y'):
            os.system("sudo bash rfRelease.sh")
        else:
            print("No Releasing")

if __name__ == "__main__":
    main()