# RaspberryPi-SpatialToolbox-BluetoothLegoSpikePrime

Code to connect a Spike Prime to a Vuforia-Spatial-Edge-Server on a Raspberry Pi

<details>
<summary><b>DIY (Not Recommended)</b></summary>

## Instructions

### Step 1: Pairing Bluetooth Device

There are a few required packages, which will also require you to reboot your device.

    sudo apt update -y && sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo apt-get autoclean -y && sudo reboot
Your device will now reboot, once you have logged back in run the following command.

    sudo apt-get install bluetooth bluez blueman pi-bluetooth python-dev libbluetooth-dev python3-pip -y && sudo pip3 install pybluez adafruit-ampy

Next you will need to edit a line and add a line in the file that can be accessed by.

  sudo vim /etc/systemd/system/dbus-org.bluez.service

Edit the line `ExecStart=/usr/lib/bluetooth/bluetoothd` to read `ExecStart=/usr/lib/bluetooth/bluetoothd -C`, and insert the line `ExecStartPost=/usr/bin/sdptool add SP` immediately afterwards.

Now reboot your Pi one last time by doing

    sudo reboot

Once the pi has restarted log in and run the following lines of code one at a time.

    sudo service bluetooth start

    sudo bluetoothctl
    power on
    pairable on
    discoverable on
    agent on
    default-agent
    quit

Now we will scan for the bluetooth device, it will have the name `LegoHub@<SPIKE NAME>`, and copy down the mac address associated with it. (Any way that you know how to find a mac address can replace this step)

    bluetoothctl scan on

Once you have the mac address run the following lines of code

    bluetoothctl pair <mac>
    bluetoothctl trust <mac>

Now we need to bind the Spike to a rfcomm port in order to perform serial communication, we do this by binding. (This needs to be run everytime you restart the Pi)

    sudo rfcomm bind 0 <mac>
    sudo ampy --port /dev/rfcomm0 run test_connection.py

When you are done release the port

    sudo rfcomm release 0

### Step 2: Creating a New Image Target

* To add another SPIKE Prime, we need to be able to attach it to a new image target
* Checkout our YouTube Tutorial video: <https://youtu.be/TBEV5K3dprA>

### Step 3: Duplicating Files

* Next, we need to go into `vuforia-spatial-edge-server` --> `addons` --> `vuforia-spatial-robotic-addon` --> `interfaces`
* Here, we can see the folder called `Spike-Prime`. If we go into the folder, our first SPIKE Prime should already be connected through editing the `serial.js` and `index.js` files
* What we need to now do is to duplicate the entire `Spike-Prime` folder and call it `Spike-Prime2` (you can increment this number based on the number of SPIKE's you want to connect)
  
### Step 4: Editing Files

* After duplicating the folder, we can then go into the `serial.js` file in the duplicated folder
* Edit line 25 so that the serial port is for the new SPIKE Prime (This will be whatever rfcomm port you connected the device to i.e. `/dev/rfcomm0`)
* When we finish typing the updated serial port, we can go into the `index.js` file within this same folder
* Here we need to edit lines 6-8
  * Line 6 should be called `Spike2` (again increment the number based on the number of SPIKE's)
  * Line 7 should be the new name of the folder that you made within `spatialToolbox` (see <b>Step 1</b> above)
  * Line 8 should have the same name as Line 6

### Step 5: Starting the Server

* Finally, we can save everything and start the server. If all the steps have been followed, it should start working!
* <b> Note: </b> Sometimes the SPIKE needs to be connected a few times to make and establish the connection. See our YouTube playlist above for more information.

</details>

<details>
<summary><b>Python Script</b></summary>

### Step 1: Download Bluetooth (NOT WORKING Follow Step 1 of DIY and then continue here)

First clone this repository onto your Raspberry Pi using the following command

    git clone https://github.com/paccionesawyer/vuforia-spatial-RPI-SPIKE-Bluetooth.git

Then change into the directory `cd vuforia-spatial-RPI-SPIKE-Bluetooth` and then run the first program, this will reboot your Spike Prime. It is downloading the necessary files to your device and setting up bluetooth. This only needs to be run once and corresponds to Step 1 of the DIY section.

    sudo python3 initialize.py 

### Step 2: Add a Spike-Prime

If you would like to add a Spike Prime, turn it on and press the bluetooth button. Once it is blinking run the following command.

    python3 setup_bluetooth.py

The built in command-line user-interface will take you through the rest of the setup. (If you would like to use it you must bind your device everytime you restart your Pi)
Once the setup is done, all you need to do is start the Edge Server like normal, and set an image target for the newly added Spike.
</details>
