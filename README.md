# RaspberryPi-SpatialToolbox-BluetoothLegoSpikePrime
Code to connect a Spike Prime to a Vuforia-Spatial-Edge-Server on a Raspberry Pi 

<details>
<summary><b>DIY</b></summary>
<br>

</details>

<details>
<summary><b>Python Script</b></summary>
<br>
First clone this repository onto your Raspberry Pi using the following command
<br>
    <code>
        git clone https://github.com/paccionesawyer/vuforia-spatial-RPI-SPIKE-Bluetooth.git
    </code>
Then if you would like to add a Spike Prime, turn it on and press the bluetooth button. Once it is blinking run the following command in the cloned repository.
    <code>
        python3 setup_bluetooth.py
    </code>
The built in command-line user-interface will take you through the rest of the setup. (If you would like to use it you must bind your device everytime you restart your Pi)
Once the setup is done, all you need to do is start the Edge Server like normal, and set an image target.
</details>
