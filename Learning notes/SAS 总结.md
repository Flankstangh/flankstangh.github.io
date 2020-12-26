# SAS 总结

作者：Flankstan

**文章的代码高亮有问题，因为 Markdown 并没有 SAS 语法高亮的 CSS，所以默认使用了 Python 关键词高亮，但影响不大**

[TOC]

## 一、DATA 步总结

### （一）导入数据

<span id='input'>
#### 1-1 DATA INPUT 语句
基本形式：
```SAS
data xyz;
    input varlist formatlist;
datalines;
1 2 3 4 5
6 7 8 9 10
;
run;
```
##### > 导入数据时的 @ 和 @@

- @ 一个数据步可以包含多条 input语句。对于多条 input 语句，若前一条 input 语句执行完时，一般情况下下一条 input 会直接跳到另一个数据行。在前一个 input 语句后加 @ 表示要保留本条数据行的数据供下一个 input 使用。

- @@ 当原始文件中一个数据行含有多个观测的时候，应在 input 语句使用 @@，这样程序执行到下一个 input 语句，甚至下一个迭代时，都不释放输入缓冲区中的记录，input 语句会继续从输入缓冲区读取数据值，直到 input 读完缓冲区中所有的数据为止。

示例：
```SAS 
data test;
	input x @;   #读取x后，读取y为本行的下一个数字
	input y;     #读取y后，跳到下一行
	input z @@;  #读取z后，读取下一循环的x为本行的下一个数字
datalines;
1 2 3 4 5 6
7 8 9 10 11 12
13 14 15 16 17 
18;
run;
```
最终输出结果为：
|x|y|z|
|---|---|---|
|1|2|7|
|8|9|13|
|14|15|18|

</span>

---

#### 1-2 DATA INFILE 语句
```SAS
data xyz;
    infile 'xyz.csv';
    input var1 $18.     #格式$w.表示生成字符型变量
          var2 5.2      #格式w.d表示读取数值型变量
          var3 format3;
    dlm=','             #数据的分隔符，可以为空格外任何符号
    firstobs=2          #从第二行开始读取
             DSD        #忽略引号中的分隔符，两个连续分隔符视为缺失值
             missover   当一行数据不够时视为缺失
    obs=100             #读取100行数据
run;
```

