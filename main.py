import pandas as pd
import json


#make sure that the headers are called "QUESTION" and "ANSWER"
#make sure that you have one row for questions and answers
data = pd.read_csv("Vragen CSS.csv")
# print(data.head(5))

correct = {}
wrong = {}
for i in range(0,data.shape[0]):
    print(f"\n{data['QUESTION'][i]}")
    a = input("\tShow answer (a) or quit(q): ")
    if a == "a":
        print(f"\t{data['ANSWER'][i]}")
    if a == "q":
        break

    x = input("\tDid you get this correct (y/n): ")
    if x == "y":
        correct[data['QUESTION'][i]] = data['ANSWER'][i]
    if x == "n":
        wrong[data['QUESTION'][i]] = data['ANSWER'][i]


print("====== DONE ========")
x = input("Do you want to practice your mistakes (y/n): ")

if x == "y":
    correct2 = {}
    wrong2 = {}

    for question, answer in wrong.items():
        print(f"\n{question}")
        a = input("\tShow answer (a) or quit(q): ")
        if a == "a":
            print(f"\t{answer}")
        if a == "q":
            break
        x = input("\tDid you get this correct (y/n): ")
        if x == "y":
            correct2[data['QUESTION'][i]] = data['ANSWER'][i]
        if x == "n":
            wrong2[data['QUESTION'][i]] = data['ANSWER'][i]
elif x == "n":
    pass

print("====== RESULTS FIRST ROUND ========")
print(correct)
print(wrong)
try:
    print("====== RESULTS SECOND ROUND ========")
    print(correct2)
    print(wrong2)
except NameError:
    pass