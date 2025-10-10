import pandas as pd
from pathlib import Path
import datetime
import os.path


# Make sure that the headers are called "QUESTION" and "ANSWER"
# Make sure that you questions and answers are on the same row but in separate columns
data = pd.read_csv("Vragen CSS_fortesting.csv")
# print(data.head(5))

def printfunc(round, ncorrect, nwrong):
    if round == 1:
        print("====== RESULTS FIRST ROUND ========")
    else: 
        print("====== RESULTS SECOND ROUND ========")
    print(f"Correct: {ncorrect}")
    print(f"Wrong: {nwrong}")


correct = {}
wrong = {}
practice = True
while practice:
    for i in range(0,data.shape[0]):

        showanswer = True
        correctwrong = True

        while showanswer:
            print(f"\n{data['QUESTION'][i]}")
            a = input("\tShow answer (a) or quit (q): ")
            if a == "a":
                print(f"\t{data['ANSWER'][i]}")
                showanswer = False 
                break
            elif a == "q":
                showanswer = False 
                correctwrong = False
                practice = False
                break
            else:
                print("Please enter a or q.")
                showanswer = True
            
        while correctwrong:
            x = input("\tDid you get this correct (y/n) or quit (q): ")
            if x == "y":
                correct[data['QUESTION'][i]] = data['ANSWER'][i]
                correctwrong = False
                break
            elif x == "n":
                wrong[data['QUESTION'][i]] = data['ANSWER'][i]
                correctwrong = False
                break
            elif x == "q":
                showanswer = False 
                correctwrong = False
                practice = False
                break
        
        if a == "q" or x =="q":
            practice = False
            break
    printfunc(1, len(correct), len(wrong))          
    practice = False
          
    

print("====== FINISHED FIRST ROUND ========")


if len(wrong) > 0:
    x = input("Do you want to practice your mistakes (y/n): ")

    if x == "y":
        correct2 = {}
        wrong2 = {}
        practice = True
        while practice:
            for question, answer in wrong.items():

                showanswer = True
                correctwrong = True
                while showanswer:
                    print(f"\n{question}")
                    a = input("\tShow answer (a) or quit (q): ")
                    if a == "a":
                        print(f"\t{answer}")
                        showanswer = False 
                        break
                    elif a == "q":
                        showanswer = False 
                        correctwrong = False
                        practice = False
                        break
                    else:
                        print("Please enter a or q.")
                        showanswer = True
                    
                while correctwrong:
                    x = input("\tDid you get this correct (y/n) or quit (q): ")
                    if x == "y":
                        correct2[question] = answer
                        correctwrong = False
                        break
                    elif x == "n":
                        wrong2[question] = answer
                        correctwrong = False
                        break
                    elif x == "q":
                        showanswer = False 
                        correctwrong = False
                        practice = False
                        break
                
                if a == "q" or x =="q":
                    practice = False
                    break
            printfunc(2, len(correct2), len(wrong2))          
            practice = False

elif x == "n":
    pass

print("====== FINISHED SECOND ROUND ========")

# Write results to csv
date = datetime.datetime.now()
results = f"{date.strftime("%d/%m/%Y")},{len(correct)},{len(wrong)}\n"

file = os.path.isfile("results.csv")
if file:
    with open('results.csv','a') as fd:
        fd.write(results)
else:
    with open('results.csv','w') as fd:
        fd.write("Date, Correct, Wrong\n")
        fd.write(results)