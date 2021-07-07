# vuforia-spatial-RPI-SPIKE-Bluetooth
Code to connect a Spike Prime to a Vuforia-Spatial-Edge-Server on a Raspberry Pi 


<details>
<summary><b>DIY</b></summary>
<br>
You can set this up with the following series of commands.


    sudo npm install -g pm2
    sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi
    pm2 start home/pi/vuforia-spatial-edge-server/server.js
    pm2 save

</details>

<details>
<summary><b>Python Script</b></summary>
<br>
First clone this repository onto your Raspberry Pi using the following command
<code>git clone</code>
</details>
