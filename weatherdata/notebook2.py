#tab1 = note.add_tab(text = "Tab One",image=scheduledimage, compound=TOP)

import Tix
root = Tix.Tk()
root.tk.eval('package require Tix')

from Tkinter import *
from ttk import *

root = Tk()
scheduledimage='' #PhotoImage(file="E:\\1.gif")
scheduledimage2='' #PhotoImage(file='e:\\2.gif')
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
Button(tab1, text='Exit', command=root.destroy).pack(padx=100, pady=100)

note.add(tab1, text = "Tab One", compound=TOP) #image=scheduledimage,
note.add(tab2, text = "Tab Two", compound=TOP)
note.add(tab3, text = "Tab Three")
note.pack()
root.mainloop()
exit()
