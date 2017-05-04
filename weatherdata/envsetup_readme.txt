1. 安装python
   32位系统安装32位版本 python-2.7.13.msi
 
   64位系统64位版本 python-2.7.13.amd64.msi



2. 安装必要的lib

   参考 http://www.cnblogs.com/eastmount/p/5052871.html

2.1 下载
   对应的lib:
Numpy、Scipy、Matplotlib、Scikit-learn 

  Numpy: https://pypi.python.org/pypi/numpy (numpy-1.12.0-cp27-none-win32.whl)
       
  numpy?1.11.3+mkl?cp27?cp27m?win32.whl


  Scipy: https://pypi.python.org/pypi/scipy/0.18.1
       
  http://www.lfd.uci.edu/~gohlke/pythonlibs/tugh5y6j/scipy-0.18.1-cp27-cp27m-win32.whl


  Matplotlib：http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib (matplotlib?1.5.3?cp27?cp27m?win32.whl)


  Scikit-learn：http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-learn (scikit_learn?0.18.1?cp27?cp27m?win32.whl)



  xlrd 1.0.0：
       
  
xlwt-1.2.0

  

非官方页面:
http://www.lfd.uci.edu/~gohlke/pythonlibs/



2.2 安装
 
  pip install **.whl



3. 配置
  
   编辑runbase.bat文件，设置为你本机的路径
  
   set PYTHON_HOME=E:\bin\python2.7.13


  

4. 运行
 
  4.1 查看单个地区天气图形
     
      运行runview.bat
 4.2 获取全部地区的气象数据
     
     运行runfetcher.bat



5.计划任务(周期性运行数据获取任务)
  
   http://jingyan.baidu.com/article/4f34706e8a2c29e387b56d9e.html

   参考上面的链接，设置周期任务
      打开周期任务，新建
      注意在出发器中选择【按预定计划】，【一次】，时间在某个整点时间后5分钟
      在高级设置中注意选择 重复任务间隔为【1小时】
      勾选上【已启用】
   在操作选中 runfetcher.bat

