#! /usr/bin/python 
# coding = utf-8

from Tkinter import *
class Notebook(Frame):
    def __init__(self, parent, activerelief = SOLID, inactiverelief = SOLID, xpad = 4, ypad = 4, activefg = 'black',activebg='green',inactivebg='grey',bd=1,inactivefg = 'black', **kw):                                                                
        self.activefg = activefg
        self.activebg=activebg
        self.bd=bd
        self.inactivebg=inactivebg
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                 
        self.tabs = 0                                                                                                                                                 
        self.noteBookFrame = Frame(parent)                                                 
        self.BFrame = Frame(self.noteBookFrame)                                            
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 1, **kw)           
        self.noteBook.grid_propagate(0)                                                    
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def add_tab(self, width = 1, **kw):            
            temp = self.tabs                                                                   
            self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               
            self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  
            self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) 
            self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                
            self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               
            self.change_tab(0)                                                                 
            self.tabs += 1                                                                     
            return self.tabVars[temp][1]
    def change_tab(self, IDNum): 
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  
                if i <> IDNum:                                                             
                    self.tabVars[i][1].grid_remove()                                       
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     
                    self.tabVars[i][0]['fg'] = self.inactivefg
                    self.tabVars[i][0]['bg'] = self.inactivebg
                    self.tabVars[i][0]['bd'] = self.bd
                else:                                                                      
                    self.tabVars[i][1].grid()                                                                    
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   
                    self.tabVars[i][0]['fg'] = self.activefg
                    self.tabVars[i][0]['bg'] = self.activebg
                    self.tabVars[i][0]['bd'] = self.bd


root=Tk()
scheduledimage=PhotoImage(data="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")
note=Notebook(root, width= 400, height =400, activefg = 'red', inactivefg = 'blue')
note.grid()
tab1 = note.add_tab(text = "Tab One",image=scheduledimage)
tab2 = note.add_tab(text = "Tab Two")                                                
tab3 = note.add_tab(text = "Tab Three")
root.mainloop()




