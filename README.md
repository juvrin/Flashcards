# Flashcards App

Flashcards App does what it says on the tin: it's an app that creates flashcards for you.
There are two versions of this app: one simple terminal version (main.py)
and one with a graphical user interface (flashcards.py). Both will be described below.

<img src="/flashcards.png" alt="Screenshot of flashcards app" width="162" height="197">

## Getting started - both versions

First create a list of questions and answers in a program like LibreOffice Calc, Excel, Google Sheets, etc. On the top row, put "QUESTION" in the first column
and "ANSWER" in the second. Optionally, you can include a third column named "TOPIC" to keep track of the topic to which each question belongs. Export this file to .csv. Make sure that your questions and answers are on the same row, but in separate columns. Download one or both .py files to your computer and pip install the necessary dependencies in a virtual environment.

## Terminal version (main.py)

This is a simple terminal flashcards app. The .csv file is used as input and you can 
go through the flashcards in the terminal. Questions that you got wrong are stored in 
a dictionary. After all questions have been answered, you can practice just the questions you got wrong in a second round. Results are written to a .csv file. These include 
the date and how many you got correct and wrong in each round.

## GUI version (flashcards.py)

When running this script, you first get a screen where you can enter your input- and outputfiles. Additionally, you can choose to only practice what you got wrong last time (stored in a JSON file) and you can opt to shuffle the cards (randomize the order of the questions). Keyboard shortcuts are added so you can go through the cards more quickly. Results are written to a .csv. These include the date, percentage correct, if you were practising everything or only the ones you got wrong last time, how many questions you got correct and how many wrong, the number of questions, and which topics were covered (if included in the third column in the input.csv). Additionally, questions that were answered incorrectly are written to a json file for practice later on. 

## Background

I created these apps because I couldn't find a decent, free tool to quickly generate flashcards. Additionally, I wanted to keep track of my results and have extra functionalities like practicing questions that I got wrong.


## How It's Made

The second app with the GUI was created with Tkinter Python 3.13.7.


## Roadmap

- Add checks on inputfiles to make sure these exist before proceeding.

- Change layout of introscreen.

- Keep track of progress per question (i.e. log per question if it was answered correctly/incorrectly and when).



## Contact

Jules Vrinten https://www.linkedin.com/in/jules-vrinten/ 
https://github.com/juvrin ~


## License

[MIT](https://choosealicense.com/licenses/mit/)