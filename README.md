# LEDServer
New server for controlling ledstrip lights, added funtionality and better code. Also easier for expansion



Server for controlling apa102 led strip with a raspberry pi. Comes with included website and rest API handles for android app. I am planning on building the app in the future. If someone wants to build an android app feel free to contact me for questions of the inner workings of the server and let me now if you made an app!

The server is written and running in Python 3.5.3. I use the Flask framework as server and for my website templates I created HTML files with Jinja, this makes sure the webpage is adjustable and changes with the code. Adding functions is done by adding them to the dictionary in init mode of the class in the LED.py file.

For LED strip I used an APA102 powered led strip. I have 135 leds but this is also variable. I also use an arduino with a second ledstrip, this one works via serial connection. The plan is to also build wifi enabled lights and implement these also. But for now I do not have the need for these in my home so this is for the long run

The code is still under production, even though I don't have much time at the moment, so it will not be the neatest code you will ever encounter. I'm still learning python and good coding habits, so it will become better. Keep in mind I'm a self teached hobbyist and by no means a proffesional programmer or computer science student. Tips, improvements and feature requests are welcome!
