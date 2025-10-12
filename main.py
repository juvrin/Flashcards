import pandas as pd
from pathlib import Path
import datetime
import os.path
import sys

def read_data(inputfile):
    """Read data from csv"""
    data = pd.read_csv(inputfile)
    return data

def printfunc(round, ncorrect, nwrong):
    """Print results"""
    if round == 1:
        print("====== RESULTS FIRST ROUND ========")
    else: 
        print("====== RESULTS SECOND ROUND ========")
    print(f"Correct: {ncorrect}")
    print(f"Wrong: {nwrong}")

def round_one(data):
    """Practice round one"""
    correct = {}
    wrong = {}

    for i in range(0,data.shape[0]):

        showanswer = True
        correctwrong = True

        while showanswer:
            print(f"\n{data['QUESTION'][i]}")
            a = input("\tShow answer (a) or quit (q): ")
            if a == "q":
                sys.exit(0)
            if a == "a":
                print(f"\t{data['ANSWER'][i]}")
                showanswer = False 
                break
            else:
                print("Please enter a or q.")
                showanswer = True
            
        while correctwrong:
            x = input("\tDid you get this correct (y/n) or quit (q): ")
            if x == "q":
                sys.exit(0)
            if x == "y":
                correct[data['QUESTION'][i]] = data['ANSWER'][i]
                correctwrong = False
                break
            elif x == "n":
                wrong[data['QUESTION'][i]] = data['ANSWER'][i]
                correctwrong = False
                break
            
    printfunc(1, len(correct), len(wrong))          
    return (correct, wrong)
          
def round_two(wrong):
    """Practice round two"""
    correct2 = {}
    wrong2 = {}
   
    for question, answer in wrong.items():
        showanswer = True
        correctwrong = True
        while showanswer:
            print(f"\n{question}")
            a = input("\tShow answer (a) or quit (q): ")
            if a == "q":
                sys.exit(0)
            if a == "a":
                print(f"\t{answer}")
                showanswer = False 
                break
            else:
                print("Please enter a or q.")
                showanswer = True
            
        while correctwrong:
            x = input("\tDid you get this correct (y/n) or quit (q): ")
            if x == "q":
                sys.exit(0)
            if x == "y":
                correct2[question] = answer
                correctwrong = False
                break
            elif x == "n":
                wrong2[question] = answer
                correctwrong = False
                break
    
    printfunc(2, len(correct2), len(wrong2))          
    return(correct2, wrong2)
    
def write_to_csv(correct,wrong, outputfile):
    """Write results of first round to csv"""
    date = datetime.datetime.now()
    results = f"{date.strftime("%d/%m/%Y")},{len(correct)},{len(wrong)}\n"
    file = os.path.isfile(outputfile)
    if file:
        with open(outputfile,'a') as fd:
            fd.write(results)
    else:
        with open(outputfile,'w') as fd:
            fd.write("Date, Correct, Wrong\n")
            fd.write(results)

def main(inputfile, outputfile):
    """Main function"""
    data = read_data(inputfile)
    correct, wrong = round_one(data)
    print("====== FINISHED FIRST ROUND ========")

    if len(wrong) > 0:
        x = input("Do you want to practice your mistakes (y/n): ")
        if x == "y":
            correct2, wrong2 = round_two(wrong)
            print("====== FINISHED SECOND ROUND ========")
        else: 
            pass

    write_to_csv(correct, wrong, outputfile)

if __name__ == "__main__":
    # Make sure that the headers are called "QUESTION" and "ANSWER"
    # Make sure that you questions and answers are on the same row but in separate columns
    inputfile = "Vragen CSS_fortesting.csv"
    outputfile = "Results.csv"
    main(inputfile, outputfile)
