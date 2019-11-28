# Setting up **Sentry Home**
## Our Hack:
1. Install and set up raspbian on a raspberry pi device. [Link](https://www.raspberrypi.org/documentation/installation/installing-images/)
1. Remove all unwanted software such as multiple IDEs, java, ruby, email client, emulators, etc and there dependencies.
1. Clone this repository into a folder in Raspbian.
1. Open the file *sources.list* (Ubuntu 19 sources) or *sources18.list* (Ubuntu 18 sources, *not tested but should work*) from the above repository and copy all the content.
1. Open */etc/apt/sources.list* as root and paste the copied content to the beginning of the file.
1. Also uncomment the last line of the file in line 5.
1. Run *sudo apt-get update*
1. Run *sudo apt-get source* (kind of optional)
1. Step 10 should upgrade python version to 3.7. If not, manually upgrade python to version 3.7 before step 10.
1. Install *python3-opencv* and *python3-numpy* from apt as pip3 install for these modules doesn’t work on ARM architecture.
1. Install/Update *python-pip* to version 3 (if required)
1. Install the dependencies *PiCamera, RPi.GPIO, firebase_admin* and *PyDub* from pip3.
1. Run *sentry.py* present in the repository just cloned.
1. Set up VNC viewer to listen to cloud networks to make it truly wireless (Optional)
1. Install the mobile app to control this remotely (Optional)
## A Better Approach (only 7 steps):
1. Install and set up Ubuntu 19.10 server on a raspberry pi device. [Link](https://ubuntu.com/download/raspberry-pi)
1. Install Raspbian Camera Kernel Modules (*Very Important Step. Can’t get this to work*)
1. Install/Update python to version 3.7 (if required)
1. Install/Update python-pip to version 3 (if required)
1. Install the dependencies *PiCamera, RPi.GPIO, firebase_admin* and *PyDub* from pip3.
1. Install *python3-opencv* and *python3-numpy* from apt as pip3 install for these modules doesn’t work on ARM architecture.
1. Clone this repository into a folder in Raspbian. 
1. Run *sentry.py* present in the repository just cloned.
1. Set up VNC viewer to listen to cloud networks to make it truly wireless (Optional)
1. Install the mobile app to control this remotely (Optional)
