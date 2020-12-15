import urllib.request
import urllib.parse
import json,time,xlwt
from bs4 import BeautifulSoup
from lxml import etree

class Tencent():
    def __init__(self):
        self.Get_info()
        self.Get_daily()
        self.Get_province()
    def Get_info(self):
        info_url='https://view.inews.qq.com/g2/getOnsInfo'
        data={}
        data['name']='disease_h5'
        unix_time=str(round(time.time() * 1000))
        data['callback']='jQuery341012106463935552259_'+unix_time
        data['_']=unix_time
        data_string=urllib.parse.urlencode(data)
        req_url=info_url+'?'+data_string
        with urllib.request.urlopen(req_url) as u:
            respond=u.read().decode('utf-8')
            response=respond.strip('jQuery341012106463935552259_'+unix_time).strip('(').strip(')')
            js=json.loads(response)
            self.datas=json.loads(js['data'])
    def Get_daily(self):
        daily = self.datas['chinaDayAddList']
        self.header = ['日期', '新增确诊', '新增疑似', '新增死亡', '新增治愈']
        confirm = []
        suspect = []
        dead = []
        heal = []
        date = []
        self.daily_increase = []
        for d in daily:
            date.append(d.get('date'))
            confirm.append(d.get('confirm'))
            suspect.append(d.get('suspect'))
            dead.append(d.get('dead'))
            heal.append(d.get('heal'))
        self.daily_increase = list(zip(date, confirm, suspect, dead, heal))
    def Get_province(self):
        provinces=self.datas['areaTree'][0].get('children')
        self.province_header=['省份','累计确诊','累计疑似','累计死亡','累计治愈','新增确诊',\
                              '新增疑似','新增死亡','新增治愈']
        province=[]
        total_confirm=[]
        today_confirm=[]
        total_suspect=[]
        today_suspect=[]
        total_dead=[]
        today_dead=[]
        total_heal=[]
        today_heal=[]
        for p in provinces:
            province.append(p.get('name'))
            total_confirm.append(p.get('total').get('confirm'))
            total_suspect.append(p.get('total').get('suspect'))
            total_dead.append(p.get('total').get('dead'))
            total_heal.append(p.get('total').get('heal'))
            today_confirm.append(p.get('today').get('confirm'))
            today_suspect.append(p.get('today').get('suspect'))
            today_dead.append(p.get('today').get('dead'))
            today_heal.append(p.get('today').get('heal'))
        self.province = list(zip(province,total_confirm,total_suspect,total_dead,total_heal,\
                                 today_confirm,today_suspect,today_dead,today_heal))
        print(self.province)

class Dxy():
    def __init__(self):
        self.Get_info()
        self.Get_province()
    def Get_info(self):
        info_url='https://ncov.dxy.cn/ncovh5/view/pneumonia'
        data={}
        data['scene']='2'
        data['clicktime']=str(round(time.time() * 1000))
        data['enterid']=str(round(time.time() * 1000))
        data['from']='timeline'
        data['isappinstalled']='0'
        data_string=urllib.parse.urlencode(data)
        req_url=info_url+'?'+data_string
        with urllib.request.urlopen(req_url) as u:
            respond=u.read().decode('utf-8')
            soup=BeautifulSoup(respond,'html.parser')
            rawdata=soup.find('body').find('script',id='getListByCountryTypeService1').get_text().strip('try { window.getListByCountryTypeService1 = ').strip('}catch(e){}')
            self.datas=eval(rawdata)
    def Get_province(self):
        self.province_header=['省份','累计确诊','累计疑似','累计死亡','累计治愈']
        province=[]
        confirm=[]
        suspect=[]
        dead=[]
        heal=[]
        self.province=[]
        for data in self.datas:
            province.append(data.get('provinceName'))
            confirm.append(data.get('confirmedCount'))
            suspect.append(data.get('suspectedCount'))
            dead.append(data.get('deadCount'))
            heal.append(data.get('curedCount'))
        self.province=list(zip(province,confirm,suspect,dead,heal))

class Netease():
    def __init__(self):
        self.Get_info()
        self.Get_province()
    def Get_info(self):
        info_url='https://c.m.163.com/ug/api/wuhan/app/index/feiyan-data-list'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        data={}
        data['t']=str(round(time.time() * 1000))
        data_string=urllib.parse.urlencode(data)
        req_url=info_url+'?'+data_string
        url = urllib.request.Request(req_url, headers=headers)
        with urllib.request.urlopen(url) as u:
            respond=u.read().decode('utf-8')
            js=json.loads(respond)
            self.datas=js['data']['list']
    def Get_province(self):
        self.province_header = ['省份','地区','累计确诊', '累计疑似', '累计死亡', '累计治愈']
        name=[]
        province = []
        province0=[]#同省份数据合并
        p=set()#判断是否遇到省份
        confirm = []
        confirm0=[]
        suspect = []
        suspect0=[]
        dead = []
        dead0=[]
        heal = []
        heal0=[]
        self.province = []
        for data in self.datas:
            name.append(data.get('name'))
            province.append(data.get('province'))
            confirm.append(0 if data.get('confirm')==None else data.get('confirm'))
            suspect.append(0 if data.get('suspect')==None else data.get('suspect'))
            dead.append(0 if data.get('dead')==None else data.get('suspect'))
            heal.append(0 if data.get('heal')==None else data.get('heal'))
        self.province=list(zip(province,name,confirm,suspect,dead,heal))

def Write2Excel(header,data,sheetname):
    worksheet=workbook.add_sheet(sheetname)#创建表
    for j in range(len(header)):
        worksheet.write(1,j+1,label=header[j])#写入标题（行，列，内容）
    for i in range(len(data)):#每一天
        for j in range(len(header)):#每一部分
            worksheet.write(i+2,j+1,label=data[i][j])

if __name__=='__main__':
    #data1=Tencent()
    data2=Dxy()
    data3=Netease()
    workbook=xlwt.Workbook(encoding='utf-8')#创建book
    Write2Excel(data1.header,data1.daily_increase,'腾讯全国新增数据')
    Write2Excel(data1.province_header, data1.province, '腾讯省份数据')
    Write2Excel(data2.province_header, data2.province,'丁香园省份数据')
    Write2Excel(data3.province_header, data3.province, '网易省份数据')
    workbook.save(r'C:\Pythonpa\CSDN-Scrapy\2019-nCoV\2019_4_23-nCoV.xls')
    print('写入完成')
