import re,json,time,shutil,os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class Blackboard():
    def __init__(self,driver,username,password):
        self.driver=driver
        self.username=username
        self.password=password
        self.Get_CourseList()
        self.Download()

    def Announcement(self,filename,coursename):
        announcement=self.driver.find_element_by_xpath('//*[@id="announcementList"]').get_attribute('outerHTML')
        soup=BeautifulSoup(announcement,'html.parser')
        if soup.find('li',class_='clearfix'):
            self.titles=[]
            self.details=[]
            for tag in soup.find_all('li',class_='clearfix'):
                self.titles.append(tag.find('h3',class_='item').string.strip('\n').strip('\t').strip(' '))
                if tag.find('div',class_='vtbegenerated'):
                    detail=' '.join(tag.find('div',class_='vtbegenerated').get_text().split())
                    self.details.append(detail)
                else :
                    detail='该公告无详细内容'
                    self.details.append(detail)
            try:
                with open(filename,'w') as f:
                    for i in range(len(self.titles)):
                        f.writelines(self.titles[i])
                        f.writelines('\n\n')
                        f.writelines(self.details[i])
                        f.writelines('\n\n\n')
                isExists = os.path.exists('D:\Course\\'+coursename)
                if not isExists:
                    os.makedirs('D:\Course\\'+coursename)
                shutil.move(filename, 'D:\Course\\'+coursename+'\公告.txt')
                print('  课程公告下载完成')
            #如果出现gbk编码错误，就不能写入文件（未解决先跳过）
            except UnicodeEncodeError:
                print('  编码错误')
                pass
        else:
            print('  该课程暂无公告')

    def File(self,coursename):
        self.menu=self.driver.find_element_by_xpath('//*[@id="courseMenuPalette_contents"]').get_attribute('outerHTML')
        menu_soup=BeautifulSoup(self.menu,'html.parser')
        if menu_soup.find('span',title='课程文档'):
            self.driver.find_element_by_xpath('//*[@title="课程文档"]').click()
            files = self.driver.find_element_by_xpath('//*[@id="content_listContainer"]').get_attribute('outerHTML')
            file_soup = BeautifulSoup(files, 'html.parser')
            filename = []
            href = []
            #如果是正常的每格一个文件
            try:
                for tag in file_soup.find_all('div',class_='item clearfix'):
                    if re.match('/bbcswebdav', tag.find('a')['href']):
                        href.append('https://bb9.sufe.edu.cn/'+tag.find('a')['href'])
                        filename.append(tag.find('a').string)
                for i in range(0,len(href)):
                    print('  正在下载'+filename[i]+'...')
                    self.driver.get(href[i])
                templist = os.listdir('D:\Download\\')
                if len(templist)>=20:
                    time.sleep(40)
                elif len(templist)>=15:
                    time.sleep(30)
                elif len(templist)>=9:
                    time.sleep(20)
                else:
                    time.sleep(10)
            #如果一格里有好多个文件
            except TypeError:
                for tag in file_soup.find_all('li', class_='clearfix read'):
                    for item in tag.find('ul',class_='attachments clearfix').find_all('li'):
                        if re.match('/bbcswebdav', item.find('a')['href']):
                            href.append('https://bb9.sufe.edu.cn/' + item.find('a')['href'])
                for i in range(0,len(href)):
                    print('  正在下载第'+str(i+1)+'个文件...')
                    self.driver.get(href[i])
                templist = os.listdir('D:\Download\\')
                if len(templist)>=20:
                    time.sleep(40)
                elif len(templist)>=15:
                    time.sleep(30)
                elif len(templist)>=9:
                    time.sleep(20)
                else:
                    time.sleep(10)

            isExists = os.path.exists('D:\Course\\' + coursename)
            if not isExists:
                os.makedirs('D:\Course\\' + coursename)
            filelist = os.listdir('D:\Download\\')
            for files in filelist:
                filename="D:\Download\\"+files
                shutil.move(filename, 'D:\Course\\' + coursename + '\\'+files)
            print('    课程文档下载完成')
        else:print('  该课程暂无文档')

    def Get_CourseList(self):
        self.driver.get('https://bb9.sufe.edu.cn/webapps/login/')
        print('正在登录...')
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="user_id"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="login"]/table/tbody/tr[3]/td[2]/input').click()
        time.sleep(3)
        html=self.driver.find_element_by_xpath('//*[@id="_3_1termCourses_noterm"]/ul').get_attribute("outerHTML")
        soup=BeautifulSoup(html,'html.parser')
        print('正在获取课程信息...')
        self.name=[]
        #self.url=[]
        for tag in soup.find_all('li'):
            if tag.find('a',target='_top'):
                self.name.append(tag.find('a',target='_top').string)
                #self.url.append(tag.find('a',target='_top').get('href'))

    def Download(self):
        for i in range(0,len(self.name)):
            print(str.format('[{}] {}',i+1,self.name[i]))
        num=input('请输入要下载的课程序号，全部下载请输入0：')
        if num=='0':
            for i in range(1,len(self.name)):
                print()
                print('正在访问'+self.name[i-1]+'...')
                filename = 'D:\Download\\' + self.name[i-i] + '.txt'
                self.driver.find_element_by_xpath('//*[@id="_3_1termCourses_noterm"]/ul/li['+str(i)+']/a').click()
                time.sleep(2)
                self.Announcement(filename,self.name[i-1])
                self.File(self.name[i-1])
                self.driver.get('https://bb9.sufe.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1')
                time.sleep(2)
        else:
            print()
            print('正在访问'+self.name[int(num)-1]+'...')
            filename='D:\Download\\'+self.name[int(num)-1]+'.txt'
            self.driver.find_element_by_xpath('//*[@id="_3_1termCourses_noterm"]/ul/li['+num+']/a').click()
            time.sleep(2)
            self.Announcement(filename,self.name[int(num)-1])
            self.File(self.name[int(num)-1])

class Chrome():
    def __init__(self):
        self.Settings()
    def Settings(self):
        chrome_options = webdriver.ChromeOptions()
        isExists = os.path.exists('D:\Download')
        if not isExists:
            os.makedirs('D:\Download')
        prefs = {"download.default_directory": r"D:\Download", "download.prompt_for_download": False,
                 "plugins.always_open_pdf_externally": True}
        #禁止pdf,flash插件
        profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],"plugins.plugins_disabled": ['Adobe Flash Player']}
        chrome_options.add_experimental_option("prefs", profile)
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ['ignore-certificate-errors'])
        # 无头模式会出错...
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(options=chrome_options)

def main():
    username = input('请输入NetID：')
    password = input('请输入密码：')
    print('正在配置Chrome Driver...\n')
    chrome=Chrome()
    bb=Blackboard(chrome.driver,username,password)

if __name__=='__main__':
    main()