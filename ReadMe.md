# GOLF WIZARDS DOCUMENTATION

## Description

Two-dimensional golf game for competing “wizards” that are capable of earning magical power-ups throughout the course to gain advantages over their opponents.


## Table of Contents

1. [pyGame](#pyGame)
2. [OpenCV](#OpenCV)
3. [MQTT](#mqtt)
4. [Speech](#speech)

## pyGame

Our python game script serves as the central linker for all project components. 

<img width="300" alt="Screen Shot 2024-03-17 at 10 30 09 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/53343f65-7e6f-4c04-8d78-9d52ef812cb1">

To play the game, run the command:

```bash
python main.py
```
Testing:
Testing the python script is a constant process to make sure the graphic user interface is functioning properly.    

## OpenCV and Gesture Recognition

To run the gesture recognition seperate from the central gamescript, run the command: 

```bash
python app.py
```

For an in depth tutorial of how the source code works, please read the more detailed GESTUREREADME.md file in this repository. 

Testing and Integration:
Early stage testing promised stable gesture recognition.  
<img width="300" alt="Screen Shot 2024-03-17 at 10 40 05 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/dfd78fea-f1f4-481f-80ce-b2d79db0f448">
<img width="300" alt="Screen Shot 2024-03-17 at 10 40 33 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/f0728f65-d499-4017-9b28-134909302d20">

Occasionally, the recognizer will read an misinterpret input from a user but will quickly correct to the most likely gesture.  To prevent overguessing, the gamescript saves a gesture only after 10 gestures have been recorded by the recognizer.  

Hyper contrasted light settings also prove a challenge for the recognizer. Making sure the player is in a stable light environment could prove helpful for playability. The game does not continue without proper gesture input is the current state solution, where users are inclined to alter their gesture slightly until input is received.  

## MQTT
IMU and Microcontroller MQTT Linking
- IMUvelocitysending3_16.ino
- Velocity.py
  
Similar to Lab 3, we developed a line of MQTT communication to link the game with the MCU where we publish our swing data velocity to a topic that the pyGame is subscribed to.  The progress we have made thus far is a working model that calculates the maximum “velocity” in the swing after the angle is clicked in the game, achieved by getting the angular velocity (DPS) from the Gyroscope data from the IMU.

Testing:
WIFI Testing was critical in linking the IMU and Microcontroller to the central pygame script. 
Several tests were conducted to cpnnect the IMU and it was found that a personal hotspot was needed to circumnavigate UCLA's firewall.  Otherwise, for the game to function properly, wifi will have to be configured on a personal home network.

For the actual MQTT and IMU testing, velocity data was constantly being read about the IMU.  WHen a player is holding the IMU, the velocity data will hover around 0 DPS in terms of angular velocity.  Sometimes this value is negative. To get around this problem, the code was altered to record the max angular velocity and send this value to the pygame script to be processed.  As the game gets further along in development, it is crtiical to send a 0 callback back to the IMU.  That is, once the computer recieves a max velocity number, the max velocity will go back to zero.  Testing was done by recording output of the mqtt device and making sure linking was working properly in the certral pygame script.  The screenshots below are examples of MQTT output, and successful veloocity interpretation by the game script.  

<img width="200" alt="Screen Shot 2024-03-18 at 10 04 44 AM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/be7d6071-4a5c-449b-a168-0140b9f5ebc5">

<img width="200" alt="Screen Shot 2024-03-18 at 10 05 25 AM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/a3a79c0a-a7fe-46ac-b127-709e2ba9ca9c">

<img width="150" alt="Screen Shot 2024-03-18 at 10 15 03 AM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/26ba450e-cc0d-4fa3-85a8-00ea2b96fcb2">

<img width="150" alt="Screen Shot 2024-03-18 at 10 15 31 AM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/1a1acc17-873b-4972-9c09-2a0d97ba4d38">

The above screenshots show on the left, MQTT readout values, and on the right, successful linking to the python script. 

## Speech

Speech processing functions with google's speech recognition library.
Speech is fully integrated into the game and runs simply in speech.py.  
Below are screenshots of speech and gesture testing. 

<img width="200" alt="Screen Shot 2024-03-17 at 10 51 36 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/9725b321-1d10-40af-87f7-29faf9398782">
<img width="200" alt="Screen Shot 2024-03-17 at 10 52 29 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/fb91c1d1-2bb7-4f18-b65c-122ce28f8c4c">
<img width="200" alt="Screen Shot 2024-03-17 at 10 52 59 PM" src="https://github.com/ECE-180D-WS-2024/Team-4/assets/97809757/a666beb3-79b3-4930-a3da-2b247fc62f8c">

The above are screenshots of gesture and audio testing performed by our lab group.  More tests were ran than shown above.  From these tests, it was concluded that audio processing is optimal when the computer is searching for time limited phrases (under 4 seconds in length).  The consistency of successful input reading was vastly improved by this change in code.

Gesture recognition performed properly with minimal miscaptures of user input.  It might be helped to slightly increase the amount of successive gestures that need to be read to count as an ATTACK or DEFEND spell cast.  Additionally, user instruction at the beginning of the game should tell users to be mindful of their hands when casting spells (so as to not misgesture)  

Digest Stats:
Game runs with a 1.0 second MQTT delay when on a personal hotspot. With more testing, this is aimed to be optimized and reduced.
10 gestures are needed to be successfully recorded for the powerups to continue functioning.  This causes some game delay (dependent on user input ability), but stabilizes gameplay and gets more accurate readings of data.  
Audio processing looks for segments of audio which are less than 4 seconds in length.  This encourages short phrases and aids the program in searching for the correct phrase.  





