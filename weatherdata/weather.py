#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from xml.dom.minidom import parse 
import xml.dom.minidom
import sys,os
import logging
from logging.handlers import RotatingFileHandler

def initLog(filename):
    #logging.basicConfig(level=logging.DEBUG,
    #            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #            datefmt='%a, %d %b %Y %H:%M:%S',
    #            filename='datafetch.log',
    #            filemode='a')
    Rthandler = RotatingFileHandler(filename, maxBytes=10*1024*1024, backupCount=5)
    #Rthandler.setLevel(logging.DEBUG)
    #'%(name)-12s: %(levelname)-8s %(message)s'
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    #logging.getLogger('datafetcher').addHandler(Rthandler)
    logger = logging.getLogger('main') 
    logger.addHandler(Rthandler)
    logger.setLevel(logging.DEBUG)

def cur_file_dir():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    # 如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def initWeatherEnv():
    WeatherEnv.WEATHER_HOME=cur_file_dir()
    WeatherEnv.WEATHER_DATA_HOME=WeatherEnv.WEATHER_HOME+os.path.sep+"data"
    WeatherEnv.WEATHER_CONFIG=WeatherEnv.WEATHER_HOME+os.path.sep+"config.ini"
    WeatherEnv.WEATHER_FILE=WeatherEnv.WEATHER_DATA_HOME+os.path.sep+"weather"
    WeatherEnv.WEATHER_CITYCODE=WeatherEnv.WEATHER_HOME+os.path.sep+"citycode.txt"
    WeatherEnv.WEATHER_TMPFILE=WeatherEnv.WEATHER_HOME+os.path.sep+"TMPFILE.xml"
    print "WEATHER_HOME:"+WeatherEnv.WEATHER_HOME
    print "WEATHER_DATA_HOME:"+WeatherEnv.WEATHER_DATA_HOME
    print "WEATHER_CONFIG:"+WeatherEnv.WEATHER_CONFIG
    print "WEATHER_CITYCODE:"+WeatherEnv.WEATHER_CITYCODE
    if not os.path.exists(WeatherEnv.WEATHER_DATA_HOME):
        os.mkdir(WeatherEnv.WEATHER_DATA_HOME)
    if not os.path.exists(WeatherEnv.WEATHER_CONFIG):
        #os.mknod(WEATHER_CONFIG)
        configfile = open(WeatherEnv.WEATHER_CONFIG, 'w')
        configfile.close()

def getCityCodeWeatherFile(citycode, wfilename):
    weatherurl="http://flash.weather.com.cn/sk2/"+citycode+".xml"
    print "weatherurl:"+weatherurl
    response = urllib2.urlopen(weatherurl)
    html = response.read()

    print "WEATHER_FILE: " +wfilename
    weatherfile = open(wfilename, 'w')
    weatherfile.write(html)
    weatherfile.close( )

class WeatherEnv():
    #global env
    WEATHER_HOME=""
    WEATHER_DATA_HOME=""
    WEATHER_CONFIG=""
    WEATHER_CITYCODE=""
    WEATHER_FILE=""

class Weather():
    #qw=[]
    def __init__(self,wfilepath):
       self.filepath = wfilepath
    def __init__(self,wid,ptime,city):
       self.id=wid
       self.ptime=ptime
       self.city=city
       self.qws=[]
    def add_qw(self, qw):
       self.qws.append(qw)

def convertFromFile(filepath):
    logger = logging.getLogger('main')
    logger.info( 'filepath:'+str(filepath))
    DOMTree = xml.dom.minidom.parse(filepath)
    Data = DOMTree.documentElement 
    if Data.hasAttribute("id"): 
      wid = Data.getAttribute("id")
    if Data.hasAttribute("ptime"): 
      wptime = Data.getAttribute("ptime")
    if Data.hasAttribute("city"): 
      wcity = Data.getAttribute("city")
  
    weather = Weather(wid,wptime,wcity)   
    # get all contry
    qws = Data.getElementsByTagName("qw") 
  
    # print contry in detail
    for qw in qws: 
      #logger.debug('qw:'+str(qw))
      wqw=[]
      if qw.hasAttribute("h"): 
       #print "h: %s" % qw.getAttribute("h")
       wqw.append(qw.getAttribute("h"))
      if qw.hasAttribute("wd"): 
       #print "wd: %s" % qw.getAttribute("wd")
       wqw.append(qw.getAttribute("wd"))   
      if qw.hasAttribute("fx"): 
       #print "fx: %s" % qw.getAttribute("fx") 
       wqw.append(qw.getAttribute("fx"))
      if qw.hasAttribute("fl"):
       #print "fl: %s" % qw.getAttribute("fl") 
       wqw.append(qw.getAttribute("fl"))
      if qw.hasAttribute("js"): 
       #print "js: %s" % qw.getAttribute("js")
       wqw.append(qw.getAttribute("js"))
      if qw.hasAttribute("sd"): 
       #print "sd: %s" % qw.getAttribute("sd") 
       wqw.append(qw.getAttribute("sd"))
      logger.debug('wqw:'+str(wqw))
      weather.add_qw(wqw)

    #print "weather:" 
    #print weather.qws 
    return weather
    

