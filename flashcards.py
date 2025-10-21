import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import sys
import datetime
import os.path
import json

# Adapted version from https://medium.com/@arunabh223/how-i-prepare-for-exams-by-creating-flashcards-using-python-6db823b74083 

# Give name of output json file 
outputfile_wrong = 'Wrong_last_time_fortesting.json'

class FlashcardApp:
    def __init__(self, master):

        # Initialize screen
        self.master = master
        master.title("Flashcard App")
        master.geometry("500x500")  # Set a fixed window size

        # Initialize intro screen
        self.input_label = tk.Label(master, text="Inputfile", font=("Helvetica", 16), wraplength=400)
        self.input_label.pack(pady=5)
        self.inputfile = tk.Entry(master)
        self.inputfile.pack(pady=5)

        self.outputfile_label = tk.Label(master, text="Outputfile csv", font=("Helvetica", 16), wraplength=400)
        self.outputfile_label.pack(pady=5)
        self.outputfile = tk.Entry(master)
        self.outputfile.pack(pady=5)

        self.random_label = tk.Label(master, text="Do you want to shuffle the cards?", font=("Helvetica", 16), wraplength=400)
        self.random_label.pack(pady=5)
        self.random_option = tk.StringVar()
        self.random_button_yes = tk.Radiobutton(master, text = "Yes", variable = self.random_option, value = "y")
        self.random_button_yes.pack(pady = 5) 
        self.random_button_no = tk.Radiobutton(master, text = "No", variable = self.random_option, value = "n")
        self.random_button_no.pack(pady = 5) 

        self.practice_wrong_label = tk.Label(master, text="Do you want to practice wrong questions from last time?", font=("Helvetica", 16), wraplength=400)
        self.practice_wrong_label.pack(pady=5)
        self.practice_wrong = tk.StringVar()
        self.practice_wrong_yes = tk.Radiobutton(master, text = "Yes", variable = self.practice_wrong, value = "y")
        self.practice_wrong_yes.pack(pady = 5) 
        self.practice_wrong_no = tk.Radiobutton(master, text = "No", variable = self.practice_wrong, value = "n")
        self.practice_wrong_no.pack(pady = 5) 

        # Next button
        self.next_button = tk.Button(master, text="Next", command=self.startup)
        self.next_button.pack()
    
    def load_flashcards(self, file_path):
        """Load flashcards from csv file"""
        df = pd.read_csv(file_path)
        dict_list = df.to_dict('records')
        return dict_list

    def load_wrongs(self, outputfile_wrong):
        """Load questions wrongly answered in previous session from json file"""
        with open(outputfile_wrong, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def startup(self):
        # Get values of outputfile path and inputfile path
        self.outputfile_var = self.outputfile.get()
        file_path = self.inputfile.get()

        # Hide all buttons and label from mainscreen
        self.input_label.pack_forget()
        self.inputfile.pack_forget()
        self.outputfile_label.pack_forget()
        self.outputfile.pack_forget()
        self.random_label.pack_forget()
        self.random_button_yes.pack_forget()
        self.random_button_no.pack_forget()
        self.practice_wrong_label.pack_forget()
        self.practice_wrong_yes.pack_forget()
        self.practice_wrong_no.pack_forget()
        self.next_button.pack_forget()
        
        try:
            wrong_last_time = self.load_wrongs(outputfile_wrong)
        except FileNotFoundError:
            pass

        try:
            flashcards = self.load_flashcards(file_path)
        except FileNotFoundError:
            pass

        # Add a progress bar
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self.master, variable = self.progress_var,
                                           maximum=100)
        self.progressbar.place(x=30, y=30, height=250)
        self.progressbar.pack(padx=20, pady=20, fill="x")

        self.question_label = tk.Label(self.master, text="", font=("Helvetica", 16), wraplength=400)
        self.question_label.pack(pady=5)

        self.reveal_button = tk.Button(self.master, text="reveal answer", command = self.reveal_answer, underline=7)
        self.reveal_button.pack()
        
        self.quit_button = tk.Button(self.master, text='quit', command=self.destroy, underline=0)
        self.quit_button.pack(pady=5)

        self.answer_label = tk.Label(self.master, text="", font=("Helvetica", 16), wraplength=400)
        self.answer_label.pack(pady=5)
        
        self.countcorrect = 0
        self.correct_button = tk.Button(self.master, text="correct", command = self.correct, underline=0)
        self.correct_button.pack(pady=5)

        self.countwrong = 0
        self.wrong_button = tk.Button(self.master, text="wrong", command = self.wrong, underline=0)
        self.wrong_button.pack()

        # Add keyboard shortcuts
        self.master.bind('a', self.reveal_answer)
        self.master.bind('A', self.reveal_answer)
        self.master.bind('q', self.destroy)
        self.master.bind('Q', self.destroy)
        self.master.bind('c', self.correct)
        self.master.bind('C', self.correct)
        self.master.bind('w', self.wrong)
        self.master.bind('W', self.wrong)

        # Initialize empty lists for storing correct and wrong items
        self.correct = []
        self.wrong = []
        self.topic = []

        # Initialize flashcards
        if self.practice_wrong.get() == 'n':
            self.flashcards = flashcards
        if self.practice_wrong.get() == 'y':
            self.flashcards = wrong_last_time

        if self.random_option.get() == 'y':
            random.shuffle(self.flashcards)

        self.current_flashcard_index = -1
        self.current_wrong_index = -1
        self.next_flashcard()

    def next_flashcard(self):
        self.answer_label.config(text="")
        self.current_flashcard_index += 1
        
        if self.current_flashcard_index == len(self.flashcards):
            self.destroy()
        else:
            self.dict = self.flashcards[self.current_flashcard_index]
            self.current_question = self.dict['QUESTION']
            self.current_answer = self.dict['ANSWER']
            self.topic.append(self.dict['TOPIC'])
            self.question_label.config(text=self.current_question)
        self.update_progress()
        
    def reveal_answer(self, event=None):
        self.answer_label.config(text=self.current_answer)
    
    def correct(self, event=None):
        self.countcorrect += 1
        self.correct.append(self.flashcards[self.current_flashcard_index])
        self.next_flashcard()

    def wrong(self, event=None):
        self.countwrong += 1
        self.wrong.append(self.flashcards[self.current_flashcard_index])
        self.next_flashcard()
     
    def destroy(self, event=None):
        self.write_to_csv()
        sys.exit(0)
    
    def update_progress(self):
        self.new_value = self.progress_var.get()
        self.new_value += 100 / len(self.flashcards)
        self.progress_var.set(self.new_value)
        self.progressbar["value"] = self.new_value
    
    def remove_duplicates_topic(self):
        self.topic_undup = []
        [self.topic_undup.append(val) for val in self.topic if val not in self.topic_undup]
        return self.topic_undup
    
    def write_to_csv(self):
        """Write results to csv"""
        self.remove_duplicates_topic()
        date = datetime.datetime.now()
        try:
            self.percentage_correct = (self.countcorrect / self.current_flashcard_index)*100
        except ZeroDivisionError:
            results = f"{date.strftime("%d/%m/%Y %H:%M")},{self.practice_wrong.get() },{self.countcorrect},{self.countwrong}, x, {self.current_flashcard_index}, {self.topic_undup}\n"
            pass
        else:
            results = f"{date.strftime("%d/%m/%Y %H:%M")},{self.practice_wrong.get() },{self.countcorrect},{self.countwrong}, {int(self.percentage_correct)}, {self.current_flashcard_index}, {self.topic_undup}\n"
        
        
        file = os.path.isfile(self.outputfile_var)
        if file:
            with open(self.outputfile_var,'a') as fd:
                fd.write(results)
        else:
            with open(self.outputfile_var,'w') as fd:
                fd.write("Date, Practice wrong?, Correct, Wrong, Percentage correct, Number of questions, Topics \n")
                fd.write(results)
        
        # Write wrong to json to enable practice later
        with open(outputfile_wrong, "w") as final:
            json.dump(self.wrong, final, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))    



root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()