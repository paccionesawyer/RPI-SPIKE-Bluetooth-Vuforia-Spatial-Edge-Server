# RaspberryPi-SpatialToolbox-BluetoothLegoSpikePrime
Code to connect a Spike Prime to a Vuforia-Spatial-Edge-Server on a Raspberry Pi 

<details>
<summary><b>DIY (Not Recommended)</b></summary>
### Step 1: Pairing Bluetooth Device
  * First we need to update our device, this will take some time, we do this by running the following commands 
    
    `sudo apt update -y && sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt dist-upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean -y && sudo apt-get autoclean -y && sudo reboot`<br>
    `sudo apt-get install bluetooth bluez blueman pi-bluetooth python-dev libbluetooth-dev python3-pip -y && sudo pip3 install pybluez adafruit-ampy`
  *
  ### Step 2: Creating a New Image Target ###
  * To add another SPIKE Prime, we need to be able to attach it to a new image target
  * Checkout our YouTube Tutorial video: https://youtu.be/TBEV5K3dprA
 
  ### Step 3: Duplicating Files ###
  * Next, we need to go into `vuforia-spatial-edge-server` --> `addons` --> `vuforia-spatial-robotic-addon` --> `interfaces`
  * Here, we can see the folder called `Spike-Prime`. If we go into the folder, our first SPIKE Prime should already be connected through editing the `serial.js` and `index.js` files
  * What we need to now do is to duplicate the entire `Spike-Prime` folder and call it `Spike-Prime2` (you can increment this number based on the number of SPIKE's you want to connect) 
  
  ### Step 4: Editing Files ###
  * After duplicating the folder, we can then go into the `serial.js` file in the duplicated folder
  * Edit line 25 so that the serial port is for the new SPIKE Prime (Open up a new terminal window and type `cd /dev/tty.` and hit tab a couple of times to find the new serial port)
  * When we finish typing the updated serial port, we can go into the `index.js` file within this same folder
  * Here we need to edit lines 6-8
    * Line 6 should be called `Spike2` (again increment the number based on the number of SPIKE's)
    * Line 7 should be the new name of the folder that you made within `spatialToolbox` (see <b>Step 1</b> above)
    * Line 8 should have the same name as Line 6

  ### Step 5: Starting the Server ###
  * Finally, we can save everything and start the server. If all the steps have been followed, it should start working! 
  * <b> Note: </b> Sometimes the SPIKE needs to be connected a few times to make and establish the connection. See our YouTube playlist above for more information. 

</details>
<details>
<summary><b>Python Script</b></summary>
<br>
First clone this repository onto your Raspberry Pi using the following command
<br>
    <code>
        git clone https://github.com/paccionesawyer/vuforia-spatial-RPI-SPIKE-Bluetooth.git
    </code>
<br>
Then if you would like to add a Spike Prime, turn it on and press the bluetooth button. Once it is blinking run the following command in the cloned repository. <br>
    <code>
        python3 setup_bluetooth.py
    </code>
<br>
The built in command-line user-interface will take you through the rest of the setup. (If you would like to use it you must bind your device everytime you restart your Pi)
Once the setup is done, all you need to do is start the Edge Server like normal, and set an image target.
</details>