---
#### 1-3 PROC IMPORT 语句
[详见 PROC 步总结 2-1：PROC IMPORT](#import)

---


#### 1-4 数据合并

##### > 使用 set 纵向合并
set 语句可以纵向拼接多张表，当子数据集变量不完全相同时，合并数据集中会出现空值：
```SAS
data COMBINED;          #合并后新数据集
    set DATA1 DATA2;    #原始数据集
run;
```
<center>
![image][1]
</center>

图片链接：https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190318143433680-1808221835.png （因为图可能会挂）

<span id="merge">
##### > 使用 merge 横向合并
1. 不使用 by 的情况下为一对一合并：
```SAS
data COMBINED;
    merge DATA1 DATA2;
run;
```
<center>
![image][2]
</center>

图片链接：https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190319143139332-2122073094.png

2. 使用 by 的情况下为匹配合并：
```SAS
data COMBINED;
    merge DATA1 DATA2;
    by YEAR;
run;
```
<center>
![image][3]
</center>

图片链接：https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190319143145018-1303102093.png

</span>

##### > 左连接、右连接、内连接、全连接
在使用合并数据集时，可以使用 in= 选项控制数据来源：
```SAS
data COMBINED;
    merge DATA1(in=da1) DATA2(in=da2);
    by var;
    if da1;         #左连接，只使用DATA1已存在的观测数据
    if da2;         #右连接，只使用DATA2已存在的观测数据
    if da1 and da2; #内连接，只使用两个数据集中都有的观测数据
    if da1 or da2;  #全连接，使用两个数据集中的所有观测数据
run;
```

---

### （二）数据处理

#### 2-1 SAS 函数

##### > 常用 SAS 字符函数
|函数名|功能|
|---|---|
|ANYALNUM(arg,start)|返回首次出现任意字母或数字的位置，可以选择起始查找位置 |
|ANYALPHA(arg,start)|返回首次出现任意字母的位置，可选择起始查找位置|
|CATS(arg,start)|连接两个或多个字符串，移除首尾全部空格|
|CAT(arg,start)|连接两个或多个字符串，移除首尾全部空格|
|COMPRESS(art,“char”)|移除字符串中的空格或者可选字符|
|LEFT(arg)| 将字符串左对齐|
|LENGTH(arg)|返回字符串长度，不考虑尾部空格，缺失值长度为1|
|SUBSTR(arg,position,n)|从position位置开始提取长度为n的字串|
|TRIM(arg)|移除字符串尾部全部空格|
|UPCASE(arg)|把参数中所有的字母转换成大写|
|LOWCASE(arg)|把参数中所有的字母转换成小写|

##### > 常用 SAS 数值函数
|函数名|功能|
|---|---|
|INT|返回参数的整数部分|
|LOG|返回自然对数|
|LOG10|返回底数为10的自然对数|
|MAX|返回最大的非缺失值|
|MEAN|返回非缺失值的算术平均值|
|MIN|返回最小的非缺失值|
|N|返回非缺失值的个数|
|ROUND|返回按指定精度四舍五入后的值|
|SUN|返回非缺失值得和|


##### > LAG 和 DIF
```SAS
# lagX(var) 函数可以查看之前X行var变量的观测值
pre1name=lag1(name); 
pre2name=lag2(name);
pre3name=lag3(name);

# difX(var) 函数可以计算var变量当前行和之前X行观测值的差
# difX(var)=var-lagX(var)
diff1sat=dif1(sat); 
diff1sat=dif2(sat); 
diff1sat=dif3(sat); 
```


---


#### 2-2 数据筛选

##### > IF 和 WHERE

主要区别：

1. IF 是语句，WHERE 可以是语句，也可以在选项里。
2. 从效率上讲，WHERE 更高效。
3. 从使用范围上讲，WHERE 更广泛，不仅可以在 DATA 步，也可以在 PROC 步工作，还可以在数据集中作为选项，而 IF 只能作为 DATA 步语句使用。
4. IF 语句对 INPUT 语句创建的观测有效，但是 WHERE 语句只能筛选数据集里的观测值。
5. 当有 BY 语句时， IF 语句与 WHERE 语句的结果可能会不同，因为 SAS 创建 BY 组在 WHERE 语句之后，IF 语句之前。
6. IF 语句可以在条件 IF 语句中，但 WHERE 语句不行。
7. 当读入多个数据集时，IF 语句无法针对每个数据集单独筛选，但是 WHERE 选项可以。

示例：

```SAS
#第一阶段：打开数据集时只读取所需要的观测
data class4_2; 
    set libref.sat_raw_a (where=(sex="F"));
run; 

#第二阶段：PDV里筛选过滤观测
data class4_2; 
    set libref.sat_raw_a; 
    where sex="f";
run; 

data class4_2; 
    set libref.sat_raw_a; 
    if sex="f";
run; 

#第三阶段： 通过WHERE选项限定输出数据集
data class4_2(where=(sex="f")); 
    set libref.sat_raw_a; 
run; 

```
---

##### > KEEP/DROP 和 RENAME

1. 在数据集读入和输出阶段，数据集选项里执行顺序是固定的，与选项书写的顺序无关。
2. 在数据读入和输出阶段执行顺序是：
    （1）KEEP/DROP （2）RENAME （3) WHERE 筛选观测。
3. 在编程处理阶段，执行顺序是：
    （1）WHERE选项筛选观测 （2）其它执行语句 （3） KEEP/DROP选项筛选变量        （4）RENAME 选项修改变量名

---

#### 2-3 循环结构
循环结构主要有三种：
```SAS
#DO循环
data random; 
	do i=1 to 5; 
	    output; 
    end;
run;

#DO-WHILE循环
data dowhile_example; 
	i=0; 
	do while(i<5);
    	i+1;
    	output; 
    end; 
run; 

#DO-UNTIL循环
data dountil_example;
	i=0;
	do until(i>=5);
    	i+1;
    	output; 
    end; 
run; 
```

##### DO-WHILE 和 DO-UNTIL
- DO-WHILE语句：与DO循环语句每次按照指示变量的值去执行不同，DO-WHILE语句会先判断是否满足条件，如果满足则执行否则跳出循环。
- DO-UNTIL语句：与DO-WHILE语句会先判断是否满足条件不同，DO-UNTIL语句，初始不去判断条件，先执行了语句再在结尾判断。

---

### （三）数据格式

#### 3-1 INPUT 函数和 PUT 函数
- input 函数将字符变量转换为数值变量，通过指定的informat读取数据源的数据值。

