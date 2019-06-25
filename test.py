from Tkinter import *
import tkMessageBox
from firebase import firebase
from emv_interrogator import *
from emv_utils import*
import os
import hashlib

cardnum=""
i=0
billMoney = 0
billAm = 0

firebase = firebase.FirebaseApplication('https://cpename-6ddb5.firebaseio.com/', None)

gui = Tk()

gui.geometry("1280x980")
gui.title("cpeName")

def startProgram(eventName):
	global firebase
	main()
	idCard=retcardnum()
	#print idCard
	result = firebase.get('/IDs', idCard)
	#rint str(result["studentID"])

	studentID.config(state=NORMAL)
	studentID.delete('0', END)
	studentID.insert(END, str(result["studentID"]))
	studentID.config(state=DISABLED)

	studentName.config(state=NORMAL)
	studentName.delete('0', END)
	studentName.insert(END, str(result["Name"]))
	studentName.config(state=DISABLED)

	firebase.put('/Event/'+eventName, str(result["studentID"]), {"name": str(result["Name"])})

def CheckID():
	global firebase
	scanner1 = str(check.get())
	count=0
	checkar=[]
	eventlist=["Week_1", "Week_2", "Week_3", "Week_4", "Week_5"]
	
	for z in eventlist:
		Objectt = firebase.get('/Event/'+z, scanner1)
		if Objectt != None:
			count+=1
			checkar.append(z)
	listbox.delete(0, END)
	for m in checkar:
		listbox.insert(END, m)

	showCount.config(state=NORMAL)
	showCount.delete('0', END)
	showCount.insert(END, str(count))
	showCount.config(state=DISABLED)

check = Entry(gui)
check.place(x=900,y=350)

b0 = Button(gui, text="Scan", fg="#000", width=8, height=5,command=lambda: startProgram(var.get()))
b0.place(x=265,y=520)

b1 = Button(gui, text="Check", fg="#000", width=8, height=5,command=lambda: CheckID())
b1.place(x=930,y=400)

event1 = "Week_1"
event2 = "Week_2"
event3 = "Week_3"
event4 = "Week_4"
event5 = "Week_5"

var = StringVar(gui)
var.set(event1)

dropDownMenu = OptionMenu(gui,var, event1, event2, event3, event4, event5)
dropDownMenu.place(x=255,y=400)

studentID = Entry(gui)
studentID.insert(END, "stundentName")
studentID.config(state=DISABLED)
studentID.place(x=150,y=450)

studentName = Entry(gui)
studentName.insert(END, "studentName")
studentName.config(state=DISABLED)
studentName.place(x=300,y=450)

listbox = Listbox(gui, width=50, height=10, background="white", fg="black", selectbackground="blue")
listbox.place(x=815, y=500)

showCount = Entry(gui)
showCount.insert(END, "showCount")
showCount.config(state=DISABLED)
showCount.place(x=910,y=700)

gui.mainloop()
