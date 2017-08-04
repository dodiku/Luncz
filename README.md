![https://www.google.com/maps/place/Lunz+St,+Tel+Aviv-Yafo,+Israel/@32.069799,34.777932,17z/data=!3m1!4b1!4m5!3m4!1s0x151d4b78cc31b63d:0xec091a05e60cc219!8m2!3d32.069799!4d34.780126](https://upload.wikimedia.org/wikipedia/commons/8/8e/%D7%90%D7%91%D7%A8%D7%94%D7%9D_%D7%9E%D7%A9%D7%94_%D7%9C%D7%95%D7%A0%D7%A5.jpg)  

# LUNCZ: PLAYING DATA
Final Project by Dror Ayalon  
Course: Software Synthesis   
Lecturer: Jean-Luc Cohen  
December 22nd, 2016  

### OVERVIEW: MUSIC AS A TOOL
“Luncz: Playing Data” was my first attempt to generate audio related data from an analog  recording, and to use this data to play new music.  
The purpose of this project was to build a tool (or an installation) that will create an endless conversation between a musician and a machine. The software allows musicians to record short snippets of music, and uses these recordings to change the background music in the room. The recorded music is being analyzed, and using the result of the audio analysis, beats and changes in timbre are being introduced on the background music.  
The background music was not designed for listening. Instead, the background music was designed to support the musician, and to leave room for further playing and recording.  

### HOW TO PLAY: INSTRUCTIONS
Luncz is being run by two Python scripts:  

1. '``input.py``' - Responsible for recoding live music using PyAudio, analyzing the recording using librosa, and dumping a WAV file with the recorded audio, a TXT file with the estimated tempo of the recording, and a CSV file with the beats onset data.
2. '``output.py``' - Responsible for initiating Csound (‘Luncz.csd’), collecting the files, reading the data, and sending score events to the Csound engine using Csound’s the Python API and ctcsound, a Python wrapper for the C Csound API.  


**The following steps should be taken in order to experience Luncz:**  


1. If you don’t have Homebrew installed, please open terminal and run:   
``$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" ``  

1. If you don’t have portaudio installed, please run the following command on your terminal:   
``$ brew install portaudio ``

1. While on the project main directory, using virtualenv, create a virtual environment for the project:   
``$ virtualenv env ``

1. While on the project main directory, activate your virtual environment by running :   
``$ source env/bin/activate``

1. While on the project main directory, install Python dependencies - Using virtualenv, install the dependencies specified in ‘requirements.txt’. Run:   
``$ pip install -r requirements.txt ``

1. Add ‘ctcsound’ to you site packages:
	- Copy ``ctcsound.py`` and ``csoundSession.py`` files from the ``ctcsound`` folder.
	- Paste the files on ``<project_main_folder>/env/lib/python2.7/site-packages ``.

1. While on the project main directory, run ``output.py`` to start the background music:   
``$ python output.py ``

1. Open a new terminal window, and go to the project main folder. While on the project main directory, run ``input.py`` to record analog audio signal:   
``$ python input.py ``

1. Hear the background music changes based on the analysis of the recorded audio.

1. Repeat step 3 as many times as you like.



##### TROUBLESHOOTING
In case where you’re getting the following error:   
``RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are Working with Matplotlib in a virtual enviroment see 'Working with Matplotlib in Virtual environments' in the Matplotlib FAQ.``  

Do the following actions:   
- In you terminal, type:   
``$ nano matplotlibrc ``  

- Add the following line to the matplotlibrc file:   
``$ backend: TkAgg``  

Thanks to [Hercules](http://stackoverflow.com/users/3614839/hercules) for his useful answer on [Stackoverflow](http://stackoverflow.com/questions/29433824/unable-to-import-matplotlib-pyplot-as-plt-in-virtualenv).





