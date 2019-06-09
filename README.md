# Step-Climbing-Robot-Robotica
Robotica was basically developed to be self navigating,responsive robot which could climb any type of staircase.
# Description
Basically the whole project idea can be divided into three Crucial tasks 
1. Autonomous Navigation,
2. Step climbing,
3. Voice Interaction 
The basic idea behind the project was to make a robot kinda like a  college mascot which would move autonomously around college and help freshers or anyone with common queries like where is the computer lab or something like that.   
### Navigation
 There are three ways in which anyone or for the matter of fact anything can move from one place to another,one is either he/she must have remembered the way(path) to the final point or he/she must have a map of some kind or there must direction signs(MARKS) showing them the  route to the destination.For this project I've opted with the third method (i.e) making my robot navigate from one place to other using direction signs(forward,left,right,stop).
 
 ### Step climbing
  We thought that a robot which could climb staircase would truly stick to theme of autonomous self navigation we had to go with step climbing mechanism.
	MECHANISM:
After detecting the upward direction sign the robot moves forward until the distance between the hind ultrasonic sensor and the first step is more than a consatant value(35.0 cm approx); then the two 30 rpm motors along with the MPU6050 gyroscopic sensor and the ultrasonic start the uplifting mechanism.
After the robot reaches the height of the first step the body of the robot moves forward and then the hind part of the robot unwinds up so that the whole  robot is now on the stair case completley.This action carries out until the robot detects that there are no more steps.

The main advantage of this motion is that the robot is not just bound to the similar steps  but can climb any type os steps irrespective of the dimensions of the staircase. 
	
	




### Component that I've used

 1. Raspberry pi 3B+;
 2. Raspberry Pi cam;
 3. Two 30 RPM Johnson Motors(for Uplifting motion of the robot);
 4. Four 100 RPM Johnson Motors are used for standard locomotion;
 5. ONe MPU6050 sensor for the stabilization of the whole system;
 6. Two ultrasonic sensors;
7. Lots of jumper wires(Male-male,female-female,male-female);
 8. 3d printed parts basically for the body of the robot;

