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
global passHash
global e1
global e2
global e3
global firebase
global a
global billMoney
global billAm
global label2
global label3
firebase = firebase.FirebaseApplication('https://osss-e0b40.firebaseio.com/', None)
class App(Tk):
	global a
	global result
	
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		#Setup Menu
		MainMenu(self)
		#Setup Frame
		print "card : "+cardnum
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)


		self.frames = {}

		for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)	
	def show_frame(self, context):
		print context
		global e1
		global e2
		global passHash

		if str(context)=="__main__.PageOne":
			print "sdflsdkfsdlkfjdsflsdfkj"
			print context
			
			toHash=e1.get()
			print len(toHash)
			if toHash<6:
				self.show_frame(StartPage)

			passHash=hashlib.md5(toHash).hexdigest()
			print passHash
			e1.delete(0, END)
			
			
		# if str(context)=="__main__.PageTwo":
		frame = self.frames[context]
		frame.tkraise()
	def checkPage(self,context):
		to=e1.get()
		if len(to)<6 or to=="":
			tkMessageBox.showinfo("Error", "Wrong Password")
			print "error"
			
		else:
			self.show_frame(PageOne)
			print "show"
	def baseCheck(self, context ,money):
		global i
		global firebase
		global passHash
		global e2
		global e3
		global a
		global moneyto
		moneyto=money
		global resultto

		global label2
		global label3
		if i==1:
			toHash=e3.get()
			print len(toHash)
			passHash=hashlib.md5(toHash).hexdigest()
		e2.delete(0, END)
		main()
		a=retcardnum()
		a='/'+a
		# money=int(money)
		result = firebase.get(a+'/amount', None)
		resultPass = firebase.get(a+'/pass', None)
		if int(result)<money or money>25000 :
			tkMessageBox.showinfo("Error", "Wrong Amount")
		elif resultPass!=passHash:
			tkMessageBox.showinfo("Error", "Wrong Password")
			resultPass = firebase.get(a+'/pass', None)
			wrongPass = firebase.put(a[1:len(a)], "wrongPass",money)
			i+=1
			if i==3:
				i=0
				tkMessageBox.showinfo("Error", "You type wrong password three time. Please contact ...")
				self.show_frame(StartPage)
			else:
				self.show_frame(PageFour)
		elif money%100==0:
			ans=int(result)-money
			f = open('cash.txt','w')
			f.write(str(money)+'BATH\n')
			f.close()

			billMoney=money
			billAm=ans
			label2.config(text="Amount : "+str(billMoney))
			label3.config(text="Balance : "+str(billAm))
			print billMoney
			print billAm
			print "123sasdasdad213thnbv"
			# os.system("lpr -P printer_name cash.txt") #print out
			result = firebase.put(a,"amount",ans)
			result2 = firebase.put(a,"wrongPass",ans)
			wrongPass = firebase.put(a[1:len(a)], "wrongPass","")
			self.show_frame(PageThree)
			print result
			resultto=result
			print "aaaaaaaaaaaaaaaaaaaaaa"
	def billPage(self,context):
		global resultto
		global moneyto
		f = open('bill.txt','w')
		f.write(str(moneyto)+'BATH/n')
		f.write('Balance : '+str(resultto))
		f.close()
		# os.system("lpr -P printer_name cash.txt") #print out
	# def passCheck(self,context):
	# 	global firebase
	# 	global i
	# 	global passHash
	# 	global a
	# 	resultPass = firebase.get(a+'/pass', None)
		
	# 	if resultPass!=passHash:
	# 		tkMessageBox.showinfo("Error", "Wrong Password")
	# 		i+=1
	# 		if i==3:
	# 			i=0
	# 			tkMessageBox.showinfo("Error", "You type wrong password three time. Please contact ...")
		
		# self.show_frame(StartPage)
class StartPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, text="Start Page")
		label.pack()
		cardnum=""
		def limitSizeDay(*args):
			value = dayValue.get()
			if len(value) > 6: dayValue.set(value[:6])
		
		dayValue = StringVar()
		dayValue.trace('w', limitSizeDay)

		global e1
		e1 = Entry(self,show="*",width=6,textvariable=dayValue)
		e1.place(x=200,y=250,height=100,width=250)
		e1.config(font=("Courier", 60))
		page_one = Button(self, text="Confirm", command=lambda:controller.checkPage(PageOne))
		page_one.pack()
		page_one.place(x=700, y=250)
		page_two = Button(self, text="Cancel")
		page_two.pack()
		page_two.place(x=700, y=300)

class PageOne(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)


		print "card : "+cardnum
		label = Label(self, text="Choose service")
		label.pack()

		start_page = Button(self, text="Cancel", command=lambda:controller.show_frame(StartPage))
		start_page.pack()
		start_page.place(x=700, y=250)

		page_two = Button(self, text="Enter amount", command=lambda:controller.show_frame(PageTwo))
		page_two.pack()
		page_two.place(x=700, y=300)
		page_two = Button(self, text="200", command=lambda:controller.baseCheck(PageThree,200))
		page_two.pack()
		page_two.place(x=700, y=350)
		page_two = Button(self, text="500", command=lambda:controller.baseCheck(PageThree,500))
		page_two.pack()
		page_two.place(x=700, y=400)
		page_two = Button(self, text="1,000", command=lambda:controller.baseCheck(PageThree,1000))
		page_two.pack()
		page_two.place(x=700, y=450)

class PageTwo(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		global e2
		def limitSizeDay(*args):
			value = dayValue2.get()
			if len(value) > 5: dayValue2.set(value[:5])

		dayValue2 = StringVar()
		dayValue2.trace('w', limitSizeDay)

		e2 = Entry(self,width=5,textvariable=dayValue2)
		e2.place(x=200,y=250,height=100,width=250)
		e2.config(font=("Courier", 60))
		nAmount=e2.get()
		label = Label(self, text="Page Two")
		label.pack()
		start_page = Button(self, text="Confirm", command=lambda:controller.baseCheck(PageThree))
		start_page.pack()
		start_page.place(x=700, y=250)
		page_one = Button(self, text="Back", command=lambda:controller.show_frame(PageOne))
		page_one.pack()
		page_one.place(x=700, y=300)

class PageThree(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		global label2
		global label3
		label = Label(self, text="Bill")
		label.pack()
		label2 = Label(self, text="Amount : ")
		label2.pack()
		label3 = Label(self, text="Balance : ")
		label3.pack()
		
		start_page = Button(self, text="Yes", command=lambda:controller.billPage(StartPage))
		start_page.pack()
		start_page.place(x=70, y=500)
		page_one = Button(self, text="No", command=lambda:controller.show_frame(StartPage))
		page_one.pack()
		page_one.place(x=700, y=500)
class PageFour(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		global firebase
		global a
		global e3
		main()
		a=retcardnum()
		print a
		print "!@#$%^&*(*&^%$#@"
		result = firebase.get(a+'/wrongPass', None)
		def limitSizeDay(*args):
			value = dayValue3.get()
			if len(value) > 6: dayValue3.set(value[:6])
			
		dayValue3 = StringVar()
		dayValue3.trace('w', limitSizeDay)
		e3 = Entry(self,show="*",width=6,textvariable=dayValue3)
		e3.place(x=200,y=250,height=100,width=250)
		e3.config(font=("Courier", 60))
		# passw=e3.get()
		print result
		print "!@#$%^&*()(*&^%$#@!@#$%^&*("
		page_one = Button(self, text="Confirm", command=lambda:controller.baseCheck(PageThree,result))
		page_one.pack()
		page_one.place(x=700, y=250)
		page_two = Button(self, text="Cancel", command=lambda:controller.show_frame(StartPage))
		page_two.pack()
		page_two.place(x=700, y=300)

class MainMenu:
	def __init__(self, master):
		menubar = Menu(master)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		master.config(menu=menubar)

app = App()
app.geometry("800x600+300+300")
app.mainloop()
