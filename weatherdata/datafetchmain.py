#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import datetime
import getopt
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

import weather
from weather import WeatherEnv
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import *
import logging
from logging.handlers import RotatingFileHandler

 
def set_style(name,height,bold=False):
  style = xlwt.XFStyle() # 初始化样式
 
  font = xlwt.Font() # 为样式创建字体
  font.name = name # 'Times New Roman'
  font.bold = bold
  font.color_index = 4
  font.height = height
 
  # borders= xlwt.Borders()
  # borders.left= 6
  # borders.right= 6
  # borders.top= 6
  # borders.bottom= 6
 
  style.font = font
  # style.borders = borders
 
  return style

#获取脚本文件的当前路径
def getcitydata(line):
    cityinfo = line.split()
    cityname = cityinfo[1]
    citycode = cityinfo[2]
    logger.info('getcitydata,'+str(cityinfo))
    wfilename=WeatherEnv.WEATHER_TMPFILE
    weather.getCityCodeWeatherFile(citycode,wfilename)
    citycodeweather = weather.convertFromFile(wfilename)
    writecityfile(citycodeweather)

def writecityfile(cityweather):
    # filename:code_year_month
    # filename = WEATHER_DATA_HOME+os.path.sep+cityweather.id+'_"+
    wdate = datetime.datetime.strptime(cityweather.ptime, '%y-%m-%d %H:%M')
    targettime = wdate.strftime("%Y%m")
    curtime = datetime.datetime.now().strftime("%Y%m")

    if(targettime!=curtime):
        print "curtime",curtime
        logger.warning('targettime!=curtime,return')
        return
    targetfilename = WeatherEnv.WEATHER_DATA_HOME+os.path.sep+cityweather.id+'_'+targettime+".xls"
    logger.info('writecityfile:'+str(wdate))
    if not os.path.exists(targetfilename):
        #os.mkdir(WeatherEnv.WEATHER_DATA_HOME)
        wbook = Workbook()
        logger.debug('new wbook:' + str(wbook))
        wsheet = wbook.add_sheet(cityweather.id)
        logger.debug('wsheet:' + str(wsheet))
        row0 = [u'id',u'ptime',u'city',u'h',u'wd',u'fx',u'fl',u'js',u'sd']
        for i in range(0,len(row0)):
            wsheet.write(0,i,row0[i],set_style('Times New Roman',220,True))
        wbook.save(targetfilename)
        logger.info('wbook.save')
        #wbook.close()

    #open file
    rbook = xlrd.open_workbook(targetfilename)
    logger.debug('open book:' + str(rbook))
    # open sheet
    # table = data.sheets()[0]          #通过索引顺序获取
    # table = data.sheet_by_index(0) #通过索引顺序获取
    #  table = data.sheet_by_name(u'Sheet1')#通过名称获取
    rsheet = rbook.sheet_by_name(cityweather.id)
    logger.debug('rsheet:' + str(rsheet))
    nrows = rsheet.nrows
    logger.debug('nrows:' + str(nrows))
    
    writebook = copy(rbook)  #wbook即为xlwt.WorkBook对象
    logger.debug('writebook:' + str(writebook))
    writesheet = writebook.get_sheet(0) #get_sheet(0)  #通过get_sheet()获取的sheet有write()方法
    #writesheet.write(0, 0, 'value')
    rowindex =0
    columindex=0
    #print 'cityweather.qws:',cityweather.qws
    for qw in cityweather.qws:
       logger.debug('qw:'+ str(qw)) 
       writesheet.write(nrows+rowindex,columindex,cityweather.id,set_style('Times New Roman',220,True))
       columindex+=1
       writesheet.write(nrows+rowindex,columindex,cityweather.ptime,set_style('Times New Roman',220,True))
       columindex+=1
       writesheet.write(nrows+rowindex,columindex,cityweather.city,set_style('Times New Roman',220,True))
       columindex+=1
       for data in qw:
           writesheet.write(nrows+rowindex,columindex,data,set_style('Times New Roman',220,True))
           columindex+=1
       #writesheet.write(nrows+rowindex,columindex,qw.wd,set_style('Times New Roman',220,True))
       #columindex+=1
       #writesheet.write(nrows+rowindex,columindex,qw.fx,set_style('Times New Roman',220,True))
       #columindex+=1
       #writesheet.write(nrows+rowindex,columindex,qw.fl,set_style('Times New Roman',220,True))
       #columindex+=1
       #writesheet.write(nrows+rowindex,columindex,qw.js,set_style('Times New Roman',220,True))
       #columindex+=1
       #writesheet.write(nrows+rowindex,columindex,qw.sd,set_style('Times New Roman',220,True))
       columindex=0
       rowindex+=1
    writebook.save(targetfilename)
    #writebook.close()
    logger.debug('save file:'+ targetfilename)

def getalldata():
    logger.info('enter getalldata')
    weather.initWeatherEnv()
    #read citycode    WeatherEnv.WEATHER_CITYCODE
    if not os.path.exists(WeatherEnv.WEATHER_CITYCODE):
        print "no file,return"
        return
    inputfile = open(WeatherEnv.WEATHER_CITYCODE, 'r')
    #list_of_all_the_lines = input.readlines( )

    for line in inputfile:
        logger.info('line:'+line+str(datetime.datetime.now()))
        if line.isspace():
            continue
        #line='20112	浦东	101021300'
        try:
            getcitydata(line)
        except Exception,e:  
            logger.warning( 'Exception,line:'+str(e))
            print Exception,":",e
        #logger.info('line:'+line+(datetime.datetime.now()))

    logger.info('leave getalldata')    

if __name__ == '__main__':
    print 'init log cfg'
    weather.initLog('datafetcher.log')
    logger = logging.getLogger('main') 
    logger.info('__main__: start')
    getalldata()
    logger.info('__main__: end')
    logging.shutdown()
    print "__main__: end"
