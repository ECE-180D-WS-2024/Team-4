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

INSERT DOCUMENTATION

INSERT IMAGES OF THE SCREEN

## Speech

INSERT DOCUMENTATION

INSERT IMAGES OF THE GAMEPLAYSCREEN

### Image 1

![Placeholder Image 1](./data/placeholder_image_1.png)

### Image 2

![Placeholder Image 2](./data/placeholder_image_2.png)

### Image 3

![Placeholder Image 3](./data/placeholder_image_3.png)


