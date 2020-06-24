# LEDServer
Server for controlling led strip with a raspberry pi. Uses a WebInterface to control the lights. 

To setup the server change the Config.py dictionary. The data you see in it now is how I set up my lights at home, take that as an example.

The server is written and running in Python 3.5.3. I use the Flask framework as server and for my website templates I created HTML files with Jinja, this makes sure the webpage is adjustable and changes with the code. Adding functions is done by adding them to the dictionary in init method of the class in the LED.py file.

For LED strip I used an APA102 powered led strip. I have 135 leds but this is also variable. I also use an arduino with a second ledstrip, this one works via serial connection. Last but not least I also have ESP01 powered wifi connected lights. These are contacted via the IP adress they have. Some testing is still required to see what network load this will create and if that's a problem.

The code is still under production, even though I don't have much time at the moment, so it will not be the neatest code you will ever encounter. I'm still learning python and good coding habits, so it will become better. Keep in mind I'm a self teached hobbyist and by no means a proffesional programmer or computer science student. Tips, improvements and feature requests are welcome!

Defenitions:
  - Alarm.py - Defines class and helper functions for setting an Alarm on the lights.
  - Config.py - In this file all the Rooms and lights are defined. This is, as the name suggests, the config file.
  - Database.py - Defines class and helper functions for the Databases(In my case Temp, Humidity and light intensity for example)
  - Error.py - Work in progress, the idea is to make a system to Log everything in a database and show this on the website.
  - LED.py - In this file all functions for LED lights are defined. If you want to program a new sort of light(maybe bluetooth ro zigbee) you need to do it in this file.
  - Main.py - Controls the whole program and starts everything up, this is the file you want to run.
  - RitRegistration.py - Defines the class for the rit registration on the site, also calculates avg mileage.
  - WorkerFunctions - Defines the functions for the threads.
  - data.py - Defines the class 'room'
  - Website
    - WEB.py - Defines all the handles for the website, this is the server.
    - static
      - functions.js - All javascript functions for the website.

<img src=./Pictures/Website1.png>
<img src=./Pictures/Website2.png>
