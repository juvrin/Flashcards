import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import sys
import datetime
import os.path

# Adapted version from https://medium.com/@arunabh223/how-i-prepare-for-exams-by-creating-flashcards-using-python-6db823b74083 

# Load flashcards from csv file
def load_flashcards(file_path):
    df = pd.read_csv(file_path)
    return dict(zip(df['QUESTION'], df['ANSWER']))

def load_topics(file_path):
    df_topics = pd.read_csv(file_path)
    df_topics_only = list(df_topics['TOPIC'])
    undup = []
    for i in df_topics_only:
        while i not in undup:
            undup.append(i)  
    return undup

# Path to your csv file
file_path = 'Vragen CSS_fortesting.csv'
outputfile = "Results.csv"
random_option = 'n'

# Load flashcards
flashcards = load_flashcards(file_path)
topics = load_topics(file_path)

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

        # Initialize flashcards by random shuffling them
        self.flashcard_list = list(flashcards.items())
        if random_option == 'y':
            random.shuffle(self.flashcard_list)
        self.current_flashcard_index = -1
        self.current_wrong_index = -1
        self.next_flashcard()

    def next_flashcard(self):
        self.answer_label.config(text="")
        self.current_flashcard_index += 1
        self.update_progress()

        if self.current_flashcard_index == len(self.flashcard_list):
            self.percentage_correct = (self.countcorrect / len(self.flashcard_list))*100
            self.write_to_csv()
        if self.current_flashcard_index >= len(self.flashcard_list):
            self.roundn = 2
            self.practice_wrongs()
        else:
            self.current_question, self.current_answer = self.flashcard_list[self.current_flashcard_index]
            self.question_label.config(text=self.current_question)

    def practice_wrongs(self):
        if self.current_wrong_index == -1:
            self.countcorrect = 0
            self.countwrong = 0
            self.progressbar.step(0)
        if random_option == 'y':
            random.shuffle(self.wrong)
        self.answer_label.config(text="")
        self.current_wrong_index += 1 
        self.update_progress()

        if self.current_wrong_index >= self.final_wrong:
            self.percentage_correct = (self.countcorrect / len(self.wrong))*100
            self.destroy()
        else:
            self.current_question, self.current_answer = self.wrong[self.current_wrong_index]
            self.question_label.config(text=self.current_question)
        
    def reveal_answer(self, event=None):
        self.answer_label.config(text=self.current_answer)
    
    def correct(self, event=None):
        self.countcorrect += 1
        if self.roundn == 1:
            self.correct.append(self.flashcard_list[self.current_flashcard_index])
        if self.roundn == 2:
            self.correct.append(self.wrong[self.current_wrong_index])
        self.next_flashcard()

    def wrong(self, event=None):
        self.countwrong += 1
        if self.roundn == 1:
            self.wrong.append(self.flashcard_list[self.current_flashcard_index])
            self.final_wrong = len(self.wrong)
        if self.roundn == 2:
            self.wrong.append(self.wrong[self.current_wrong_index])
        self.next_flashcard()
    
    def destroy(self, event=None):
        self.write_to_csv()
        sys.exit(0)
    
    def update_progress(self):
        self.new_value = self.progress_var.get()
        self.new_value += 100 / len(self.flashcard_list)
        if self.new_value > 100:
            self.new_value = 0
        self.progress_var.set(self.new_value)
        self.progressbar["value"] = self.new_value
    
    def write_to_csv(self):
        """Write results to csv"""
        date = datetime.datetime.now()
        results = f"{date.strftime("%d/%m/%Y %H:%M")},{self.roundn},{self.countcorrect},{self.countwrong}, {int(self.percentage_correct)}, {len(self.flashcard_list)}, {topics}\n"
        file = os.path.isfile(outputfile)
        if file:
            with open(outputfile,'a') as fd:
                fd.write(results)
        else:
            with open(outputfile,'w') as fd:
                fd.write("Date, Roundn, Correct, Wrong, Percentage correct, Number of questions, Topics \n")
                fd.write(results)

        
root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()