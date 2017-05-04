# import Tkinter
# import os
from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

# root = Tk()
# root.title("weather2017")
# root.iconname("weathergui")
# app = Application(master=root)
# app.mainloop()
	
def wmain():
	#notebook = Notebook()
    root = Tk()
	#root.title("weather2017")
    #root.iconname("weathergui")
    app = Application(master=root)
	#app.master.title("weather2017")
    app.mainloop()
    root.destroy()

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.entrythingy = Entry()
        self.entrythingy.pack()

        # here is the application variable
        self.contents = StringVar()
        # set it to some value
        self.contents.set("this is a variable")
        # tell the entry widget to watch this variable
        self.entrythingy["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Key-Return>',
                              self.print_contents)

    def print_contents(self, event):
        print "hi. contents of entry is now ---->", \
              self.contents.get()

#root = Tk()
#app = App(master=root)
#app.mainloop()
#root.destroy()

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
    def test():
        print "test"
        

def main_show():
    #create the application
    myapp = App()
    #here are method calls to the window manager class

    myapp.master.title("My Do-Nothing Application")
    myapp.master.maxsize(1000, 400)

    #start the program
    myapp.mainloop()

	
def main_show2():
    #create the application
    myapp = App()
    #here are method calls to the window manager class

    myapp.master.title("My Do-Nothing Application")
    myapp.master.maxsize(1000, 400)

    #start the program
    myapp.mainloop()

if __name__ == '__main__':
	print "__main__:"
	#wmain()
    main_show2()