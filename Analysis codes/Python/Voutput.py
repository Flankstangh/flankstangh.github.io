import pandas
import numpy 
import statsmodels.api
from numpy import *
import os

def ispath_exist(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)

# 输入数据应为DataFrame格式
def df2csv(df,filename):    #通用函数，输出pd至csv
    ispath_exist('./output')
    df.to_csv(filename+'.csv',encoding='utf_8_sig')    #解决输出中文乱码


#输入数据应为SimpleTable格式，可为以下几种：
# var_mod.model.select_order().summary() （VAR模型的信息准则）
# vecm_mod.summary().tables[i] （VECM回归报告特定表格）
class tbl2csv():
    def __init__(self,table,filename):
        ispath_exist('./output')
        self.table=table
        self.filename=filename
        self.tbl2pd()

    def tbl2pd(self):
        tbl_list=list(self.table)
        df_tbl=pandas.DataFrame(tbl_list)
        df_tbl.to_csv(self.filename+'.csv',encoding='utf_8_sig',index=False, header=False)


# 输入数据应为Summary格式，可为：
# statsmodels.iolib.summary.Summary （OLS/VECM回归报告）
def ols2latex(summary,foldname):
    fold=foldname
    ispath_exist(fold)
    filename=pandas.DataFrame(summary.tables[0])[1][0]
    data=summary.as_latex()
    with open(fold+'/'+str(filename)+'.txt', 'a') as file_handle:
        file_handle.write(data)  # 写入
        file_handle.write('\n')
def vecm2latex(summary,filename):
    data=summary.as_latex()
    ispath_exist('./output')
    with open(filename+'.txt', 'a') as file_handle:
        file_handle.write(data)  # 写入
        file_handle.write('\n')


# 输入数据应为Summary格式，可为：
# statsmodels.iolib.summary.Summary （VECM回归报告）
def vecm2csv(summary,filename):
    data=summary.as_csv()
    ispath_exist(filename)
    with open(filename+'.csv', 'a') as file_handle:
        file_handle.write(data)  # 写入
        file_handle.write('\n')


# 目标对象为irf = var_mod.irf()，为以下数据类型：
# statsmodels.tsa.vector_ar.irf.IRAnalysis
class irf2csv():  # 输出脉冲响应图数据
    def __init__(self, irf_obj, foldname):
        self.irf_obj = irf_obj
        self.foldname = foldname
        ispath_exist(self.foldname)
        self.get_names()
        self.irf_stderr()

    def irf_stderr(self):   #分别输出数据点和标准差
        self.irf_array=self.irf_obj.irfs
        datapoint=self.irf_array2df(self.irf_array)
        self.irf_df2csv(datapoint,'irf_datapoint')

        self.stderr_array=self.irf_obj.stderr()
        stderror = self.irf_array2df(self.stderr_array)
        self.irf_df2csv(stderror, 'irf_stderror')

    def get_names(self):
        self.namelist=[]
        names=self.irf_obj.model.names  #变量名，查源码statsmodels/statsmodels/tsa/vector_ar/irf.py得到
        for i in names:
            temp1=str()
            temp1='->'+i
            for j in names:
                temp2=str()
                temp3=str()
                temp2=j
                temp3=temp2+temp1
                temp2=''
                self.namelist.append(temp3)

    def mergelist(self, array):  # 把多个array合并为一个list
        merged = []
        for i in range(len(array)):
            for j in list(array[i]):  # 把ndarray转为list
                merged.append(j)
        return merged

    def irf_array2df(self,input_array):
        self.array=input_array
        graphic_list =[]
        dot_list = []  # 按图像顺序记录最终点
        for i in self.array:
            graphic_list.append(i)
        graph_number = len(self.mergelist(graphic_list[0]))
        for index in range(graph_number):
            temp =[]
            for j in graphic_list:  # 获得一个图像的所有点
                temp.append(self.mergelist(j)[index])
            dot_list.append(temp)
        self.dot_df = pandas.DataFrame(dot_list,dtype=numpy.float)
        return self.dot_df

    def irf_df2csv(self,input_df,category):
        input_df.insert(0,'冲击顺序',self.namelist)
        input_df.to_csv(self.foldname+'/'+category+'.csv',encoding='utf_8_sig',index=False, header=True)  # 输出至csv


# 继承父类irf2csv
# 输入数据应为FEVD格式，可为：
# statsmodels.tsa.vector_ar.var_model.FEVD （VAR模型预测误差方差）
class fevd2csv(irf2csv):
    def __init__(self, fevd_obj, foldname):
        self.fevd_obj = fevd_obj
        self.foldname = foldname
        ispath_exist(self.foldname)
        self.get_names()
        self.fevd_array2df()

    def get_names(self):
        self.namelist=self.fevd_obj.names

    def fevd_df2csv(self,df,name):
        isExists = os.path.exists(self.foldname)
        if not isExists:
            os.makedirs(self.foldname)
        df.to_csv(self.foldname+'/'+name+'.csv',encoding='utf_8_sig',index=True, header=True)  # 输出至csv

    def fevd_array2df(self):
        fevd_arrays=self.fevd_obj.decomp
        for i in range(len(fevd_arrays)):
            name=self.namelist[i]   #被解释变量名称
            array=fevd_arrays[i]    #单张图数据量：期数x变量数
            dec_df = pandas.DataFrame(array)
            dec_df.columns=self.namelist
            self.fevd_df2csv(dec_df,name)



def main():
    pass

if __name__=="__main__":
    main()

