from Tkinter import *

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

def main_show_return():
    root = Tk()
    app = App(master=root)
    app.mainloop()
    root.destroy()

class WMApp(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
    def test():
        print "test"
        

def main_show2():
    #create the application
    root = Tk()
    myapp = WMApp()
    #here are method calls to the window manager class
    myapp.master.title("My Do-Nothing Application")
    myapp.master.minsize(200, 40)
    myapp.master.maxsize(1000, 400)
    #start the program
    myapp.mainloop()
		
if __name__ == '__main__':
	print "__main__:"
	#main_show_return()
	main_show2()	