<center>**INPUT(Source, Informat)**</center>
```SAS
data input;
	character = '18.002';
	number=character*1;     #字符数字变量*1可以快速转为数值变量
	number2=input(character,best12.);   #Informat是字符的格式
	output;
	character = '$18.00';   #但非数字字符变量不能这样转换
	number=character*1;
	number2=input(character,dollar12.);
	output;
run;
```
重点：
1. informat 决定/判断结果是字符型还是数值型;决定读取值的长度(或宽度 width )；
2. 新生成的变量的长度，by default 取决于第一个 argument 的宽度。

- put 函数将数值变量转换成字符变量。

<center>**PUT(Source , Format)**</center>
```SAS
data put;
	number=18.002;
	put=strip(put(number,best12.)); #Format是转换后数值的格式
run;
```
重点： 
1. 如果新生成的变量没有特别指定长度，变量的长度由 format 决定。
2. 和 input 函数一样，put 函数不可以直接将原来的变量更改属性，但是可以生成一个新变量，在生成新变量的过程中，将变量属性改变。
3. 将数值变量改写为字符变量，自动更改的方式是使用 best12. ,产生的结果自动左对齐。


----

#### 3-2 常用格式

##### > 常用输入格式
|类别| 格式名 |作用|
|---|---|---|
|字符 | $w.| 标准字符格式 |
|| \$CHARw.| 读入带入空格的字符|
|     |ANYDTDTEw.|“万能”读入日期格式 |
|     |ANYDTTMEw.|“万能”读入日期时间格式 |
|     |ANYDTTMEw. |“万能”读入时间格式 |
|   |DATEw. |读入格式为ddmmmyy或者ddmmmyy的日期 |
|数字 |COMMAw.d |读入数字时移除数字间的字符 |
|     |w.D| 读入标准数字格式 |
|     |PERCENTw.d |读入百分比数字 |
|日期时间 |DATETIMEw.| 读入格式为ddmmmyy hh:mm:ss:ss或者 ddmmmyyyy hh:mm:ss:ss的日期时间 |
|     |DDMMYYw. |读入格式为ddmmyy<yy>或者dd-mm-yy<yy>格式的日期，中间连接字符可以是-，.或者/ |
|   |  MMDDYYw.d |读入格式为mmddyy或者mmddyy的日期 |

##### > 常用输出格式
|类别| 格式名 |作用|
|---|---|---||
|字符| $w. |标准字符格式，w表示变量的宽度。 |
| |\$UPCASEw.| 把字符转成大写，相当于UPCASE函数。 |
|数字 |BESTw.| SAS 自动选择最合适的数字格式 |
| |COMMAw.d |带千分位的数字格式 |
| |DOLLARw.d| 带美元符号的格式 |
| |PERCENTw.d| 显示百分比形式 |
| |PVALUEw.d| 统计P值显示格式 |
| |w.d |标准的数字格式 |
| |Zw.d |前面位数不够补0填充 |
|时间日期 |DATETIMEw.d| 显示日期时间格式为ddmmyy:hh:mm:ss:ss |
| |DATEw. |显示日期格式为ddmmyy |

##### > 部分格式详细说明
|格式名 |举例 |输入值|保存值|
|---|---|---|---|
| \$w. | \$5.00 | 'ABCDE'| 'ABCDE' |
| \$UPCASEw. | \$UPCASE5. |'aBcDe'| 'ABCDE' |
|w.d |5.3| 1.2345 |1.235 |
|BESTw.| BEST6. |1235000 |1.24E+06 |
|COMMAw.d| COMMA11.1| 1000000| 1,000,000.10 |
|DOLLARw.d| DOLLAR13.2 |1000000 |$1,000,000.01  |
|PERCENTw.d| PERCENT8.2| -0.12345| -12.35% |


- **$w.** : 表示储存至多 w 个字符
- **w.d** : w 表示数值总共的宽度，小数点、负号都算一位，d 表示小数点后的位数
- **bestw.** : 和 w.d 类似，只是可以储存更多位数
- **commaw.d** : 将数值以逗号分隔


