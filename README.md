Planetary
=========

Solar system game for the XO PC. Teaches kids about the arrangment of the solar system, and about the planets themselves. Since the fourth grade science curriculum requires students to know basic astronomical facts, this game helps teach those facts in an interactive way.

###Requirements
	Python 2.7
	Pygame

How to Run
=========
There are multiple ways to play Planetary. The game can be played as a standalone pygame app, or as an activity on an XO.


###Running as Pygame App
This game can be played as a desktop application. As long as python and pygame are installed, simply run Planetary.py to play and test. Please note, this method does NOT use any XO or sugargame components.


###Running on an XO
Get a flash drive (or USB volume of your choice), copy the Planetary-#.xo file into the root. Then, plug the drive into XO, and go to the journal. After a second or two, a small flash drive icon will appear in the lower left corner. Click this icon, and you will be presented with a file list. Simply click on the Planetary-#.xo file, and it will install and run.


Developers
==========
Developing is fairly straight-forward, since python files run as interpreted plaintext. The bigger challenge is testing and debugging. While the app can be run as a standalone pygame app, you will still need to test your code on an XO or an XO emulator. It is strongly recomended that you use a linux machine for this, since Sugar (the XO environment) is linux based (I used Ubuntu with no difficulties).

###Testing with an emulator
Testing on your local machine means you need to install the python-sugar3 library. Simply search for and install it from your local package repository. Now, for running Sugar itself, you could load up a virtual machine with Sugar on it, but using the sugar-emulator is much simpler, and much faster. It should be an available package with most linux distros. After installing sugar-emulator, you will need to run:

	./setup.py dev

This creates an Activities directory in your home folder (if there wasn't one already), and places a symbolic link inside that leads to the project's root folder. Once this is done, you can simply run:

	sugar-emulator -i 1200x900

This will launch the emulator. After picking your colored icon and whatnot, it will drop you off at the home screen (the Wheel of activities). To make Planetary show up in the wheel, click on the list icon in the upper right corner, scroll to Planetary, and click on the star. Now, if you go back to the wheel version of the home screen, the Planetary icon should appear.

Every time you run a version of an Activity on the XO, it stores both the app itself, and any progress/resume files to the journal. To delete an old version of the activity (as is neccessary in development), you must delete all of your activity's entries in the journal.

###Testing on an XO
To run the game on an XO, you will need to build an XO file. This is incredibly complicated. You will need to run:

	./build.sh

This will generate a *.xo file in your root folder, which you can run on an XO using the instructions in the How To Play section.


File Explanations
=================


###PlanetaryActivity.py (Entry point)
Wrapper to run pygame as an Activity on an XO. Handles basic sugar activity things, like the toolbar and read_file/write_file


###Planetary.py (Pygame App)
Handles primary game logic and UI. Manages the game state and data. Switches and interacts with screen objects


###PlanetaryScreens.py
Defines classes for the various screens in the game ("Home" and "Play" in this case). Each screen class manages its own sprites, and computes the changes from one frame to the next.


###PlanetarySprites.py
Defines individual sprites (ie. "Planet", "Background", "TextBox"). Sprites handle their own graphics internally, and contain functions and switches for the screen class to change.


###PlanetaryConstants.py
Game-wide constants and utility functions.


###init_data.json (question set / game state)
Written in JSON, questions are stored in one of two lists. "live" holds questions that are in play (that the user should be able to answer), and "wait" holds potential questions. Each question can have multiple answers. This file is only used for starting a game. Once a game is started and saved, the instance JSON (game state) is saved to the journal.

License
=======
Planetary source code is licensed under GPL v2. Artwork is licensed under [Creative Commons Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/legalcode).
