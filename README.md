# NAO Planning AI
**Group name:** DanceExMachina

**Team Members:**

Sarra Ghali – sarra.ghali@studio.unibo.it

Annalisa Poluzzi – annalisa.poluzzi@studio.unibo.it

**Notes:**
- The project automatically plans a NAO choreography by inserting intermediate moves between mandatory moves while respecting a maximum duration of 120 seconds.
- The robot performs the planned moves and plays music concurrently.
- The audio file must be in WAV format (the file “levitating.wav” is included).
- All movement scripts are in the “RobotPositions” folder and are loaded dynamically.
- Settings like robot IP, port, and python path must be adjusted in config.yaml before running.
  
**How to run:**
- Start the simulated NAO robot in Choregraphe.
- Set correct IP, port number and pythonpath in config.yaml.
- Run the program using: `python2 main.py`
- The robot executes the full choreography and stops the music automatically at the end.