##### > 自定义格式
[详见 PROC 步总结 3-3：PROC FORMAT](#format)

---

### （四）数组
数组的定义格式如下：
```SAS
ARRAY array-name[k,n] <$> <Length> <elements> <initial value list>;
```
    # array-name：数组的名称，在调用时使用，不进入数据集
    # k：数组的维数，缺省默认为1
    # n：数组元素的个数，可以为数如[8]; 数字范围，如[1:7}; [*]表示自动计数
    # elements：元素名可以是变量名，也可以是SAS自定义的变量
    
定义示例：
```SAS
#定义一维数组
array sbp[7] sbp1-sbp7; 
array dbp[1:7] dbp1-dbp7;

#定义数组时包含元素值
array sbp[1:7] sbp1-sbp7 (163 164 167 171 155 158 154); 
array dbp[7] dbp1-dbp7 (98 99 92 94 95 93 93); 

#定义二维数组
array bp[2, 1:7] sbp1-sbp7 
                 dbp1-dbp7; 
array bp[2, 5] sbp1-sbp5 (164 164 167 171 125) 
               aa bb cc dd ee (164 164 167 171 119); #元素名不必类似
```

---

## 二、PROC 步总结

> 各种问题都可查文档：[SAS Procedure Documentation Guide](https://documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.5&docsetId=proc&docsetTarget=titlepage.htm&locale=en)


### （一）PROC 的基本形式
所有过程步都可选的选项，作用也都类似：
```SAS
proc procedure data=work.xyz         #PROC步处理的对象集
               <out=work.abc>        #生成新数据集的路径合名称
               <noprint>             #不打印报告，一般配合OUT=选项
               <noobs>               #不打印观测值序号
               <options(sub options)> #options也可以有子选项
               <other options>;       #<>中为可选选项
               
    #变量相关options：
    id var1;                #将var1作为数据报告的行索引
    var var2;               #除了var1外，输出报告中还保留var2
    where var2 statement    #保留var2满足statement的观测值
    by var3;                #对var3进行单独分析，必须先proc sort
    label var2='VAR2'       #为变量增加标签，仅在这个proc步有效
    #输出报告相关options：
    title 'This is a title' #修改报告的标题
    footnote 'A footnote'   #增加报告脚注
    <other specific options>
run;
```

-----

### （二）数据处理过程步
<span id='import'>
#### 2-1. **PROC IMPORT***
从外部文件导入数据：
```SAS
proc import out=work.xyz        
            datafile='xyz.xlsx' #导入数据文件的路径和名称
            dbms=excel replace; #常用DBMS：EXCEL\CSV\DTA\DLM
            
    sheet='sheetname';  #导入EXCEL文件时输入sheet名
    delimter='20'x      #导入txt文件（DBMS=DLM）选项，分隔符为空格
    getnames=yes;       #将第1行设置为变量名
    datarow=3;          #从第3行开始读取数据（和getnames不冲突）
    guessingrows=20;    #根据前20行判断数据的informat
    mixed=yes;          #如果一列中同时有数字和字符，则将数字转为字符
    usedate=yes;        #使用日期格式，默认为NO，表示使用日期时间格式
run;    
```
</span>
##### > DATA 步相似过程

[详见 DATA 步总结 1-1：DATA INPUT](#input)

---

#### 2-2. **PROC SORT***
按照某个变量的一定次序为观测值排序：
```SAS
proc sort data=work.xyz     
          <out=work.xyz>     
          <sortseq=ASCII>   #按照ASCII排序，可选EBCDIC\linguistic
          <nodupkey>        #去除重复关键变量的其余观测，保留一个
          <dupout=abc>      #nodupkey情况下，将重复变量观测输出至abc
          <nouniquekey>     #去除关键变量唯一的观测
          <uniqueout=def>   #nouniquekey情况下，将唯一变量观测输出def
          <equals>          #对于关键变量重复的观测，保留相对次序
          
    by <descending> var1 var2...    #降序依次按照var1、var2排序
run;
```
##### > 对 **sortseq=** 选项的补充说明
|选项|子选项|排列顺序|
|:---|---|---|
|ASCII||空格 数字 大写字母 小写字母|
|EBCDIC||空格 小写字母 大写字母 数字|
|linguistic|strength=primary|空格 数字 大小写字母混合|
||numeric_collation=on|空格 数字按照数值处理 大写字母 小写字母|

##### > 利用 **first.var** 和 **last.var** 进行分组计数和求和*

```SAS
proc sort data=work.abc;
    by var1     #依照要分组的变量进行排序

data work.abc;
    set work.abc;
    by var1;
    if first.var1 then do;      #到了一个新的组别
        count_var=0;            #初始化计数变量
        cumulative_var=0;       #初始化求和变量
    end;
    count_var+1;
    cumulative_var+var;
    if last.var then output;    #输出计数及求和结果
end;
```

---


#### 2-3. **PROC TRANSPOSE**
转置数据集：
``` SAS
proc transpose data=work.xyz
               <out=work.abc>
               <other options>;
    var var1 var2 var3;     #保留var1-var3进行转置
    by var1;        #以var1分组，对每一组分别转置，需提前排序
    id var1;        #以var1作为转置后变量的名称，默认为col1-col3
    idlabel var2l   #以var2作为转置后变量的label，默认无
run;
```

---

#### **2-4. PROC APPEND**
使用APPEND过程进行串接时，SAS不会处理主数据集中的观测， 而是直接将追加数据集的观测添加到主数据集最后一条观测的后面，且变量仅包含主数据集中的变量：
``` SAS
proc append base/out=work.abc   #希望增添数据的数据集，不存在则新建
            <data/new=work.xyz> #被追加进base的数据集，默认最新数据
            <force>;    #强制合并
run;
```
##### > proc append 的运行机制

proc append 先读取 base= 与 data= 选项中的各数据集的描述部分信息，看看各自变量的情况，然后才执行后面的过程：

- 变量不一致时

        1. 如果 data= 数据集中的变量 base= 数据集中没有，则整个过程不会被执行；如果有 force 选项则强制执行，并且这些在 base= 数据集中没有的变量会被删除，LOG窗口中会有提示删除了哪些变量；
        
        3. 如果 base= 数据集中的变量 data= 数据集中没有，那追加之后这些变量值被置为缺失值；

- 属性不一致时

        1. 如果两数据集相同的变量类型不一致时，则整个过程不会被执行，SAS 会报错；如果有 force 选项则强制执行，以 base= 数据集的类型为准，data= 中相应变量值被置为缺失值；
        
        2. 如果两数据集相同的变量长度不一致时，base= 数据集中的变量长度大于 data= 数据集中的变量，则正常执行；如果长度小于，则过程不会被执行，除非有 force 选项，则将多余的字符截断；
        
        3. 两数据集相同的变量其他属性不一致，如输入输出格式、标签等都以 base= 数据集中的为准。

##### > DATA 步的相似过程

[**使用 set 纵向合并**](#merge)

需要注意的是，当新数据集和源数据集变量不完全相同时，proc append不会在 base 数据集生成新的变量，而data set会新生成变量。

---

#### 2-5. **PROC DATASETS**
对数据集进行处理，结果不输出，在日志中显示：
``` SAS
#基本语法
proc datasets lib=libref      #指定对work索引下的所有数据集进行处理
              <memtype=data>  #从libref中挑选的数据类型为.data
              <nolist>        #不在sas结果查看器中显示
              <kill>;         #删除该libref下的所有数据集
quit;
```
proc datasets 有以下常用方法：
``` SAS
#数据集加密和读取变量信息
proc datasets lib=work
              nolist;
              
    modify xyz (label='test'        #为数据集设定标签
                read=r2020);        #设置读取权限，密码为pw
    contents data=xyz (read=r2020); #使用密码读取数据集信息
quit;
```
``` SAS
#复制数据集
proc datasets; 
	copy in=sashelp     
	     out=work;          #将sashelp中的数据集拷贝至work
	select class cars;      #拷贝数据集class和cars
quit; 
```
``` SAS
#数据集改名
proc datasets lib=work; 
	change class=student;   #将class改名为student
quit; 
```
``` SAS
#删除和保留数据集
proc datasets lib=work; 
	delete student;    #删除student数据集
	save cars;         #只保留cars数据集，和delete只能有一个
quit;
```
```SAS
#修改数据集信息
proc datasets lib=work; 
	modify satdata;     #选定要修改的数据集为sasdata
	format sat age 3.0; 
	rename gender=sex; 
quit; 
```


##### > 利用 proc datasets 加密数据集
数据集有权限**读、写、修改、全局**四种，分别用 **READ=, WRITE=, ALTER=, PW=** 来设置。
密码格式为：_密码1/密码2_，具体组合形式有5种：

    1. 密码1：设置密码
    2. 密码1/密码2：修改密码1为密码2； 
    3. /密码2：不管旧密码是什么，设置新密码为密码2；
    4. 密码1/：删除密码
    5. /：删除密码

---

### （三）输出报告过程步
#### 3-1. **PROC CONTENTS**
打印数据集的信息：
``` SAS
proc contents data=work.xyz
              <out=work.xyz
              varnum>;      #按变量在数据集中的顺序生成报告
run;
```
---

#### 3-2. **PROC PRINT***
打印数据集的内容：
``` SAS
proc print data=work.xyz (firstobs=m obs=n)  #控制打印观测值数目 
           <noobs
           label>;         #打印标签代替变量名
            
    id var1 var2 var3;
    label var2='VAR2';
run;
```
---

<span id='format'>
#### 3-3. **PROC FORMAT***
为数据设置格式或改变数据分组：
``` SAS
#数据格式的设立
proc format <library=libref>  #将格式储存为永久格式，无其他option
    value fsmt low-<60='C'      #数值格式的转换
               60-<80='B'         
               80-100='A';   
    value $sexf '1'='male'      #字符格式的转换，字符格式名要加$
                '2'='female';    
    value color 0,4-9='other color'; #离散变量的格式表示方式
run;

#数据格式的使用
proc print data=work.xyz;
#格式后面打点才能正确输出，打点是为了区别变量名和格式名;
    format t1-t3 fsmt.; #将t1-t3变量按照fsmt的格式输出
run;
```
</span>

##### > 利用 proc format 将连续数据转为离散数据

对连续变量使用PROC FREQ等过程，系统会对每个数值进行频数统计，这在大多数情况下都不是最终想要的结果，因此要用 PROC FORMAT 将连续变量转为离散变量：
``` SAS
#一个例子
proc format;
    value height_ctg 0-50='<50'
                     50-60='50-60'
                     60-high='>60';
run;
```
---

### （四）统计分析过程步

#### 4-1. **PROC MEANS***
对数据集进行基本的统计分析：
``` SAS
proc means data=work.xyz
           <noprint
           mexdec=n #指定显示n位小数
           missing  #将缺失值视为有效
           #以下为常用统计量选项
           max      #针对每个变量，输出最大值，下同
           min      #最小值
           mean     #均值
           median   #中位数
           mode     #众数
           n        #非缺失值个数
           nmiss    #缺失值个数
           range    #极差
           std      #标准差
           var      #方差
           sum      #总和
           Q1       #第一四分位数（25%百分位）
           Q3       #第三四分位数（75%百分位）
           clm      #平均值上下95%双侧置信区间
           uclm     #平均值以上95%单侧置信区间
           lclm>;   #平均值以下95%单侧置信区间
           
    by var1;
    class var1;             #按照var1分类输出，class不需要排序
    output out=work.abc     #将结果输出至数据集，代替out= 选项
run;
```
##### > **by** 和 **class** 的区别
    by 和 class 是两个完全不同的关键字，只是在proc means里实现的效果类似。二者最直观的区别是，by 在使用前必须要经过 proc sort 排序，而 class 则不用，这种差别正体现了它们原理的不同。
    - by 语句将排序后的数据集依照变量分为多个子数据集，每一个子数据集都被视为完全独立的个体，任何 proc 步（不仅是 proc means）的操作都会在每个子数据集上重复进行，最终报告也是每组单独生成的。
    - class 语句则没有这么复杂，它只是将数据集按照关键变量分组，常用于对不同组别进行比较，比如t-检验和回归分析等，最终获得的报告也只是一份。
    
> 更详细的说明参考：[The difference between CLASS statements and BY statements in SAS](https://blogs.sas.com/content/iml/2018/02/14/difference-class-and-by-statements-sas.html)
    
--- 

#### 4-2. **PROC FREQ**
输出频数表，展示数据分布：
``` SAS 
proc freq data=work.xyz;
          <other options>
    by var1;                #根据var1分组输出多份报告
    table var2*var3/        #在每一份报告中，计算var2和var3的交叉频数
                    #以下为table关键词的options：
                    LIST            #以列表格式而非网格形式打印交叉表
                    MISSPRINT       #在频数中包括缺失值
                    MISSING         #在频数和百分比计算中包括缺失值
                    NOCOL           #不打印列百分比
                    NOPERCENT       #不打印频数百分比
                    NOROW           #不打印行百分比
                    NOCUM           #单变量时不打印累计频数
                    NOFREQ          #不打印频数
                    OUT=work.abc    #输出至数据集
run;
```

---

#### 4-3. **PROC CORR**
观察变量间的相关性：
``` SAS
proc corr <data=work.xyz>
          <nosimple>        #不进行简单描述性统计（均值方差等）
          <pearson>         #变量均服从正态分布，默认选项
          <spearman>        #变量不都服从正态分布
          <kendall>;        #有序分类变量使用的相关性检验
          
    var var1 var2 var3;     #相关性矩阵的列
    with var2 var3;         #相关性矩阵的行，没有则显示完整矩阵
    partial var4            #偏相关
run;
```
---

#### 4-4 **PROC REG**
最一般的回归分析：
``` SAS 
proc reg <data=work.xyz>
         <outest=work.abc>  #输出参数估计以及拟合统计量至数据集
         <edf>              #输出误差自由度和R2至work.abc
         <outseb>           #输出参数估计标准误
         <tableout>;        #输出参数估计标准误、置信区间和检验统计量
         
    model y=x1 x2 x3/    #回归模型，y为因变量，x1-x3为自变量
                    #以下为model关键字的options：
                    r       #输出拟合优度R2
                    clm     #输出每个观测值因变量期望值的95%置信区间
                    cli     #输出每个个体观测值的95%置信区间
run;
```

---

#### 4-5 **PROC UNIVARIATE**
对变量进行详尽的分布描述，如矩、位置和可变形的基本测度、位置检验、分位数、极值观测、用几个散点图描绘变量的分布、频数表和正态分布的检验等：

``` SAS
proc univariate data=work.xyz
                <out=work.abc>;
                
    var var1;       #指定需要进行EDA的变量
    plot-statement\<distribution curve(options>; #绘制图像
        #以下为绘图语句：
        cdfplot var1   #绘制var1的cdf图像，下同
        histogram       #绘制直方图
        probplot        #绘制概率图
        ppplot/qqplot   #绘制ppplot或qqplot
            #以下为标准分布曲线类型：
                beta        #贝塔分布
                exponential #指数分布
                gamma       #伽马分布
                lognormal   #对数正态分布
                normal      #正态分布
                weibull     #威布尔分布
                kernel      #核密度曲线
run;
```

> 每种图表的详细解释可参考：[PROC UNIVARIATE过程](https://www.cnblogs.com/immaculate/p/6371767.html)

---

### （五）SQL 过程步
不考，暂时不写了，跳过

---

## 三、MACRO 总结

### （一）宏变量
宏变量不必限定在DATA步使用，即独立于数据集的变量。分为**系统变量**和**用户自定义宏变量**，也分为**“全局宏变量”**和**“局部宏变量”**。

#### 1-1 定义宏变量
```SAS
#定义方式：
%let TIME=%sysfunc(Date());     #最一般的定义方法
%global TIME=%sysfunc(Date());  #全局宏变量
%local TIME=%sysfunc(Date());   #局部宏变量，只能用在宏程序内部
call symput("TIME",Date());     #在data步内将某个数据定义为宏变量
#宏变量中可以有SAS语句，需写在%str()中
%let print=%str(proc print; 
                run;        
                )；
#查看方式
%put &SUFE;     #在日志中显示
```

---

#### 1-2 自动宏变量
在SAS进程开始时，或程序运行过程中由系统自动创建，在SAS退出前一直保持有效。为全局宏变量，能在SAS的任何地方被使用。以下是主要的自动宏变量：
```SAS
&SYSDATE    #sas进程开始的日期
&SYSDATE9   #以Date9.格式显示SAS进程开始的日期
&SYSTIME    #SAS进程开始的时间
&SYSSCP     #使用的操作系统
&SYSVER     #SAS的版本
&SYSLAST    #最新创建的SAS数据集的名字

```
---

#### 1-3 宏变量命名规则
命名规则和一般变量一样：

- 最长32字符
- 首字符可以拉丁字母和下划线，后继的字符可是字母和下划线，还有数字符号
- 末尾空格忽略，且左对齐
- 中间不能包含空格和特殊字符（下划线除外）
- 字符大小写均可，不作区分
- 不能为SAS自动变量，如\_N_、\_ERROR_等

宏变量的值：

- 全部都是字符串，数字字符串无数值含义
- 数学表达式不进行赋值
- 可以为空
- 其中有宏变量的引用，则先解读后赋值

---

#### 1-4 引用宏变量
```SAS
#一般情况下，使用&name来引用宏变量
%let TIME=%sysfunc(date());
%put &TIME;

#当需要将宏变量和文本结合时，使用""并在宏变量后加.
%let YEAR=2020;
%put "The &YEAR.to2021 book";    #输出The 2020to2021 book
```

---

### （二）宏程序
可以包含编程语句，包括DATA步和PROC语句，可以接受宏参数。

#### 2-1 定义宏程序
```SAS
#按照其他语言函数的逻辑理解宏程序，虽然本质不一样，但效果差不多
%macro funcname(arg1, arg2);
    proc print;
    run;
    other function statements;
%mend funcname;

#这样写和Python逻辑类似
def funcname(arg1, arg2)
    function statements

#实际调用时
&funcname(arg1, arg2);
#对比Python
funcname(arg1, arg2)
```
用%MACRO开头，用%END结尾。
使用宏程序：用%+宏程序。

---

#### 2-2 嵌套调用
```SAS
#宏程序可以嵌套调用
data score; 
	input math phy eng @@; 
	datalines; 
	87 67 87 78 96 84 95 69 65
	;
run;

%macro data; 
	data temp; 
		set score; 
	run; 
%mend data; 

%macro plot; 
	proc plot; 
		plot &math*&phy;  #这里使用宏参数，因为%link传入了参数，不用也行
	run; 
%mend plot; 

%macro link(math, phy); 
	%data   #调用时就直接用&name
	%plot   #和函数不一样的是，内部调用的宏程序不需要传入参数
%mend link; 
```

---


#### 2-3 %IF-%ELSE 和 IF-ELSE

带有 % 的关键字组成的语句是宏语句。宏语句让 SAS 在 PROC 和 DATA 之外的其他位置（宏程序内、开放代码区域）也可以进行逻辑处理，提高了效率。
```SAS
# %if-%else可以在宏程序内、data步外使用
%macro func(key);
    %if &key=print %then %do;
        proc print;
        run;
    %end;
    %if &key=mean %then %do;
        proc mean;
        run;
    %end;
%mend func;

#上面的程序等价于（这一段也可以用%if-%else)
%macro func(key);
    data _null_;
        if key=print then do;
            proc print;
            run;
        end;
        if key=mean then do;
            proc mean;
            run;
        end;
    run;
%mend func;
```
%DO-%TO/ %WHILE/ %UNTIL 语句也是类似的

##### > 补充 %SYSFUNC + %IFC
但是%if-%else 还是不能在宏程序外用，如果要想在宏程序外进行判断，需要用 %sysfunc + %ifc 两个宏函数：
```SAS
options nosource2;
%Put option source2 is
%sysfunc(ifc(%sysfunc(getoption(source2)) eq SOURCE2
        ,True
        ,False
        ,Missing
        ));
```
更详细介绍参见 [相关的 SAS Documentation](https://support.sas.com/resources/papers/proceedings09/054-2009.pdf)

---

#### 2-4 一些宏程序模板
留作备用：

##### > 导出数据到 EXCEL
```SAS
%macro export_file(datafile, outputPath, filename, sheetname);
	proc export data=&datafile
		%if %length(&filename)>0 %then 
			%str(outfile="&outputPath.\&filename");
		%else 
			%str(outfile="&outputPath.\&datafile");
		dbms=excel2002 replace;
		%if %length(&sheetname)>0 %then 
			%str(sheet="&sheetname";);
		%else 
			%str(sheet="&datafile";);
	run;
%mend;
```
##### > DEBUG 宏程序
```SAS
%macro macro_debug(switch, outfile_for_debug, skip_format, lrecl_option);
	%if %upcase(&switch) = ON %then %do;
		%delete_file(&outfile_for_debug);
		ods listing close;
		%if &lrecl_option = %str() %then %let lrecl_option = 150;
		filename mprint &outfile_for_debug lrecl=&lrecl_option; 
		options mfile;
		options mprint;
	%end;
	
	%else %if %upcase(&switch) = OFF %then %do;
		options nomfile;
		ods listing;
		%if &lrecl_option = %str() %then %let lrecl_option = 150;
		*Include format_mfile submacro if not already declared;
		%format_mfile(outfile_for_workpaper=&outfile_for_debug, skip_format=&skip_format, save_comments=1, lrecl_option=&lrecl_option);
	%end;
%mend;
```

##### > 清理 WORK 逻辑库
```SAS
%macro clean_Work (datasets);
	%if %length(&datasets)=0 %then %do;
		proc datasets lib=work nolist kill;
			quit;
		run;
	%end;
	%else %do;
		proc datasets lib=work memtype=data;
			 save &datasets;
		quit;
	%end;
%mend;

```

##### > PROC SORT 排序
```SAS
%macro sort(dataset,variables,nodupdataset);
	proc sort data=&dataset 
	%if %length(&nodupdataset)>0 %then %str(out=&nodupdataset nodupkey);
		;
		by &variables;
	run;
%mend;

```

---

<center>**本文终结，这么多考试应该是够用了。**</center>


  [1]: https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190318143433680-1808221835.png
  [2]: https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190319143139332-2122073094.png
  [3]: https://img2018.cnblogs.com/blog/1469136/201903/1469136-20190319143145018-1303102093.png