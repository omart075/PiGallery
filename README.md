# PiGallery

PiGallery is an interpretation of the [Pepper's Ghost illusion](https://en.wikipedia.org/wiki/Pepper%27s_ghost) built with Python, React, and a Leap motion controller 2. Users can use hand gestures to interact with a gallery of images/GIFs that are projected from a screen onto a piece of glass or any transparent film/material.

The original implementation was built with Python and Tkinter (Python_v1). The most up to date version of the UI is in the React_v2 directory.

The most up to date version of the Leap controller code can be found in Python_v1 > leap > gestures.py

# Gestures

There are two types of gestures that allow users to interact with the illusion (both hands supported):

#### Static Gestures
These gestures are only processed within a specific horizontal range (-60, 60). This is to avoid confusion with dynamic gestures. 
 
 - **Fist**: close hand into a fist
	 - toggle between random image mode (automatically changes the image every 5 secs) or stationary mode (stays on current image)
 - **Pinch**: bring index finger and thumb together
	 - toggle between gallery and interactive particle mode

#### Dynamic Gestures
These gestures must start outside of the static gesture threshold and within the specified tracking threshold for each axis (-200, 200), but once initiated, they persist everywhere until the gesture ends.

 - **Fist and drag**: make and hold a fist as you move your hand left to right (backward swipe) or right to left (forward swipe) then opening your hand to trigger the end of the gesture
	 - forward swipe: must start within range (100, 200) and end (-100, -200)
	 - backward swipe: must start within range (-100, -200) and end (100, 200)

## Particle Mode
This is an interactive mode built with [tsparticles](https://github.com/tsparticles/react). After completing a static pinch gesture, the user will be put into this mode and will be able to freely move their hand to create moving particles.


## Installation

#### Python
- `pip install pyautogui`
- `pip install pynput`
- Follow steps for [leapc python bindings](https://github.com/ultraleap/leapc-python-bindings)

#### React
- `npm v9.2.0`
- `node v18.9.0`
- Follow steps for [tsparticles](https://github.com/tsparticles/react)

NOTE: If you encounter animation loop errors, [try this fix](https://stackoverflow.com/questions/77705733/react-tsparticleserror-in-animation-loop).

#### Display
The display used was the [Waveshare 5.5 AMOLED display](https://www.waveshare.com/5.5inch-HDMI-AMOLED.htm) but any display works. This display was chosen because OLED/AMOLED displays provide true blacks. This helps the illusion significantly.
 
If your OS uses the Wayland display server protocol, pyautogui might not work as expected. If that's the case, you will have to either
- use another library to control the mouse
- change to the X11 display server protocol ([example for RPi 64 bit](https://raspberrypi.stackexchange.com/questions/144866/can-i-use-x11-on-the-new-64-bit-os-instead-of-wayland)) 

## Run
- start libtrack_server for Leap controller
	- `sudo systemctl start libtrack_server`
- start gesture tracking (from a venv or wherever you installed leapc python bindings)
	- `python gestures.py`
- start UI (from React_v2/pi-gallery)
	- `npm start`