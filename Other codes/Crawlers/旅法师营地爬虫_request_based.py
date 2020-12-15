import urllib.request
import json, re, time, collections, xlwt
from lxml import etree

class hearthstone():
    def __init__(self):
        self.post=0
        self.expression=0
        self.get_source()
        self.get_comments()
        self.sorts()
    def get_source(self):
        self.postIds=list()
        url=r'https://www.iyingdi.com/rstag/get/source'
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')
        for i in range(30):
            get_dict={"tagId":"17",
                      "module":"3",
                      "system":"web",
                      "size":"30",
                      "token":"",
                      "version":"800",
                      "page":str(i),
                      "orderBy":"created desc"}
            get_string=urllib.parse.urlencode(get_dict)
            new_url=url+'?'+get_string
            with urllib.request.urlopen(new_url,timeout=60) as u:
                html=u.read().decode('utf-8')
                decoded=json.loads(html)
                for i in decoded['bbsPosts']:
                    self.postIds.append(str(i['bbsPost']['toPostId']))
    def get_comments(self):
        url = 'https://www.iyingdi.com/bbsplus/comment/list/post'
        req = urllib.request.Request(url)
        self.expressions=list()
        for postId in self.postIds:
            try:    #若网络中断自动跳过的try/except
                locker = True
                page = 0
                time.sleep(0.5)
                print("正在进入帖子"+str(postId))
                self.post+=1
                while locker:
                    try:    #爬取不同页数的try/except
                        print('正在爬取第' + str(page + 1) + '页内容')
                        get_dict = {"postId": postId, "token": "", "system": "web", "page": page}
                        get_string = urllib.parse.urlencode(get_dict)
                        new_url = url + '?' + get_string
                        with urllib.request.urlopen(new_url,timeout=60) as u:
                            time.sleep(0.3)
                            html = u.read().decode('utf-8')
                            decoded = json.loads(html)
                            if decoded['comments'] == []:
                                raise ValueError
                            #主贴
                            if page==0:
                                if decoded['post']['bbsPost']['imgs']!='':
                                    if(';' in decoded['post']['bbsPost']['imgs']):
                                        strings=re.split(';',decoded['post']['bbsPost']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.', string):
                                                self.expressions.append(string)
                                                self.expression+=1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', decoded['post']['bbsPost']['imgs']):
                                        self.expressions.append(decoded['post']['bbsPost']['imgs'])
                                        self.expression += 1
                            #评论
                            for comment in decoded['comments']:
                                if (comment['reply']!=[]):  #获取楼中楼评论
                                    self.get_comment_reply(comment)
                                if (comment['bbsComment']['imgs'] != ''):
                                    if (';' in comment['bbsComment']['imgs']):
                                        strings = re.split(';',comment['bbsComment']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.',string):
                                                self.expressions.append(string)
                                                self.expression += 1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', comment['bbsComment']['imgs']):
                                        self.expressions.append(comment['bbsComment']['imgs'])
                                        self.expression += 1
                        page += 1
                    except ValueError:
                        locker = False

            except (TimeoutError,urllib.error.URLError):
                continue

    def get_comment_reply(self,comment):
        for reply in comment['reply']:
            if (reply['bbsReply']['imgs'] != ''):
                if (';' in reply['bbsReply']['imgs'] ):
                    strings = re.split(';', reply['bbsReply']['imgs'] )
                    for string in strings:
                        if re.match('http://wspic.iyingdi.cn/expression/.', string):
                            self.expressions.append(string)
                            self.expression += 1
                elif re.match('http://wspic.iyingdi.cn/expression/.', reply['bbsReply']['imgs'] ):
                    self.expressions.append(reply['bbsReply']['imgs'] )
                    self.expression += 1

    def sorts(self):
        links=list()
        frequency=list()
        self.collect=collections.Counter(self.expressions)
        for key in self.collect.keys():
            links.append(key)
        for value in self.collect.values():
            frequency.append(value)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('炉石传说',cell_overwrite_ok=True)
        worksheet.write(0, 0, label='表情包链接')
        worksheet.write(0, 1, label='出现次数')
        worksheet.write(0, 2, label='爬取帖子数：')
        worksheet.write(0, 3, label=self.post)
        worksheet.write(1, 2, label='总计表情数：')
        worksheet.write(1, 3, label=self.expression)
        for i in range(len(links)):
            worksheet.write(i+1, 0, label=links[i])
            worksheet.write(i+1, 1, label=frequency[i])
        # 保存
        workbook.save('炉石传说区表情包统计.xls')
        print('成功输出至Excel')

class quint():
    def __init__(self):
        self.post=0
        self.expression=0
        self.get_source()
        self.get_comments()
        self.sorts()
    def get_source(self):
        self.postIds=list()
        url=r'https://www.iyingdi.com/rstag/get/source'
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')
        for i in range(20):
            get_dict={"tagId":"19",
                      "module":"3",
                      "system":"web",
                      "size":"30",
                      "token":"",
                      "version":"800",
                      "page":str(i),
                      "orderBy":"created desc"}
            get_string=urllib.parse.urlencode(get_dict)
            new_url=url+'?'+get_string
            with urllib.request.urlopen(new_url,timeout=60) as u:
                html=u.read().decode('utf-8')
                decoded=json.loads(html)
                for i in decoded['bbsPosts']:
                    self.postIds.append(str(i['bbsPost']['toPostId']))
    def get_comments(self):
        url = 'https://www.iyingdi.com/bbsplus/comment/list/post'
        req = urllib.request.Request(url)
        self.expressions=list()
        for postId in self.postIds:
            try:    #若网络中断自动跳过的try/except
                locker = True
                page = 0
                time.sleep(0.5)
                print("正在进入帖子"+str(postId))
                self.post+=1
                while locker:
                    try:    #爬取不同页数的try/except
                        print('正在爬取第' + str(page + 1) + '页内容')
                        get_dict = {"postId": postId, "token": "", "system": "web", "page": page}
                        get_string = urllib.parse.urlencode(get_dict)
                        new_url = url + '?' + get_string
                        with urllib.request.urlopen(new_url,timeout=60) as u:
                            time.sleep(0.3)
                            html = u.read().decode('utf-8')
                            decoded = json.loads(html)
                            if decoded['comments'] == []:
                                raise ValueError
                            #主贴
                            if page==0:
                                if decoded['post']['bbsPost']['imgs']!='':
                                    if(';' in decoded['post']['bbsPost']['imgs']):
                                        strings=re.split(';',decoded['post']['bbsPost']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.', string):
                                                self.expressions.append(string)
                                                self.expression+=1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', decoded['post']['bbsPost']['imgs']):
                                        self.expressions.append(decoded['post']['bbsPost']['imgs'])
                                        self.expression += 1
                            #评论
                            for comment in decoded['comments']:
                                if (comment['reply']!=[]):  #获取楼中楼评论
                                    self.get_comment_reply(comment)
                                if (comment['bbsComment']['imgs'] != ''):
                                    if (';' in comment['bbsComment']['imgs']):
                                        strings = re.split(';',comment['bbsComment']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.',string):
                                                self.expressions.append(string)
                                                self.expression += 1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', comment['bbsComment']['imgs']):
                                        self.expressions.append(comment['bbsComment']['imgs'])
                                        self.expression += 1
                        page += 1
                    except ValueError:
                        locker = False

            except (TimeoutError,urllib.error.URLError):
                continue

    def get_comment_reply(self,comment):
        for reply in comment['reply']:
            if (reply['bbsReply']['imgs'] != ''):
                if (';' in reply['bbsReply']['imgs'] ):
                    strings = re.split(';', reply['bbsReply']['imgs'] )
                    for string in strings:
                        if re.match('http://wspic.iyingdi.cn/expression/.', string):
                            self.expressions.append(string)
                            self.expression += 1
                elif re.match('http://wspic.iyingdi.cn/expression/.', reply['bbsReply']['imgs'] ):
                    self.expressions.append(reply['bbsReply']['imgs'] )
                    self.expression += 1

    def sorts(self):
        links=list()
        frequency=list()
        self.collect=collections.Counter(self.expressions)
        for key in self.collect.keys():
            links.append(key)
        for value in self.collect.values():
            frequency.append(value)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('昆特牌',cell_overwrite_ok=True)
        worksheet.write(0, 0, label='表情包链接')
        worksheet.write(0, 1, label='出现次数')
        worksheet.write(0, 2, label='爬取帖子数：')
        worksheet.write(0, 3, label=self.post)
        worksheet.write(1, 2, label='总计表情数：')
        worksheet.write(1, 3, label=self.expression)
        for i in range(len(links)):
            worksheet.write(i+1, 0, label=links[i])
            worksheet.write(i+1, 1, label=frequency[i])
        # 保存
        workbook.save('昆特区表情包统计.xls')
        print('成功输出至Excel')

class magic():
    def __init__(self):
        self.post=0
        self.expression=0
        self.get_source()
        self.get_comments()
        self.sorts()
    def get_source(self):
        self.postIds=list()
        url=r'https://www.iyingdi.com/rstag/get/source'
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')
        for i in range(20):
            get_dict={"tagId":"18",
                      "module":"3",
                      "system":"web",
                      "size":"30",
                      "token":"",
                      "version":"800",
                      "page":str(i),
                      "orderBy":"created desc"}
            get_string=urllib.parse.urlencode(get_dict)
            new_url=url+'?'+get_string
            with urllib.request.urlopen(new_url,timeout=60) as u:
                html=u.read().decode('utf-8')
                decoded=json.loads(html)
                for i in decoded['bbsPosts']:
                    self.postIds.append(str(i['bbsPost']['toPostId']))
    def get_comments(self):
        url = 'https://www.iyingdi.com/bbsplus/comment/list/post'
        req = urllib.request.Request(url)
        self.expressions=list()
        for postId in self.postIds:
            try:    #若网络中断自动跳过的try/except
                locker = True
                page = 0
                time.sleep(0.5)
                print("正在进入帖子"+str(postId))
                self.post+=1
                while locker:
                    try:    #爬取不同页数的try/except
                        print('正在爬取第' + str(page + 1) + '页内容')
                        get_dict = {"postId": postId, "token": "", "system": "web", "page": page}
                        get_string = urllib.parse.urlencode(get_dict)
                        new_url = url + '?' + get_string
                        with urllib.request.urlopen(new_url,timeout=60) as u:
                            time.sleep(0.3)
                            html = u.read().decode('utf-8')
                            decoded = json.loads(html)
                            if decoded['comments'] == []:
                                raise ValueError
                            #主贴
                            if page==0:
                                if decoded['post']['bbsPost']['imgs']!='':
                                    if(';' in decoded['post']['bbsPost']['imgs']):
                                        strings=re.split(';',decoded['post']['bbsPost']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.', string):
                                                self.expressions.append(string)
                                                self.expression+=1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', decoded['post']['bbsPost']['imgs']):
                                        self.expressions.append(decoded['post']['bbsPost']['imgs'])
                                        self.expression += 1
                            #评论
                            for comment in decoded['comments']:
                                if (comment['reply']!=[]):  #获取楼中楼评论
                                    self.get_comment_reply(comment)
                                if (comment['bbsComment']['imgs'] != ''):
                                    if (';' in comment['bbsComment']['imgs']):
                                        strings = re.split(';',comment['bbsComment']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.',string):
                                                self.expressions.append(string)
                                                self.expression += 1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', comment['bbsComment']['imgs']):
                                        self.expressions.append(comment['bbsComment']['imgs'])
                                        self.expression += 1
                        page += 1
                    except ValueError:
                        locker = False

            except (TimeoutError,urllib.error.URLError,KeyError):
                continue

    def get_comment_reply(self,comment):
        for reply in comment['reply']:
            if (reply['bbsReply']['imgs'] != ''):
                if (';' in reply['bbsReply']['imgs'] ):
                    strings = re.split(';', reply['bbsReply']['imgs'] )
                    for string in strings:
                        if re.match('http://wspic.iyingdi.cn/expression/.', string):
                            self.expressions.append(string)
                            self.expression += 1
                elif re.match('http://wspic.iyingdi.cn/expression/.', reply['bbsReply']['imgs'] ):
                    self.expressions.append(reply['bbsReply']['imgs'] )
                    self.expression += 1

    def sorts(self):
        links=list()
        frequency=list()
        self.collect=collections.Counter(self.expressions)
        for key in self.collect.keys():
            links.append(key)
        for value in self.collect.values():
            frequency.append(value)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('万智牌',cell_overwrite_ok=True)
        worksheet.write(0, 0, label='表情包链接')
        worksheet.write(0, 1, label='出现次数')
        worksheet.write(0, 2, label='爬取帖子数：')
        worksheet.write(0, 3, label=self.post)
        worksheet.write(1, 2, label='总计表情数：')
        worksheet.write(1, 3, label=self.expression)
        for i in range(len(links)):
            worksheet.write(i+1, 0, label=links[i])
            worksheet.write(i+1, 1, label=frequency[i])
        # 保存
        workbook.save('万智牌表情包统计.xls')
        print('成功输出至Excel')

class shadow():
    def __init__(self):
        self.post=0
        self.expression=0
        self.get_source()
        self.get_comments()
        self.sorts()
    def get_source(self):
        self.postIds=list()
        url=r'https://www.iyingdi.com/rstag/get/source'
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')
        for i in range(20):
            get_dict={"tagId":"20",
                      "module":"3",
                      "system":"web",
                      "size":"30",
                      "token":"",
                      "version":"800",
                      "page":str(i),
                      "orderBy":"created desc"}
            get_string=urllib.parse.urlencode(get_dict)
            new_url=url+'?'+get_string
            with urllib.request.urlopen(new_url,timeout=60) as u:
                html=u.read().decode('utf-8')
                decoded=json.loads(html)
                for i in decoded['bbsPosts']:
                    self.postIds.append(str(i['bbsPost']['toPostId']))
    def get_comments(self):
        url = 'https://www.iyingdi.com/bbsplus/comment/list/post'
        req = urllib.request.Request(url)
        self.expressions=list()
        for postId in self.postIds:
            try:    #若网络中断自动跳过的try/except
                locker = True
                page = 0
                time.sleep(0.5)
                print("正在进入帖子"+str(postId))
                self.post+=1
                while locker:
                    try:    #爬取不同页数的try/except
                        print('正在爬取第' + str(page + 1) + '页内容')
                        get_dict = {"postId": postId, "token": "", "system": "web", "page": page}
                        get_string = urllib.parse.urlencode(get_dict)
                        new_url = url + '?' + get_string
                        with urllib.request.urlopen(new_url,timeout=60) as u:
                            time.sleep(0.3)
                            html = u.read().decode('utf-8')
                            decoded = json.loads(html)
                            if decoded['comments'] == []:
                                raise ValueError
                            #主贴
                            if page==0:
                                if decoded['post']['bbsPost']['imgs']!='':
                                    if(';' in decoded['post']['bbsPost']['imgs']):
                                        strings=re.split(';',decoded['post']['bbsPost']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.', string):
                                                self.expressions.append(string)
                                                self.expression+=1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', decoded['post']['bbsPost']['imgs']):
                                        self.expressions.append(decoded['post']['bbsPost']['imgs'])
                                        self.expression += 1
                            #评论
                            for comment in decoded['comments']:
                                if (comment['reply']!=[]):  #获取楼中楼评论
                                    self.get_comment_reply(comment)
                                if (comment['bbsComment']['imgs'] != ''):
                                    if (';' in comment['bbsComment']['imgs']):
                                        strings = re.split(';',comment['bbsComment']['imgs'])
                                        for string in strings:
                                            if re.match('http://wspic.iyingdi.cn/expression/.',string):
                                                self.expressions.append(string)
                                                self.expression += 1
                                    elif re.match('http://wspic.iyingdi.cn/expression/.', comment['bbsComment']['imgs']):
                                        self.expressions.append(comment['bbsComment']['imgs'])
                                        self.expression += 1
                        page += 1
                    except ValueError:
                        locker = False

            except (TimeoutError,urllib.error.URLError,KeyError):
                continue

    def get_comment_reply(self,comment):
        for reply in comment['reply']:
            if (reply['bbsReply']['imgs'] != ''):
                if (';' in reply['bbsReply']['imgs'] ):
                    strings = re.split(';', reply['bbsReply']['imgs'] )
                    for string in strings:
                        if re.match('http://wspic.iyingdi.cn/expression/.', string):
                            self.expressions.append(string)
                            self.expression += 1
                elif re.match('http://wspic.iyingdi.cn/expression/.', reply['bbsReply']['imgs'] ):
                    self.expressions.append(reply['bbsReply']['imgs'] )
                    self.expression += 1

    def sorts(self):
        links=list()
        frequency=list()
        self.collect=collections.Counter(self.expressions)
        for key in self.collect.keys():
            links.append(key)
        for value in self.collect.values():
            frequency.append(value)
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('影之诗',cell_overwrite_ok=True)
        worksheet.write(0, 0, label='表情包链接')
        worksheet.write(0, 1, label='出现次数')
        worksheet.write(0, 2, label='爬取帖子数：')
        worksheet.write(0, 3, label=self.post)
        worksheet.write(1, 2, label='总计表情数：')
        worksheet.write(1, 3, label=self.expression)
        for i in range(len(links)):
            worksheet.write(i+1, 0, label=links[i])
            worksheet.write(i+1, 1, label=frequency[i])
        # 保存
        workbook.save('影之诗表情包统计.xls')
        print('成功输出至Excel')

def main():
    hs=hearthstone()
    qn=quint()
    mg=magic()
    sv=shadow()
if __name__=="__main__":
    main()
