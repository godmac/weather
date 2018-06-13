#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import datetime
import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy
from xlwt import *
import re

#r'd:\a.txt'
filepath_orig="D:/repo/weather/excel/oil.xlsx"
filepath_transfer="D:/repo/weather/excel/oil_transfer.xls"

start_row_index=4
num_each_factory=15

def wmain():
    print(filepath_orig)
    wb_orig = xlrd.open_workbook(filepath_orig)
    sheet_orig = wb_orig.sheets()[0] 
    print(sheet_orig)

    NROWS=sheet_orig.nrows
    NCOLS=sheet_orig.ncols
    print("NROWS:",NROWS)
    print("NCOLS:",NCOLS)
    #for() rm colum total, 15 span
    
    wb_tranfer = xlwt.Workbook(encoding = 'ascii')
    sheet_tranfer = wb_tranfer.add_sheet('OK')
    newline=0;
    for irow in range(start_row_index,NROWS):
        print('==============================================================================')
        print('-------------------------------------------------------irow:',irow)

        for icol in range(1,NCOLS):
            print('-----------------------------------------------------------------------------')
            print('-------------------------------------------------------icol:',icol)
            # if column is total, continue
            if icol%num_each_factory==1:
                continue;
            print('-------------------------------------------------------cell:',sheet_orig.cell(irow,0).value)
            #datetime copy
            sheet_tranfer.write(newline,0, sheet_orig.cell(irow,0).value)
            for index in range(0,start_row_index):
                print('-------------------------------------------------------cell:',sheet_orig.cell(index, icol).value)
                sheet_tranfer.write(newline,index+1,sheet_orig.cell(index, icol).value)
            print('-------------------------------------------------------cell:',sheet_orig.cell(irow, icol).value)
            sheet_tranfer.write(newline,start_row_index+1,sheet_orig.cell(irow, icol).value)
            newline=newline+1
    wb_tranfer.save(filepath_transfer)
    
    print('wbook.save')



if __name__ == '__main__':
    print('start to transfer')
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    wmain()
    
    print('start to transfer ')



