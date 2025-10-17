import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import sys
import datetime
import os.path
import json

""""
MOETNOG:
- topics anders laten wegschrijven naar .csv en die aparte functie waarbij je het apart inlaadt is niet nodig

===== evt ====
- vervolgens toevoegen aan homescreen dat je ofwel de vragenlijst.json doorneemt ofwel de vorig_keer_fout.json
=> door dit als eerste vraag toe te voegen als question text 
bv "wil je je fouten van vorige keer oefenen? correct = ja, wrong = nee, alles opnieuw doen)"
"""
# Adapted version from https://medium.com/@arunabh223/how-i-prepare-for-exams-by-creating-flashcards-using-python-6db823b74083 

# Path to your csv file
file_path = 'Vragen CSS_fortesting.csv'
outputfile = "Results_fortesting.csv"
outputfile_wrong = 'Wrong_last_time_fortesting.json'
random_option = 'n'
practice_wrong = 'y'

def load_flashcards(file_path):
    """Load flashcards from csv file"""
    df = pd.read_csv(file_path)
    dict_list = df.to_dict('records')
    return dict_list
    
def load_wrongs(outputfile_wrong):
    """Load questions wrongly answered in previous session from json file"""
    with open(outputfile_wrong, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Load flashcards
flashcards = load_flashcards(file_path)
try:
    wrong_last_time = load_wrongs(outputfile_wrong)
except FileNotFoundError:
    pass

class FlashcardApp:
    def __init__(self, master):

        # Initialize screen
        self.master = master
        master.title("Flashcard App")
        master.geometry("500x500")  # Set a fixed window size

        # Add a progress bar
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(master, variable = self.progress_var,
                                           maximum=100)
        self.progressbar.place(x=30, y=30, height=250)
        self.progressbar.pack(padx=20, pady=20, fill="x")

        self.question_label = tk.Label(master, text="", font=("Helvetica", 16), wraplength=400)
        self.question_label.pack(pady=5)

        self.reveal_button = tk.Button(master, text="reveal answer", command = self.reveal_answer, underline=7)
        self.reveal_button.pack()
        
        self.quit_button = tk.Button(master, text='quit', command=self.destroy, underline=0)
        self.quit_button.pack(pady=5)

        self.answer_label = tk.Label(master, text="", font=("Helvetica", 16), wraplength=400)
        self.answer_label.pack(pady=5)
        
        self.countcorrect = 0
        self.correct_button = tk.Button(master, text="correct", command = self.correct, underline=0)
        self.correct_button.pack(pady=5)

        self.countwrong = 0
        self.wrong_button = tk.Button(master, text="wrong", command = self.wrong, underline=0)
        self.wrong_button.pack()

        # Optional next button
        # self.next_button = tk.Button(master, text="Next", command=self.next_flashcard)
        # self.next_button.pack()

        # Add keyboard shortcuts
        master.bind('a', self.reveal_answer)
        master.bind('q', self.destroy)
        master.bind('c', self.correct)
        master.bind('w', self.wrong)

        # Initialize empty lists for keeping correct and wrong items in
        self.correct = []
        self.wrong = []
        self.roundn = 1
        self.final_wrong = 0

        # Initialize flashcards
        if practice_wrong == 'n':
            self.flashcards = flashcards
        if practice_wrong == 'y':
            self.flashcards = wrong_last_time

        if random_option == 'y':
            random.shuffle(self.flashcards)

        self.current_flashcard_index = -1
        self.current_wrong_index = -1
        self.next_flashcard()

    def next_flashcard(self):
        self.answer_label.config(text="")
        self.current_flashcard_index += 1
        self.percentage_correct = (self.countcorrect / len(self.flashcards))*100

        if self.current_flashcard_index == len(self.flashcards):
            self.destroy()
        else:
            self.dict = self.flashcards[self.current_flashcard_index]
            self.current_question = self.dict['QUESTION']
            self.current_answer = self.dict['ANSWER']
            self.current_topic = self.dict['TOPIC']
            self.question_label.config(text=self.current_question)
        self.update_progress()
        
    def reveal_answer(self, event=None):
        self.answer_label.config(text=self.current_answer)
    
    def correct(self, event=None):
        self.countcorrect += 1
        if self.roundn == 1:
            self.correct.append(self.flashcards[self.current_flashcard_index])
        if self.roundn == 2:
            self.correct.append(self.wrong[self.current_wrong_index])
        self.next_flashcard()

    def wrong(self, event=None):
        self.countwrong += 1
        if self.roundn == 1:
            self.wrong.append(self.flashcards[self.current_flashcard_index])
            self.final_wrong = len(self.wrong)
        if self.roundn == 2:
            self.wrong.append(self.wrong[self.current_wrong_index])
        self.next_flashcard()
     
    def destroy(self, event=None):
        self.write_to_csv()
        sys.exit(0)
    
    def update_progress(self):
        self.new_value = self.progress_var.get()
        self.new_value += 100 / len(self.flashcards)
        if self.new_value > 100:
            self.new_value = 0
        self.progress_var.set(self.new_value)
        self.progressbar["value"] = self.new_value
    
    def write_to_csv(self):
        """Write results to csv"""
        date = datetime.datetime.now()
        results = f"{date.strftime("%d/%m/%Y %H:%M")},practice wrong? {practice_wrong},{self.countcorrect},{self.countwrong}, {int(self.percentage_correct)}, {len(self.flashcards)}\n"
        file = os.path.isfile(outputfile)
        if file:
            with open(outputfile,'a') as fd:
                fd.write(results)
        else:
            with open(outputfile,'w') as fd:
                fd.write("Date, Roundn, Correct, Wrong, Percentage correct, Number of questions, Topics \n")
                fd.write(results)
        
        # Write wrong to json to enable practice later
        with open(outputfile_wrong, "w") as final:
            json.dump(self.wrong, final, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))    

        
root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()