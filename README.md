# SuDoKu-Solver
This project lets you solve a SuDoKu Puzzle, which you can enter manually into the GUI or load from an image.

## Getting Started
Download all the files from this repository.
Install all the necessary pre requisites.
Run SuDoKuGUI_v2.py

## Sample Operations
The GUI:
<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr1.png"><br>
</div>

You enter your own puzzle into the grids:

<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr2.png"><br>
</div>

Then press correct to finalize it:

<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr3.png"><br>
</div>

Or You can press load to load an image into the GUI.
<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr4.png"><br>
</div>

The program reads from the image and loads into the puzzle.
<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr5.png"><br>
</div>

Press solve to solve it using the program.

<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr6.png"><br>
</div>

If any of the digits are not recognized properly, rectify it, press correct and then click on teach to update the model.
<div align="center">
<img src="https://github.com/REXJJ/SuDoKu-Solver/blob/master/ScreenShots/scr7.png"><br>
</div>

Files
-----
Filename | Description 
----------|------------
/SuDoKuGUI_v2.py| the main file containing the GUI and other functions.
/imageprocessing.py| file containing functions for processing the sudoku image. 
/backtrack.py| the file containing methods to solve a sudoku.
/digitidentifier.py| contains methods for identifying a digit from its image.
/digitrecognition.py| Extracts data from images for image recognition training.
/generalresponses.data| Contains the data for image recognition training.
/generalsamples.data| Contains the data extracted from images for digit recognition training.
/images| contains sample images.
/Readme.md| the README file

## Pre Requisites
- OpenCV for python3
- numpy
- scipy
- griddata

## Author
Rex Jomy Joseph
