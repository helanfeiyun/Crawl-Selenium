import numpy as np
import xlrd,xlwt
from xlutils.copy import copy as cp
import copy
import os




def b2n(x):
    '''将布尔值转化为0,1表示的数组
    输入必须是布尔类型，输出为与原shape相同的numpy数组
    '''
    assert bool(x)==True
    seq=np.zeros(np.array(x).shape)
    return seq+x



def writer(x,sheetname,rename,sheethead=None,keyname=None,interval=True):
    '''将目标写入excel文件

    参数：
       x:要输写入的目标变量，类型可以是list，numpy.array等
         shape维度最多为2
       sheetname：要写入sheet的名称。若该表不存在，则会新建该表
         并写入内容；若已存在该sheet且存在内容，新写入的内容会和
         原来的内容相隔一行依次写入sheet内
       sheethead：写入数据的表头，即每列的名称，
         类型为str，默认为无
       rename：excel文件的名字,类型为str
       keyname:sheethead的注释，默认为None
       interval: 新写入的内容是否与原来的内容有间隔，True为有一
       行间隔，False为无间隔，默认为True
    注意：若excel文件不存在，则会自动生成一个名称为rename的excel文件
       并包含一个名称为空表的sheet
    '''

    if os.path.exists(rename)==False:
        workbook = xlwt.Workbook(rename)
        workbook.add_sheet('空表', cell_overwrite_ok=True)
        workbook.save(rename)

    sheethead=copy.deepcopy(sheethead)
    if keyname!=None:
        sheethead.append(keyname)
    excel=xlrd.open_workbook(rename)
    sheetnames=excel.sheet_names()
    y=np.array(x)
    l=len(y.shape)
    if sheetname in sheetnames:
        if l==2:
            sheet1 = excel.sheet_by_name(sheetname)
            v0 = sheet1.col_values(0)
            book=cp(excel)
            sheet2=book.get_sheet(sheetname)
            if interval==True:
                lenth = len(v0) + 1
            else:
                lenth=len(v0)
            if sheethead!=None:
                for i in range(len(sheethead)):
                    sheet2.write(lenth, i, sheethead[i])
                for i in range(len(x)):
                    for j in range(len(x[i])):
                        sheet2.write(i + lenth + 1, j, x[i][j])
            else:
                for i in range(len(x)):
                    for j in range(len(x[i])):
                        sheet2.write(i + lenth, j, x[i][j])

            book.save(rename)
        else:
            sheet1 = excel.sheet_by_name(sheetname)
            v0 = sheet1.col_values(0)
            book = cp(excel)
            sheet2 = book.get_sheet(sheetname)
            if interval==True:
                lenth = len(v0) + 1
            else:
                lenth=len(v0)
            if sheethead!=None:
                for i in range(len(sheethead)):
                    sheet2.write(lenth, i, sheethead[i])
                for i in range(len(x)):
                    sheet2.write(lenth + 1, i, x[i])
            else:
                for i in range(len(x)):
                    sheet2.write(lenth, i, x[i])
            book.save(rename)
        excel.release_resources()
    else:
        if l==2:
            book = cp(excel)
            newsheet = book.add_sheet(sheetname, cell_overwrite_ok=True)
            if sheethead!=None:
                for i in range(len(sheethead)):
                    newsheet.write(0, i, sheethead[i])
                for i in range(len(x)):
                    for j in range(len(x[i])):
                        newsheet.write(i + 1, j, x[i][j])
            else:
                for i in range(len(x)):
                    for j in range(len(x[i])):
                        newsheet.write(i, j, x[i][j])
            book.save(rename)
        else:
            book = cp(excel)
            newsheet = book.add_sheet(sheetname, cell_overwrite_ok=True)
            if sheethead!=None:
                for i in range(len(sheethead)):
                    newsheet.write(0, i, sheethead[i])
                for i in range(len(x)):
                    newsheet.write(1, i, x[i])
            else:
                for i in range(len(x)):
                    newsheet.write(0, i, x[i])
            book.save(rename)
        excel.release_resources()

