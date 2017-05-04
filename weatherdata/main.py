#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import datetime
import urllib2
from Tkinter import *
from ttk import *
import Tix
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.font_manager import fontManager
from matplotlib.figure import Figure
#import tktools
import weather
from weather import WeatherEnv
import logging
from logging.handlers import RotatingFileHandler

class WeatherWindow(Frame):

    def initWidgets(self,parent):
        self.__parent = parent
        logger.info('initWidgets: start')
        ############ __topcontrols
        self.__topcontrols = Frame(parent)
        self.__topcontrols.pack(side=TOP, fill=X)
        #label
        self.__label = Label(self.__topcontrols, text=u"城区编码:")
        self.__label.pack(side=LEFT)
        #input
        self.__rootentry = Entry(self.__topcontrols, width=50)
        self.__rootentry.pack(side=LEFT)
        self.__rootentry.bind('<Key-Return>', self.updateDataEntry)
        self.__rootentry.focus_set()
        #run buttion
        self.__start = Button(self.__topcontrols, text="更新", command=self.updateDataButton)
        self.__start.pack(side=LEFT)
        if __name__ == '__main__': # No Quit button under Grail!
            self.__quit = Button(self.__topcontrols, text="Quit",
                                 command=self.__parent.quit)
            self.__quit.pack(side=RIGHT)
        ############ __controls weather
        self.__controls = Frame(parent)
        self.__controls.pack(side=TOP, fill=X)

        #stop buttion
        #self.__stop = Button(self.__controls, text="Stop", command=self.stop,
        #                     state=DISABLED)
        #self.__stop.pack(side=LEFT)
        
        #self.__cv = BooleanVar(parent)
        self.__cityval = StringVar()
        self.__cityval.set("NO CITY.")
        self.__city = Label(self.__controls, textvariable = self.__cityval, anchor=W)
        self.__city.pack(side=TOP, fill=X)
        self.__statusval = StringVar()
        self.__statusval.set("NO STATUS.")
        self.__status = Label(self.__controls, textvariable = self.__statusval, anchor=W)
        self.__status.pack(side=TOP, fill=X)
        # show weather detail
        self.__note = Notebook(self.__controls) #, activefg = 'red', inactivefg = 'blue'

        self.__tab_wd = Frame(self.__note)
        self.__tab_fx = Frame(self.__note)
        self.__tab_fl = Frame(self.__note)
        self.__tab_js = Frame(self.__note)
        self.__tab_sd = Frame(self.__note) #湿度

        #Button(tab1, text='Exit', command=root.destroy).pack(padx=100, pady=100)

        self.__note.add(self.__tab_wd, text = "温度", compound=TOP) #image=scheduledimage,
        self.__note.add(self.__tab_fx, text = "风向", compound=TOP)
        self.__note.add(self.__tab_fl, text = "风力", compound=TOP)
        self.__note.add(self.__tab_js, text = "降水量", compound=TOP)
        self.__note.add(self.__tab_sd, text = "相对湿度", compound=TOP)
        self.__note.pack(side=TOP, fill=X)
        
        #fonts = [font.name for font in fontManager.ttflist if os.path.exists(font.fname) and os.stat(font.fname).st_size>1e6] 
        #font = set(fonts)
        #print fontManager.ttflist
        #print "\nfonts:",fonts
        #print "\n\nfont",font
        logger.info('initWidgets: end')
    def updateDataButton(self):
        print "updatedataButton"
        citycode = self.__rootentry.get()
        self.updateDataWeather(citycode)
        
    def updateDataEntry(self, event):
        print "updatedataEntry"
        citycode = self.__rootentry.get()
        self.updateDataWeather(citycode)

    def updateDataWeather(self, citycode):
        logger.info('updateDataWeather: start')
        wfilename =  WeatherEnv.WEATHER_FILE+citycode+".xml"
        weather.getCityCodeWeatherFile(citycode,wfilename)
        self.drawUpdateWeather(wfilename)
        
        if not self.__weather:
            return
        ptime=self.__weather.ptime #ptime="17-01-12 12:00"
        wdate = datetime.datetime.strptime(ptime, '%y-%m-%d %H:%M')
        print "date:",wdate
        targettime = wdate.strftime("%Y%m%d%H%M")
        targetfilename = WeatherEnv.WEATHER_FILE+citycode+targettime+".xml"
        print "targetfilename:",targetfilename
        if not os.path.exists(targetfilename):
            os.rename(wfilename,targetfilename)
        logger.info('updateDataWeather: end')

    def drawUpdateWeather(self,wfilename):
        logger.info('drawUpdateWeather: start')
        self.__weather = weather.convertFromFile(wfilename)
        if not self.__weather:
            self.__statusval.set('ERROR')
            logger.warning(str(wfilename)+' convertFromFile error')
            return
        self.__cityval.set(self.__weather.city)
        self.__statusval.set('SUCCESS')
        logger.info(str(wfilename)+' convertFromFile success')
        print "__statusval: " + self.__statusval.get()    
        self.drawWeatherTab(1,self.__weather,self.__tab_wd)
        self.drawWeatherTab(2,self.__weather,self.__tab_fx)
        self.drawWeatherTab(3,self.__weather,self.__tab_fl)
        self.drawWeatherTab(4,self.__weather,self.__tab_js)
        self.drawWeatherTab(5,self.__weather,self.__tab_sd)
        #self.__note[IDNum][0]['relief'] = self.activerelief
        self.__note.select(0) #select add(child, **kw)
        logger.info('drawUpdateWeather: end')

    def drawWeatherTab(self, frameindex, weather, ownerframe): #ownerframeParent
        logger.info("drawWeatherTab frameindex:%d, ownerframe:%s"%(frameindex,ownerframe))
        print "drawWeatherTab(),frameindex:%d " %(frameindex)
        tempqws = weather.qws
        tmph = [x[0] for x in weather.qws]
        tmpwd = [y[frameindex] for y in weather.qws]
        #print "tmph,len:%d, tmph:%s"%(len(tmph),tmph)
        #print "tmph,len:%d, tmph:%s"%(len(tmpwd),tmpwd)

        x = []
        index = 0
        for index in range(0, len(tmph)):#while index < len(tmph):
            #print "index:%d ,tmph:%s %s"%(index, tmph[index], "END")
            if tmph[index]:
                x.append(int(tmph[index]))
            elif  tmph[index-1]:
                x.append(int(tmph[index-1]))
            elif  tmph[index-2]:                
                x.append(int(tmph[index-2]))   
            elif  tmph[index-3]:                
                x.append(int(tmph[index-3]))
            else :   
                x.append(int(tmph[index+1]))                 
            #index++                
        print "lenth:%d,x:%s"%(len(x),x)
        #y = [ int( y ) for y in y if y ]
        y = []
        index=0
        while index < len(tmpwd):
            if tmpwd[index]:
                y.append(int(tmpwd[index]))
            elif tmpwd[index-1]:
                y.append(int(tmpwd[index-1]))
            elif tmpwd[index-2]:                
                y.append(int(tmpwd[index-2]))   
            elif tmpwd[index-3]:                
                y.append(int(tmpwd[index-3]))
            else :  
                y.append(int(tmpwd[index+1])) 
            index=index+1                

        print "y len:%d,y:%s"%(len(y),y)
        #import numpy as np
        #import matplotlib.pyplot as plt
        #直接使用Artists创建图表的标准流程如下：
        #创建Figure对象
        #用Figure对象创建一个或者多个Axes或者Subplot对象
        #调用Axies等对象的方法创建各种简单类型的Artists
        fig = plt.Figure(figsize=(11,6), dpi=100) 
        canvas = FigureCanvasTkAgg(fig, master=ownerframe)
        canvas.show()
        grid = canvas.get_tk_widget().grid(row=0, columnspan=4)
        print "grid:",grid
        #toolbar = NavigationToolbar2TkAgg(canvas, master=ownerframe)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        #清空图像，以使得前后两次绘制的图像不会重叠
        fig.clf()
        print "fig:",fig
        axes=fig.add_subplot(111) #Axies等
        print "axes:",axes 

        ax=np.array(x)
        ay=np.array(y)
        print "ax:",ax
        print "ay:",ay
        
        #axes.plot(x,y)
        rx=np.linspace(0,len(x)-1,len(x))
        
        color=['b','r','y','g']
        #绘制这些随机点的散点图，颜色随机选取
        axes.plot(rx,ay,'--',color="red",linewidth=1) #label=$cos(x^2)$
        axes.scatter(rx,ay,s=10,color=color[np.random.randint(len(color))])
        #plt.clear();
        axes.set_title(u"24小时整点天气实况",{'fontname':u'FangSong','fontsize':18})

        axes.set_xlabel(u"24小时时间轴(H)",{'fontname':u'FangSong','fontsize':18}) 
        
        print "frameindex:",frameindex
        if frameindex==1:
            axes.set_ylabel(u"摄氏度℃" ,{'fontname':u'FangSong','fontsize':18})
        elif frameindex==2:
            axes.set_ylabel(u"风向",{'fontname':u'FangSong','fontsize':18})
        elif frameindex==3:
            axes.set_ylabel(u"风力",{'fontname':u'FangSong','fontsize':18})
        elif frameindex==4:
            axes.set_ylabel(u"降水量",{'fontname':u'FangSong','fontsize':18})
        elif frameindex==5:
            axes.set_ylabel(u"相对湿度",{'fontname':u'FangSong','fontsize':18})
        #plt.xticks((0,1),(u'男',u'女'))
        axes.set_xticks(rx)
        axes.set_xticklabels(tmph,rotation=30)
        #plt.ylim(-12,30)
        #axes.legend()
        canvas.draw()
        canvas.show()

    def drawPic(self, ownerframe):
        """
        获取GUI界面设置的参数，利用该参数绘制图片
        """
        #在Tk的GUI上放置一个画布，并用.grid()来调整布局
        drawPicf = plt.Figure(figsize=(5,4), dpi=100) 
        drawPiccanvas = FigureCanvasTkAgg(drawPicf, master=ownerframe)
        drawPiccanvas.show()
        drawPiccanvas.get_tk_widget().grid(row=0, columnspan=3)    
        #获取GUI界面上的参数
        #try:sampleCount=int(inputEntry.get())
        #except:
        #    sampleCount=50
        #    print '请输入整数'
        #    inputEntry.delete(0,END)
        #    inputEntry.insert(0,'50')
        sampleCount=50
        #清空图像，以使得前后两次绘制的图像不会重叠
        drawPicf.clf()
        drawPica=drawPicf.add_subplot(111)
        
        #在[0,100]范围内随机生成sampleCount个数据点
        x=np.random.randint(0,100,size=sampleCount)
        y=np.random.randint(0,100,size=sampleCount)
        color=['b','r','y','g']
        
        #绘制这些随机点的散点图，颜色随机选取
        drawPica.scatter(x,y,s=3,color=color[np.random.randint(len(color))])
        drawPica.set_title('Demo: Draw N Random Dot')
        drawPiccanvas.show()  

    def updateTempture(self, ownerframe):
        '''绘图逻辑'''
        x = np.random.randint(0,50,size=100)
        y = np.random.randint(0,50,size=100)
        
        #ownerframe.fig.clf()                  # 方式一：①清除整个Figure区域
        #ownerframe.ax = self.fig.add_subplot(111)    # ②重新分配Axes区域
        #ownerframe.ax.clear()                  # 方式二：①清除原来的Axes区域
        #ownerframe.ax.scatter(x, y, s=3)  # 重新画
        #ownerframe.canvas.show()
    
        #metod1
        #plt,plot([1,2,3])
        #plt.ylabel('some numbers')
        #plt.show()
        x = np.linspace(0, 10, 1000)
        y = np.sin(x)
        z = np.cos(x**2)
        plt.figure(figsize=(8,4)) 
        plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2) 
        plt.plot(x,z,"b--",label="$cos(x^2)$") 
        plt.xlabel("Time(s)") 
        plt.ylabel("Volt") 
        plt.title("PyPlot First Example") 
        plt.ylim(-1.2,1.2) 
        plt.legend() 
        plt.show()

    def quit(self):
        print "quit"
        #self.__parent.quit()
        self.quit()
        self.destroy()

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        #self.pack()
        self.initWidgets(parent)

def wmain():
    logger.info('wmain: start')
    root = Tk(className='Weather') #show in window as title
    #parse config
    #citycode, citycodefile
    weather.initWeatherEnv()
    root.geometry("1100x700+100+30")  
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.iconbitmap(WeatherEnv.WEATHER_HOME+os.path.sep+'weather.ico')
    window = WeatherWindow(root)
    window.mainloop()
    root.quit()
    root.destroy()
    logger.info('wmain: end')

if __name__ == '__main__':
    print 'init log cfg'
    weather.initLog('mainview.log')
    logger = logging.getLogger('main') 
    print "__main__: start"
    logger.info('__main__: start')
    wmain()
    logger.info('__main__: end')
    print "__main__: end"



